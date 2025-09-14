import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
// Optional: attempt to load BufferGeometryUtils if exists
let mergeGeometries = null;
try {
    const mod = await import('three/examples/jsm/utils/BufferGeometryUtils.js');
    mergeGeometries = mod.mergeGeometries;
} catch (e) { /* ignore */ }

let scene, camera, renderer, controls;
let meshes = {};
let assemblyData = null;
let jointState = {};

function initThree() {
    const container = document.getElementById('viewport');
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x111111);
    camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.1, 1000);
    camera.position.set(0, -120, 120);
    camera.lookAt(0, 0, 0);
    const light = new THREE.DirectionalLight(0xffffff, 1.0);
    light.position.set(50, -50, 100);
    scene.add(light);
    scene.add(new THREE.AmbientLight(0x404040));
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;
    controls.screenSpacePanning = false;
    controls.minDistance = 10;
    controls.maxDistance = 1000;
    animate();
    window.addEventListener('resize', onWindowResize);
}

function animate() {
    requestAnimationFrame(animate);
    if (controls) controls.update();
    renderer.render(scene, camera);
}

function onWindowResize() {
    const container = document.getElementById('viewport');
    const w = container.clientWidth;
    const h = container.clientHeight;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);
}

function clearScene() {
    for (const k in meshes) {
        scene.remove(meshes[k]);
    }
    meshes = {};
}

function buildGeometry(poly, thickness = 1) {
    // poly: {exterior: [[x,y],...], holes: [...]}
    const shape = new THREE.Shape(poly.exterior.map(p => new THREE.Vector2(p[0], p[1])));
    for (const hole of poly.holes) {
        const path = new THREE.Path(hole.map(p => new THREE.Vector2(p[0], p[1])));
        shape.holes.push(path);
    }
    const extrudeSettings = { depth: thickness || 1, bevelEnabled: false };
    return new THREE.ExtrudeGeometry(shape, extrudeSettings);
}

function applyTransform(matrixArray, mesh) {
    const m = new THREE.Matrix4();
    // Python stores row-major 4x4; Three.js expects column-major.
    // Convert by transposing.
    const flat = matrixArray.flat();
    const transposed = [
        flat[0], flat[4], flat[8], flat[12],
        flat[1], flat[5], flat[9], flat[13],
        flat[2], flat[6], flat[10], flat[14],
        flat[3], flat[7], flat[11], flat[15]
    ];
    m.fromArray(transposed);
    mesh.matrixAutoUpdate = false;
    mesh.matrix = m;
}

function loadAssembly(data) {
    assemblyData = data;
    clearScene();
    // Add parts
    const added = [];
    for (const part of data.parts) {
        if (part.profile2d) {
            const thickness = part.profile2d?.metadata?.thickness || 1;
            const geomList = [];
            for (const poly of part.profile2d.polygons) {
                geomList.push(buildGeometry(poly, thickness));
            }
            const geom = mergeGeometries ? mergeGeometries(geomList) : geomList[0];
            // Color precedence: part.material.color (hex string '#rrggbb' or number) else default blue.
            let colorVal = 0x2196f3;
            if (part.material && part.material.color) {
                const c = part.material.color;
                if (typeof c === 'number') {
                    colorVal = c;
                } else if (typeof c === 'string') {
                    // Strip leading '#' and parse hex
                    const hex = c.startsWith('#') ? c.slice(1) : c;
                    if (/^[0-9a-fA-F]{6}$/.test(hex)) {
                        colorVal = parseInt(hex, 16);
                    }
                }
            }
            const mat = new THREE.MeshStandardMaterial({ color: colorVal, metalness: 0.1, roughness: 0.8 });
            const mesh = new THREE.Mesh(geom, mat);
            applyTransform(part.transform, mesh);
            mesh.userData.partId = part.id;
            scene.add(mesh);
            meshes[part.id] = mesh;
            added.push(mesh);
        }
    }
    fitCameraToObjects(added);
    buildJointUI();
}

function isIdentityMatrix(flatM) {
    if (!flatM || flatM.length !== 16) return false;
    const id = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1];
    for (let i = 0; i < 16; i++) if (Math.abs(flatM[i] - id[i]) > 1e-9) return false;
    return true;
}

function buildJointUI() {
    const container = document.getElementById('jointControls');
    container.innerHTML = '';
    // Determine root drivers (drivers that are not themselves driven by another gear joint)
    const gearJoints = assemblyData.joints.filter(j => j.type === 'GearJoint');
    const drivenSet = new Set(gearJoints.map(j => j.driven));
    const rootDrivers = [...new Set(gearJoints.map(j => j.driver))].filter(d => !drivenSet.has(d));
    for (const driverId of rootDrivers) {
        const row = document.createElement('div');
        row.className = 'slider-row';
        const label = document.createElement('label');
        label.textContent = `Driver ${driverId} angle`;
        const input = document.createElement('input');
        input.type = 'range';
        input.min = '0';
        input.max = '360';
        input.value = jointState[driverId] || '0';
        input.addEventListener('input', () => {
            jointState[driverId] = parseFloat(input.value);
            updateKinematics();
        });
        row.appendChild(label);
        row.appendChild(input);
        container.appendChild(row);
    }
}

function updateKinematics() {
    const joints = assemblyData.joints.filter(j => j.type === 'GearJoint');
    if (!joints.length) return;
    // Build adjacency list driver -> [joint,...]
    const adj = new Map();
    for (const j of joints) {
        if (!adj.has(j.driver)) adj.set(j.driver, []);
        adj.get(j.driver).push(j);
    }
    const drivenSet = new Set(joints.map(j => j.driven));
    const rootDrivers = [...new Set(joints.map(j => j.driver))].filter(d => !drivenSet.has(d));
    // Angle map accumulates resolved angles
    const angleMap = new Map();
    // Seed roots
    for (const r of rootDrivers) angleMap.set(r, jointState[r] || 0);
    // BFS queue
    const q = [...rootDrivers];
    const partTeeth = (pid) => {
        const p = assemblyData.parts.find(pp => pp.id === pid);
        return p?.parameters?.teeth || 1;
    };
    while (q.length) {
        const cur = q.shift();
        if (!adj.has(cur)) continue;
        for (const j of adj.get(cur)) {
            const driverAngle = angleMap.get(cur) || 0;
            const ratio = (j.ratio != null) ? j.ratio : (partTeeth(j.driver) / partTeeth(j.driven));
            const drivenAngle = -driverAngle * ratio;
            if (!angleMap.has(j.driven)) {
                angleMap.set(j.driven, drivenAngle);
                q.push(j.driven);
            } else {
                // Already has an angle; skip (could add consistency check here)
            }
        }
    }
    // Helper to convert row-major JSON to Three matrix
    const toThree = (m) => {
        const f = m.flat();
        return new THREE.Matrix4().fromArray([
            f[0], f[4], f[8], f[12],
            f[1], f[5], f[9], f[13],
            f[2], f[6], f[10], f[14],
            f[3], f[7], f[11], f[15]
        ]);
    };
    // Apply rotations
    for (const [pid, ang] of angleMap.entries()) {
        const mesh = meshes[pid];
        if (!mesh) continue;
        mesh.matrixAutoUpdate = false;
        const baseRaw = assemblyData.parts.find(p => p.id === pid).transform;
        const base = toThree(baseRaw);
        const rot = new THREE.Matrix4().makeRotationZ(THREE.MathUtils.degToRad(ang));
        mesh.matrix = base.clone().multiply(rot);
    }
}

async function bootstrap() {
    initThree();
    const jc = document.getElementById('jointControls');
    const waiting = document.createElement('div');
    waiting.textContent = 'Waiting for /update POST ...';
    jc.appendChild(waiting);
    if (window.dcad.onAssemblyUpdate) {
        window.dcad.onAssemblyUpdate((data) => {
            console.log('[dcad_ui] Live update received');
            jc.innerHTML = '';
            loadAssembly(data);
        });
    }
}

function fitCameraToObjects(objs) {
    if (!objs.length) return;
    const box = new THREE.Box3();
    for (const o of objs) box.expandByObject(o);
    const size = new THREE.Vector3();
    box.getSize(size);
    const center = new THREE.Vector3();
    box.getCenter(center);
    const maxDim = Math.max(size.x, size.y, size.z);
    const dist = maxDim * 1.8;
    camera.position.set(center.x, center.y - dist, center.z + dist * 0.8);
    camera.lookAt(center);
}

bootstrap();
