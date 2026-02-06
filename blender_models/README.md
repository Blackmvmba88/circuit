# Blender Models for Circuit Components

This directory contains 3D models and scripts for generating electronic components using Blender.

## Directory Structure

```
blender_models/
├── scripts/           # Blender Python scripts for generating components
│   ├── component_generator.py   # Main 3D component generator
│   └── validate_circuit.py      # Circuit validation tool
├── components/        # Individual component .blend files (to be populated)
└── scenes/           # Complete circuit scene files (to be populated)
```

## Quick Start

### Method 1: Command-Line (Recommended)

Load a circuit directly from a `.circuit.json` file:

```bash
blender --python blender_models/scripts/component_generator.py -- examples/simple_circuit.circuit.json
```

This will:
- Launch Blender
- Parse the circuit JSON file
- Generate all components in 3D
- Set up camera and lighting
- Display the circuit in Blender's 3D viewport

**Available example circuits:**
```bash
# Simple LED circuit
blender --python blender_models/scripts/component_generator.py -- examples/simple_circuit.circuit.json

# Full circuit with 3D positioning
blender --python blender_models/scripts/component_generator.py -- examples/circuit_with_3d.circuit.json

# H-Bridge motor driver
blender --python blender_models/scripts/component_generator.py -- examples/h_bridge_motor_driver.circuit.json

# Voltage regulator (LM7805)
blender --python blender_models/scripts/component_generator.py -- examples/voltage_regulator_lm7805.circuit.json
```

### Method 2: Interactive Mode (Manual)

1. **Install Blender** (version 3.0+)
2. **Open Blender** and switch to the Scripting workspace
3. **Load the script**: Open `scripts/component_generator.py`
4. **Run the script**: Click the Run Script button (▶) or press Alt+P
5. **Create components**: Use the provided functions in the Python console

### Example Usage (Interactive)

```python
# Create an example circuit
create_example_circuit()

# Or create individual components
create_resistor_smd_0805("R1", location=(0, 0, 0), resistance_value="10K")
create_capacitor_smd_0805("C1", location=(5, 0, 0), capacitance_value="100nF")
create_ic_soic8("U1", location=(10, 0, 0))
create_led_smd_0805("LED1", location=(15, 0, 0), color="red")

# Load a circuit from JSON
load_circuit_from_json("/path/to/your/circuit.circuit.json")
```

## Available Components

### SMD Components
- **Resistor 0805**: Standard SMD resistor
- **Capacitor 0805**: Ceramic capacitor
- **LED 0805**: SMD LED (red, green, blue, yellow)

### Integrated Circuits
- **SOIC-8**: 8-pin small outline IC package

### Connectors
- **Pin Headers**: Configurable pin count (2.54mm pitch)

### PCB
- **PCB Board**: Customizable FR4 board with standard green finish

## Circuit JSON Format

Your `.circuit.json` files can include optional `model_3d` sections for precise 3D positioning:

```json
{
  "metadata": {
    "name": "My Circuit",
    "description": "Description here"
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
    }
  ]
}
```

**Note:** If `model_3d` sections are not present, components will be automatically arranged in a row.

## What You Can Do in Blender

Once your circuit is loaded:

* 🎥 **Navigate**: Orbit, pan, and zoom around your circuit
* 🎨 **Customize**: Change materials, colors, and lighting
* 📐 **Adjust**: Fine-tune component positions
* 📸 **Render**: Create high-quality images of your circuit
* 💾 **Export**: Save as STL, OBJ, glTF, FBX for other tools
* 🎞️ **Animate**: Create turntable animations or assembly sequences

## Tips & Tricks

1. **Camera Control**: Use numpad or middle mouse button to orbit
2. **Shading**: Switch to "Shading" workspace to adjust materials
3. **Rendering**: Press F12 to render the current view
4. **Export**: File → Export → choose your format
5. **Lighting**: Adjust the Sun light energy in Scene Properties

## Troubleshooting

### "File not found" error
Make sure to run the command from the repository root directory, or use absolute paths:
```bash
cd /path/to/circuit
blender --python blender_models/scripts/component_generator.py -- examples/simple_circuit.circuit.json
```

### Components not appearing
- Check that the JSON file is valid (use `test_json_loading.py` or `validate_circuit.py` first)
- Ensure component types are supported (resistor, capacitor, led, ic, connector, diode, voltage_regulator)
- Virtual components (power_supply, ground) won't generate 3D models

### Blender not found
Install Blender 3.x from [blender.org](https://www.blender.org/download/) and ensure it's in your PATH.

## Documentation

See the complete guide at: `docs/blender_usage_guide.md`

For EMI/noise design considerations: `docs/guidelines/emi_noise_prevention.md`

## Features

- ✅ Industry-standard component dimensions
- ✅ Realistic materials and colors
- ✅ EMI-aware spacing guidelines
- ✅ Easy-to-use Python API
- ✅ Export to STL, OBJ, glTF, FBX
- ✅ Integration with .circuit.json format
- ✅ Command-line circuit loading
- ✅ Auto-layout for circuits without 3D positions

## Contributing

To add new component types:

1. Follow the existing function structure
2. Use standard package dimensions from datasheets
3. Create realistic materials
4. Document the function with docstrings
5. Add usage examples

## License

MIT License - See LICENSE in root directory
