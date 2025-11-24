# Blender Models for Circuit Components

This directory contains 3D models and scripts for generating electronic components using Blender.

## Directory Structure

```
blender_models/
├── scripts/           # Blender Python scripts for generating components
│   └── component_generator.py
├── components/        # Individual component .blend files (to be populated)
└── scenes/           # Complete circuit scene files (to be populated)
```

## Quick Start

1. **Install Blender** (version 3.0+)
2. **Open Blender** and switch to the Scripting workspace
3. **Load the script**: Open `scripts/component_generator.py`
4. **Run the script**: Click the Run Script button (▶) or press Alt+P
5. **Create components**: Use the provided functions

### Example Usage

```python
# Create an example circuit
create_example_circuit()

# Or create individual components
create_resistor_smd_0805("R1", location=(0, 0, 0), resistance_value="10K")
create_capacitor_smd_0805("C1", location=(5, 0, 0), capacitance_value="100nF")
create_ic_soic8("U1", location=(10, 0, 0))
create_led_smd_0805("LED1", location=(15, 0, 0), color="red")
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

## Contributing

To add new component types:

1. Follow the existing function structure
2. Use standard package dimensions from datasheets
3. Create realistic materials
4. Document the function with docstrings
5. Add usage examples

## License

MIT License - See LICENSE in root directory
