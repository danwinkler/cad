# multipart module (current architecture)

Light‑weight API for composing mechanical assemblies from parametric part definitions (currently: sheet / gear parts) and exporting or streaming them to a live UI. Kinematics for simple gear trains are performed entirely client‑side inside the Electron/Three.js renderer (no Python solver at runtime).

Implemented today:
- Parametric sheet gear parts (`GearPartDefinition`) producing 2D profiles + metadata (pitch radius, addendum, etc.)
- `Assembly` + `PartInstance` with transforms, optional material/color metadata
- `GearJoint` relationships (driver → driven, ratio, backlash placeholder)
- JSON serialization (`assembly.to_dict`) consumed by UI
- Client-side hierarchical gear kinematic propagation (BFS over gear joint graph)
- `DXFExporter` for sheet outlines
- `DCADUIExporter` for pushing a live assembly to the running UI (`/update` endpoint)
- Examples: `gear_pair.py`, `gear_triplet.py`

Planned / not yet implemented in Python core (some are sketched below for roadmap clarity): additional joint types, on‑server solvers, 3D solids, analysis utilities, caching layers, legacy adapters beyond gears.

## Design Principles

1. Separation of Concerns
   - Geometry generation vs. assembly composition vs. export vs. simulation.
2. Extensibility by Protocol / Interface
   - Clear base classes / protocols allow downstream projects to register custom part generators or joints without touching core.
3. Immutable Geometry, Mutable Placement
   - Parts have intrinsic geometry (local space). Placement into an Assembly uses transforms + parameters; this simplifies reuse.
4. Declarative, Parameter-First
   - Encourage parametric definitions (e.g. GearModule(module=2, teeth=24)).
5. Lazy / Demand-Driven Generation
   - Heavy geometry (meshes, triangulation, path offsetting) generated only when required for a given export or simulation.
6. Pluggable Solvers
   - Kinematic, packing/nesting, interference check, clearance analysis.
7. Deterministic Outputs
   - Stable IDs for parts and joints for UI synchronization & caching.

## Current Layered View (trimmed to what exists)

```
User Code (examples/*.py)
  └─ Builds Assembly, adds GearPartDefinitions & GearJoints, pushes via DCADUIExporter

Assembly Layer
  ├─ Assembly (list of PartInstances + joints)
  ├─ PartInstance (definition + transform + material)
  └─ GearJoint (driver, driven, ratio, backlash placeholder)

Definition Layer
  └─ GearPartDefinition (sheet profile, pitch circle metadata)

Geometry Layer
  └─ Profile2D (shapely polygon(s) + metadata)

Export Layer
  ├─ DXFExporter (writes outlines)
  └─ DCADUIExporter (POST JSON to UI)

Client UI (Electron/Three.js)
  ├─ Parses assembly JSON
  ├─ Builds meshes from polygons (extruded thickness approximation)
  ├─ Builds gear joint graph; root driver sliders
  └─ Propagates angles BFS: driverAngle → drivenAngle = -driverAngle * ratio
```

## Key Abstractions (Proposed API Sketch)

### PartDefinition
Represents intrinsic geometry recipe. Instances may be reused in multiple places.
```python
class PartDefinition(Protocol):
    id: str  # stable
    def kind(self) -> str: ...  # 'sheet' | 'solid' | 'hybrid'
    def parameters(self) -> dict: ...
    def dependencies(self) -> list[PartDefinition]: ...  # optional composition
    def get_profile_2d(self, context: BuildContext) -> Profile2D | None: ...
    def get_solid_3d(self, context: BuildContext) -> Solid3D | None: ...
```

### PartInstance
Binds a definition into an Assembly with transform & material.
```python
@dataclass
class PartInstance:
    id: str
    definition: PartDefinition
    transform: Transform  # 4x4 or (pos, rot, scale)
    material: MaterialDefinition | None = None
    tags: set[str] = field(default_factory=set)
```

### Assembly
```python
class Assembly:
    def add_part(self, definition: PartDefinition, transform=None, material=None, tags=None) -> PartInstance: ...
    def add_subassembly(self, name: str) -> 'Assembly': ...
    def add_joint(self, joint: Joint): ...
    def solve(self, solver: ConstraintSolver | None = None): ...
    def find(self, predicate) -> list[PartInstance]: ...
    def export(self, exporter: Exporter, selection=None, **opts): ...
```

### GearJoint (current only joint)
Serialized fields:
```jsonc
{ "id": "j1", "type": "GearJoint", "driver": "pi1", "driven": "pi2", "ratio": 1.5, "backlash": 0.0 }
```
Ratio meaning: (pitch_radius_driver / pitch_radius_driven). Sign inversion handled in UI (mesh contact flips rotation direction each stage).

### Client-side Kinematics
Implemented in `dcad_ui/src/renderer.js`:
1. Discover gear joints; compute set of root drivers (drivers not driven elsewhere).
2. Each root driver gets a slider (0–360°).
3. BFS over driver→driven edges applying `drivenAngle = -driverAngle * ratio`.
4. Apply rotation about local Z by multiplying original (base) transform matrix with a Z-rotation.
5. Backlash not yet used (placeholder for future clearance visualization).

### Exporters
Each exporter implements:
```python
class Exporter(Protocol):
    def can_handle(self, part: PartDefinition) -> bool: ...
    def emit(self, assembly: Assembly, selection: list[PartInstance], ctx: ExportContext): ...
```

## Example Usage (current API)

Minimal gear pair:
```python
from cad.common.multipart import Assembly, GearPartDefinition, GearJoint, Transform, DCADUIExporter

asm = Assembly(name="gear_pair")
g1 = GearPartDefinition(teeth=24, tooth_width=1.0, thickness=3)
g2 = GearPartDefinition(teeth=12, tooth_width=1.0, thickness=3)
pr1 = g1.get_profile_2d(None).metadata["pitch_radius"]
pr2 = g2.get_profile_2d(None).metadata["pitch_radius"]
center = pr1 + pr2
a = asm.add_part(g1, transform=Transform.at(x=0), material={"color": "#1976d2"})
b = asm.add_part(g2, transform=Transform.at(x=center, rz=0.5 * 360 / g2.teeth), material={"color": "#ff9800"})
asm.add_joint(GearJoint(id="g1", driver=a, driven=b, ratio=pr1 / pr2))
asm.export(DCADUIExporter())  # pushes live update to UI
```

Triplet (A→B→C) example exists at `examples/gear_triplet.py` demonstrating hierarchical angle propagation.

## Serialization Shape

Top-level JSON (abridged):
```jsonc
{
  "name": "gear_pair",
  "version": 1,
  "parts": [
    {
      "id": "pi1",
      "kind": "sheet",
      "transform": [[1,0,0,x],[0,1,0,y],[0,0,1,z],[0,0,0,1]],
      "parameters": {"teeth":24, "thickness":3, ...},
      "material": {"color":"#1976d2"},
      "profile2d": {"polygons":[{"exterior":[[x,y],...],"holes":[]}],"metadata":{"pitch_radius":12.0,...}}
    }
  ],
  "joints": [ {"id":"g1","type":"GearJoint","driver":"pi1","driven":"pi2","ratio":1.2,"backlash":0.0} ]
}
```

Matrix convention: stored row‑major 4×4 (Python); UI converts to Three.js column‑major by transposing blocks when loading.

Color: `material.color` may be hex string ("#RRGGBB") or numeric. Optional.

Gear metadata: currently includes pitch_radius, outer_radius, addendum, dedendum, thickness.

## Migration from `lasercut` v1 (early thoughts)

Phased approach:
1. Adapter: Wrap `MultipartModel` -> `Assembly` with each `Model` -> `PartDefinition` (sheet) and `Part` -> `Profile2D`.
2. Provide bridging exporters that delegate to existing DXF / SCAD export logic.
3. Gradually re-implement geometry as new PartDefinitions (e.g., TextGlyph, Bendy, FontRenderer integration) using shared utility functions.
4. Deprecate direct use of `MultipartModel` once parity achieved.

### Mapping Table
| v1 Concept           | v2 Equivalent                   |
| -------------------- | ------------------------------- |
| MultipartModel       | Assembly                        |
| Model                | PartDefinition + PartInstance   |
| Part (polygon+meta)  | SheetPartDefinition / Profile2D |
| Renderer transforms  | Transform on PartInstance       |
| render_parts / DXF   | DXFExporter                     |
| get_total_cut_length | CutLengthAnalyzer               |

## Transforms
Represent as small utility struct:
```python
@dataclass(frozen=True)
class Transform:
    matrix: np.ndarray  # 4x4
    @staticmethod
    def identity(): ...
    @staticmethod
    def at(x=0,y=0,z=0, rx=0, ry=0, rz=0, scale=1.0): ...
    def compose(self, other: 'Transform') -> 'Transform': ...
```

## Lazy Geometry Caching
- Each PartDefinition function (`get_profile_2d`, `get_solid_3d`) can use an internal hash of parameters to memoize.
- Assembly holds a central `GeometryCache` keyed by (part_def_id, kind, param_hash).

## Kerf & Manufacturing Adjustments
Attach to `MaterialDefinition` or a `ManufacturingProfile`:
```python
@dataclass
class MaterialDefinition:
    name: str
    thickness: float
    kerf: float = 0.0
    density: float | None = None
    color: tuple[int,int,int] | None = None
```
Downstream exporters (DXF/SVG) can perform outward/inward offsets per edge classification if needed.

## Error Handling & Validation
- Clear exceptions: `GeometryGenerationError`, `JointResolutionError`, `ExportError`.
- Validator pass before export: ensure no unresolved transforms or unsatisfied constraints.

## Suggested Implementation Phases
1. Scaffolding: directories, base protocols, minimal `Assembly`, `Transform`, `PartDefinition` + simple `SheetPartDefinition` using shapely polygon.
2. Export MVP: DXF (via existing logic), SCAD, STL (triangulate sheet via extrusion or pass-through for 3D parts).
3. Joints & Solver: Rigid, Revolute, Prismatic. Provide simple forward kinematics.
4. Procedural Parts: SpurGear, Rack, TextGlyph (reuse font utilities), BendySheet.
5. Analysis utilities: interference, cut length, mass properties.
6. Adapters and migration helpers; deprecation warnings in `lasercut`.
7. Advanced joints (gear meshing parameters, backlash), improved solver (numeric constraints).

## Module Layout (Proposed)
```
multipart/
  __init__.py
  assembly.py              # Assembly, PartInstance, query helpers
  definitions/
    __init__.py
    base.py                # PartDefinition base + BuildContext
    sheet.py               # SheetPartDefinition
    solid.py               # SolidPartDefinition
    gear.py                # Spur gear, rack, param families
    text.py                # TextGlyph / Font-based parts
    bendy.py               # Bendy / path-based deformation
  geometry/
    __init__.py
    profile2d.py           # Profile2D wrapper (shapely + metadata)
    solid3d.py             # Solid3D wrapper (mesh/CSG/trimesh)
    transform.py           # Transform struct & utilities
    cache.py               # Geometry cache
  joints/
    __init__.py
    base.py                # Joint protocol + DOF structures
    rigid.py
    revolute.py
    prismatic.py
    gear_joint.py
  # (Solver module removed; kinematics handled client-side in UI for now)
  export/
    __init__.py
    base.py                # Exporter protocol + ExportContext
    dxf_exporter.py
    svg_exporter.py
    scad_exporter.py
    stl_exporter.py
    nesting.py             # Packing/nesting algorithms adapters
  analysis/
    __init__.py
    interference.py
    cutlength.py
    massprops.py
  materials/
    __init__.py
    material.py            # MaterialDefinition
    library.py             # Common presets (e.g., birch_3mm, pla_0.2)
  adapters/
    __init__.py
    legacy_lasercut.py     # Bridge to v1 models
  util/
    __init__.py
    idgen.py               # Stable ID generation
    logging.py
    hashing.py             # Param hashing for cache keys
```

## Minimal Immediate Deliverable (Phase 1 Skeleton)
- Provide `Assembly`, base `PartDefinition`, a simple `SheetPartDefinition` that wraps a shapely polygon, and a DXF export stub that delegates to existing code paths.

### Current Implementation Snapshot
Implemented:
* `Assembly`, `PartInstance`, `Transform`
* `GearPartDefinition` (+ profile metadata)
* `GearJoint` + client-side kinematic graph (BFS)
* `DXFExporter`, `DCADUIExporter`
* Examples: `gear_pair.py`, `gear_triplet.py`

Not yet implemented (roadmap): other joint types, server-side solver, solids, nesting/packing integration, analysis utilities, caching, legacy adapters.

## Open Questions
- Should transforms be stored as numpy or a small custom float tuple for serialization efficiency? (Leaning: numpy 4x4; provide `.to_json()`)
- Gear meshing: encode as special joint or purely geometric constraint? (Leaning: specialized `GearJoint` deriving from `Joint`.)
- Packing: incorporate polygon nesting library now or preserve existing physics packer adapter until later? (Leaning: adapter first.)
- Thread-safe cache? (Probably unnecessary initially.)

## Roadmap (high-level)
1. Additional procedural parts (rack, pulley, text glyph)
2. Joint types (revolute, prismatic) & optional dependency solver
3. Geometry caching & mass properties
4. Additional exporters (SVG nesting, STL extrusion of sheets)
5. Visual overlays (pitch circles, joint axes) in UI
6. Backlash visualization & interactive joint graph

---
This README reflects the code as of the current commit: client-side kinematics, JSON streaming via `DCADUIExporter`, and gear-focused examples.
