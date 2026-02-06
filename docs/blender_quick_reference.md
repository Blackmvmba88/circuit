# Blender 3D Visualization - Quick Reference

## One-Liner Command

```bash
blender --python blender_models/scripts/component_generator.py -- <path-to-circuit.json>
```

## Examples

### Basic Usage
```bash
# From repository root
blender --python blender_models/scripts/component_generator.py -- examples/simple_circuit.circuit.json
```

### Background Mode (No GUI)
```bash
blender --background --python blender_models/scripts/component_generator.py -- examples/circuit_with_3d.circuit.json
```

### Render Directly to File
```bash
blender --background \
  --python blender_models/scripts/component_generator.py \
  -- examples/circuit_with_3d.circuit.json \
  --render-output output.png
```

## Supported Components

| Component Type | 3D Model | Auto-Layout Support |
|----------------|----------|---------------------|
| `resistor` | ✅ 0805 SMD | ✅ Yes |
| `capacitor` | ✅ 0805 SMD | ✅ Yes |
| `led` | ✅ 0805 SMD | ✅ Yes |
| `ic` | ✅ SOIC-8 | ✅ Yes |
| `connector` | ✅ Pin Header | ✅ Yes |
| `power_supply` | ⚪ Virtual | - |
| `ground` | ⚪ Virtual | - |

## Keyboard Shortcuts in Blender

### Navigation
- **Orbit**: Middle Mouse Button (or Scroll Wheel Click)
- **Pan**: Shift + Middle Mouse
- **Zoom**: Scroll Wheel
- **Frame All**: Home key

### Views
- **Front**: Numpad 1
- **Right**: Numpad 3
- **Top**: Numpad 7
- **Camera**: Numpad 0
- **Toggle Perspective/Ortho**: Numpad 5

### Rendering
- **Render Image**: F12
- **Render Animation**: Ctrl + F12

### Export
File → Export → Select format (STL, OBJ, glTF, FBX)

## Pre-Flight Check

Before running the command, verify your circuit JSON:

```bash
python blender_models/scripts/test_json_loading.py your_circuit.circuit.json
```

This will show:
- ✅ JSON validity
- 📋 Component list
- ⚠️ Potential issues
- 📍 Which components will be auto-laid out

## Troubleshooting

### Command not found
```bash
# Use full path (macOS example)
/Applications/Blender.app/Contents/MacOS/Blender --python ...

# Or add Blender to PATH
export PATH="/Applications/Blender.app/Contents/MacOS:$PATH"
```

### File not found
```bash
# Make sure you're in the repository root
cd /path/to/circuit
pwd  # Should show .../circuit

# Then run the command
blender --python blender_models/scripts/component_generator.py -- examples/simple_circuit.circuit.json
```

### Empty scene
- Press **Home** key to frame all objects
- Check Blender console for errors (Window → Toggle System Console)

## JSON Format Quick Reference

### Minimal (Auto-Layout)
```json
{
  "metadata": {"name": "My Circuit"},
  "components": [
    {"id": "R1", "type": "resistor", "value": "10K"},
    {"id": "LED1", "type": "led", "color": "red"}
  ]
}
```

### With 3D Positioning
```json
{
  "board": {
    "dimensions": {"width": 60, "height": 40, "thickness": 1.6},
    "model_3d": {"position": {"x": 0, "y": 0, "z": -0.8}}
  },
  "components": [
    {
      "id": "R1",
      "type": "resistor",
      "value": "10K",
      "model_3d": {
        "position": {"x": -10, "y": 0, "z": 0},
        "params": {"resistance_value": "10K"}
      }
    }
  ]
}
```

## Output Formats

### For 3D Printing
Export as **STL**: File → Export → Stl (.stl)

### For Web Viewers (Three.js)
Export as **glTF/GLB**: File → Export → glTF 2.0 (.glb/.gltf)

### For CAD/Game Engines
Export as **FBX**: File → Export → FBX (.fbx)

### For Universal 3D
Export as **OBJ**: File → Export → Wavefront (.obj)

## What You Get

✅ Geometric 3D representation of your circuit  
✅ Realistic component appearance  
✅ Proper scaling (1 Blender unit = 1mm)  
✅ Camera and lighting setup  
✅ Ready to render or export  

❌ NOT electrical simulation (use SPICE for that)

## Full Documentation

- **Complete Guide**: [`docs/blender_3d_visualization.md`](../docs/blender_3d_visualization.md)
- **Component Reference**: [`blender_models/README.md`](../blender_models/README.md)
- **Script Source**: [`blender_models/scripts/component_generator.py`](../blender_models/scripts/component_generator.py)

---

**Quick tip**: Start with `examples/circuit_with_3d.circuit.json` to see a fully configured circuit with proper 3D positioning! 🚀
