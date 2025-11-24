# Circuit Adapters

This directory contains adapters for converting between the `.circuit.json` format and other EDA (Electronic Design Automation) tools.

## Available Adapters

### Altium Designer Adapter

**Script**: `circuit_to_altium.py`

Exports `.circuit.json` files to Altium Designer compatible formats.

**Usage**:
```bash
python3 adapters/circuit_to_altium.py <input.circuit.json> [output_directory]
```

**Example**:
```bash
# Export simple circuit
python3 adapters/circuit_to_altium.py examples/simple_circuit.circuit.json altium_export/

# Export complex circuit with 3D models
python3 adapters/circuit_to_altium.py examples/circuit_with_3d.circuit.json my_altium_project/
```

**Output Files**:
- `component_library.csv` - Component definitions for Altium library import
- `netlist.net` - Protel format netlist for circuit connectivity
- `bom.csv` - Bill of Materials
- `component_placement.csv` - PCB component placement coordinates
- `board_outline.txt` - PCB dimensions and specifications
- `design_rules.txt` - Recommended design rules based on circuit specifications
- `ALTIUM_IMPORT_GUIDE.txt` - Step-by-step instructions for importing into Altium

**Features**:
- ✅ Component library export (CSV format)
- ✅ Netlist export (Protel format)
- ✅ Bill of Materials with grouped components
- ✅ Component placement coordinates for PCB layout
- ✅ Board outline dimensions
- ✅ Design rules export (EMI/EMC compliance, thermal, etc.)
- ✅ Comprehensive import guide
- ✅ Support for SMD components (0805, SOIC, etc.)
- ✅ Automatic footprint mapping
- ✅ Value formatting (resistors, capacitors, etc.)

**Supported Component Types**:
- Resistors (SMD packages)
- Capacitors (SMD packages)
- LEDs (SMD packages)
- Integrated Circuits (SOIC, QFN, etc.)
- Connectors (through-hole and SMD)

---

## Future Adapters (Planned)

### KiCAD Adapter
- Export to KiCAD schematic and PCB formats
- Import from KiCAD to `.circuit.json`

### EAGLE Adapter
- Export to Autodesk EAGLE format
- Import from EAGLE XML

### SPICE Adapter
- Export to SPICE netlist for circuit simulation
- Support for LTspice and ngspice

### EasyEDA Adapter
- Export to EasyEDA JSON format
- Import from EasyEDA

### Gerber Export
- Generate Gerber files directly from `.circuit.json`
- Support for RS-274X format

---

## Creating Custom Adapters

To create a new adapter, follow this template:

```python
#!/usr/bin/env python3
"""
My EDA Tool Adapter

Description of what this adapter does.
"""

import json
import sys
from pathlib import Path

class MyToolExporter:
    def __init__(self, circuit_data, output_dir):
        self.circuit = circuit_data
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_all(self):
        """Main export function."""
        # Implement your export logic here
        pass

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 circuit_to_mytool.py <input.circuit.json> [output_dir]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "mytool_export"
    
    with open(input_file, 'r') as f:
        circuit_data = json.load(f)
    
    exporter = MyToolExporter(circuit_data, output_dir)
    exporter.export_all()

if __name__ == '__main__':
    main()
```

### Adapter Guidelines

1. **Input Format**: Always accept `.circuit.json` as input
2. **Output Directory**: Create a separate directory for all output files
3. **Documentation**: Include a guide for importing into the target tool
4. **Error Handling**: Provide clear error messages
5. **Validation**: Validate input before processing
6. **Metadata**: Preserve circuit metadata in exports
7. **Testing**: Test with both simple and complex circuits

---

## Testing Adapters

Test your adapter with the example circuits:

```bash
# Test with simple circuit
python3 adapters/circuit_to_mytool.py examples/simple_circuit.circuit.json test_output/

# Test with complex circuit
python3 adapters/circuit_to_mytool.py examples/circuit_with_3d.circuit.json test_output/

# Verify output files
ls -lh test_output/
```

---

## Contributing

To contribute a new adapter:

1. Create your adapter script in this directory
2. Add documentation to this README
3. Include example usage
4. Test with provided example circuits
5. Submit a Pull Request

See `CONTRIBUTING.md` in the root directory for more details.

---

## Support

For questions or issues with adapters:
- Open an issue: https://github.com/Blackmvmba88/circuit/issues
- Tag with `adapter` label
- Include example circuit and error messages

---

## License

All adapters are licensed under MIT License - see `LICENSE` in the root directory.
