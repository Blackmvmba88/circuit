# Blender 3D Circuit Visualization Guide

## Overview

This guide explains how to visualize your circuit designs in 3D using Blender. The circuit project includes a complete pipeline to transform your `.circuit.json` files into fully rendered 3D models that you can view, modify, and export.

## The Big Picture

Think of this as "compiling" your circuit to 3D geometry:

```
Circuit JSON → Blender Script → 3D Scene → Visualization/Rendering
```

Your circuit description becomes a physical-looking 3D object that you can inspect from any angle, just like holding the actual PCB in your hands.

## Prerequisites

- **Blender 3.0+** installed and accessible from command line
- This repository cloned locally
- A `.circuit.json` file (examples provided in `examples/`)

### Installing Blender

1. Download from [blender.org](https://www.blender.org/download/)
2. Install for your platform (Windows, macOS, Linux)
3. Add to PATH (optional but recommended):
   - **Linux/macOS**: Usually automatic or add to `~/.bashrc`
   - **Windows**: Add Blender's installation directory to system PATH

## Quick Start

### Basic Usage

From the repository root, run:

```bash
blender --python blender_models/scripts/component_generator.py -- examples/circuit_with_3d.circuit.json
```

**What happens:**
1. Blender launches in GUI mode
2. The Python script executes automatically
3. Your circuit appears in 3D space
4. Camera and lighting are configured
5. You can now navigate, render, or export

### Running in Background Mode

To generate without the GUI (useful for automation):

```bash
blender --background --python blender_models/scripts/component_generator.py -- examples/circuit_with_3d.circuit.json
```

Add `--render-output output.png` to render directly to a file.

## Available Example Circuits

Try these circuits that are included in the repository:

### 1. Simple LED Circuit
```bash
blender --python blender_models/scripts/component_generator.py -- examples/simple_circuit.circuit.json
```
A basic LED circuit with resistor. Components will be auto-arranged since it doesn't have 3D position data.

### 2. Full Circuit with 3D Layout
```bash
blender --python blender_models/scripts/component_generator.py -- examples/circuit_with_3d.circuit.json
```
Complete circuit with ICs, capacitors, resistors, LEDs, and connectors. This has precise 3D positioning defined.

### 3. H-Bridge Motor Driver
```bash
blender --python blender_models/scripts/component_generator.py -- examples/h_bridge_motor_driver.circuit.json
```
Motor control circuit (will auto-layout).

### 4. Voltage Regulator
```bash
blender --python blender_models/scripts/component_generator.py -- examples/voltage_regulator_lm7805.circuit.json
```
LM7805 based power supply circuit (will auto-layout).

## What You Can Do in Blender

Once your circuit is loaded, you have full access to Blender's capabilities:

### Navigation
- **Orbit**: Middle mouse button drag (or scroll wheel click + drag)
- **Pan**: Shift + Middle mouse button
- **Zoom**: Scroll wheel
- **Reset view**: Home key or View → Frame All

### Viewing
- **Switch views**: Numpad 1 (front), 3 (side), 7 (top)
- **Camera view**: Numpad 0
- **Perspective/Ortho toggle**: Numpad 5

### Rendering
1. Press **F12** to render the current view
2. Save the render: Image → Save As
3. For animations: Set keyframes and render animation (Render → Render Animation)

### Exporting
File → Export → Choose format:
- **STL**: For 3D printing
- **OBJ**: Universal 3D format
- **glTF/GLB**: For web viewers (Three.js, etc.)
- **FBX**: For game engines and CAD tools

### Materials and Lighting
1. Switch to **Shading** workspace (top tabs)
2. Select an object
3. Adjust material properties in the shader editor
4. Add more lights: Add → Light → (Sun, Point, Area, etc.)

## Understanding the .circuit.json Format

### Minimal Circuit (Auto-Layout)

If your circuit doesn't have 3D position data, components will be automatically arranged:

```json
{
  "metadata": {
    "name": "My Circuit",
    "description": "A simple circuit"
  },
  "components": [
    {
      "id": "R1",
      "type": "resistor",
      "value": "10K"
    },
    {
      "id": "LED1",
      "type": "led",
      "color": "red"
    }
  ]
}
```

### Circuit with 3D Positioning

For precise control, add `model_3d` sections:

```json
{
  "metadata": {
    "name": "Positioned Circuit"
  },
  "board": {
    "dimensions": {
      "width": 60,
      "height": 40,
      "thickness": 1.6
    },
    "model_3d": {
      "position": { "x": 0, "y": 0, "z": -0.8 }
    }
  },
  "components": [
    {
      "id": "R1",
      "type": "resistor",
      "value": "10K",
      "model_3d": {
        "generator": "create_resistor_smd_0805",
        "position": { "x": -10, "y": 0, "z": 0 },
        "params": { "resistance_value": "10K" }
      }
    },
    {
      "id": "C1",
      "type": "capacitor",
      "model_3d": {
        "generator": "create_capacitor_smd_0805",
        "position": { "x": 0, "y": 0, "z": 0 },
        "params": { "capacitance_value": "100nF" }
      }
    },
    {
      "id": "U1",
      "type": "ic",
      "package": "SOIC8",
      "model_3d": {
        "generator": "create_ic_soic8",
        "position": { "x": 10, "y": 10, "z": 0 }
      }
    }
  ],
  "blender_generation": {
    "render_options": {
      "engine": "EEVEE",
      "resolution": [1920, 1080],
      "camera_position": [50, -50, 40],
      "camera_rotation": [1.1, 0, 0.785]
    }
  }
}
```

### Supported Component Types

| Type | Package | Generator Function |
|------|---------|-------------------|
| resistor | 0805 | `create_resistor_smd_0805` |
| capacitor | 0805 | `create_capacitor_smd_0805` |
| ic | SOIC8 | `create_ic_soic8` |
| led | 0805 | `create_led_smd_0805` |
| connector | Header | `create_header_connector` |

**Virtual components** (power_supply, ground) are functional but don't generate 3D models.

## Advanced Usage

### Custom Camera Positions

Edit the `blender_generation` section in your JSON:

```json
"blender_generation": {
  "render_options": {
    "camera_position": [30, -30, 25],
    "camera_rotation": [1.0, 0, 0.7]
  }
}
```

### Batch Processing

Create a script to process multiple circuits:

```bash
#!/bin/bash
for circuit in examples/*.circuit.json; do
  echo "Processing $circuit..."
  blender --background --python blender_models/scripts/component_generator.py -- "$circuit" \
    --render-output "renders/$(basename $circuit .circuit.json).png"
done
```

### Integration with CI/CD

Generate 3D previews automatically in your workflow:

```yaml
# .github/workflows/generate-3d-previews.yml
- name: Generate 3D Preview
  run: |
    blender --background \
      --python blender_models/scripts/component_generator.py \
      -- examples/circuit_with_3d.circuit.json
```

## Troubleshooting

### Error: "Blender: command not found"
**Solution**: Install Blender and add it to your PATH, or use the full path:
```bash
/Applications/Blender.app/Contents/MacOS/Blender --python ...  # macOS
"C:\Program Files\Blender Foundation\Blender 3.6\blender.exe" --python ...  # Windows
```

### Error: "File not found"
**Solution**: Make sure you're running from the repository root:
```bash
cd /path/to/circuit
blender --python blender_models/scripts/component_generator.py -- examples/simple_circuit.circuit.json
```

### Components Not Appearing
1. Check the JSON is valid: `python blender_models/scripts/test_json_loading.py your_circuit.json`
2. Verify component types are supported
3. Check Blender console for error messages (Window → Toggle System Console)

### Empty Scene
- The PCB might be outside the camera view. Press **Home** to frame all objects.
- Check the Outliner panel (top-right) to see if objects were created.

### Python Errors in Blender
- Open Blender's console: Window → Toggle System Console
- Look for detailed error messages
- Common issues: JSON syntax errors, missing required fields

## Testing Without Blender

To verify your JSON file is correct before loading in Blender:

```bash
python blender_models/scripts/test_json_loading.py examples/simple_circuit.circuit.json
```

This will show you:
- ✅ If the JSON is valid
- 📋 Circuit metadata
- 🔧 Component list and status
- ⚠️  Any potential issues

## Next Steps

### For Documentation
- Capture turntable animations
- Render high-quality stills for datasheets
- Export to web viewers (Three.js/WebGL)

### For Mechanical Design
- Export to STEP for CAD integration
- Check clearances and component heights
- Verify enclosure fit

### For Teaching
- Create assembly animations
- Show component placement sequence
- Highlight design decisions visually

## Important Notes

### This is Geometric Visualization, Not Electrical Simulation

- ✅ **You get**: Physical 3D representation of your circuit
- ✅ **You can**: View, render, export, document
- ❌ **You don't get**: Electrical behavior, current flow, voltages
- ℹ️  **For simulation**: Use SPICE, Falstad, or other circuit simulators

This tool is perfect for:
- Design review and documentation
- Mechanical clearance checking
- Marketing and presentation materials
- Teaching and learning about PCB layout
- Integration planning with enclosures

### Coordinate System

- Units are in millimeters (1 Blender unit = 1mm)
- Origin (0,0,0) is the center of the PCB by default
- Z-axis points up (away from PCB surface)
- Components sit on top of the PCB (positive Z)

## Examples Gallery

After running the examples, you should see:

1. **Simple Circuit**: Resistor and LED in a row on a small board
2. **Full Circuit**: Complete layout with IC, multiple passives, LEDs, connector
3. **Motor Driver**: H-bridge with MOSFETs/transistors (auto-arranged)
4. **Voltage Regulator**: LM7805 with capacitors (auto-arranged)

## Getting Help

If you encounter issues:

1. Check this guide first
2. Verify JSON syntax with the test script
3. Check Blender console for Python errors
4. Review the component generator code: `blender_models/scripts/component_generator.py`
5. Open an issue on GitHub with:
   - Your `.circuit.json` file
   - Error messages from Blender console
   - Steps to reproduce

## Contributing

Want to add more component types? See:
- `blender_models/scripts/component_generator.py` for examples
- Follow the existing patterns for consistency
- Use real-world dimensions from datasheets
- Add materials that match actual components

## License

MIT License - See LICENSE in root directory

---

**Happy visualizing!** 🎨🔌✨
