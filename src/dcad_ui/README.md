# DCAD UI (Electron Prototype)

Prototype Electron + Three.js viewer for multipart assembly JSON.

Features:
- Receives serialized assembly JSON exclusively via HTTP POST (`/update`)
- Renders sheet parts as extruded 2D profiles (depth=1)
- Slider controls for GearJoint driver angles (client-side kinematics)
- Live update endpoint (POST http://localhost:5123/update) for streaming assemblies from Python

## Run
```
npm install
npm start
```

## Live Update Workflow
1. Start the Electron app (`npm start`). It launches an HTTP server on `http://localhost:5123`.
2. Run your Python script (e.g. `gear_pair.py`). It POSTs the serialized assembly JSON to `/update`.
3. The UI receives an `assembly-update` IPC event and re-renders automatically.

Optional curl example:
```
curl -X POST http://localhost:5123/update -H "Content-Type: application/json" -d @gear_pair.json
```

Health check:
```
curl http://localhost:5123/health
```

## JSON Format (subset)
```
{
  "name": "gear_pair",
  "parts": [
    {"id":"pi1","definition_id":"gear_ab12","kind":"sheet","transform":[[...4 floats] x4],"parameters":{"teeth":24,...},"profile2d":{"polygons":[{"exterior":[[x,y],...],"holes":[]}],"metadata":{"pitch_radius":..}}}
  ],
  "joints": [
    {"id":"g1","type":"GearJoint","driver":"pi1","driven":"pi2","ratio":0.5,"backlash":0.0}
  ]
}
```

## Next Improvements
- Graph-based multi-stage joint propagation (chains, networks)
- Part selection + metadata panel
- 3D solid part support (beyond sheet extrusion)
- Basic theming & persistence of last received assembly
- Optional WebSocket streaming for lower latency updates
