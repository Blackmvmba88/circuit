# Altium Designer Export - Example Usage

This document provides practical examples of using the Altium Designer export adapter.

## Quick Start

### Basic Export
```bash
# Export a simple circuit
python3 adapters/circuit_to_altium.py examples/simple_circuit.circuit.json output/

# Output:
# output/
#   ├── ALTIUM_IMPORT_GUIDE.txt
#   ├── board_outline.txt
#   ├── bom.csv
#   ├── component_library.csv
#   ├── component_placement.csv
#   ├── design_rules.txt
#   └── netlist.net
```

### Export with Custom Output Directory
```bash
python3 adapters/circuit_to_altium.py examples/circuit_with_3d.circuit.json my_project/altium/
```

## Generated Files Explained

### 1. component_library.csv
Component definitions for importing into Altium's library system.

**Format**:
```csv
Designator,Description,Footprint,Value,Manufacturer,PartNumber,Type,Package
"R1","Pull-up resistor","RES-0805","10K","","","resistor","0805"
"C1","Decoupling capacitor","CAP-0805","100nF","","","capacitor","0805"
```

**Use**: Import this CSV into an Integrated Library in Altium.

### 2. netlist.net
Circuit connectivity in Protel format (Altium's native netlist format).

**Format**:
```
[
  Circuit exported from example-circuit
  Format: Protel Netlist
]

(
 ( R1 RES-0805
  1 VCC
  2 SIGNAL1
 )
)
```

**Use**: Import directly into Altium PCB or schematic document.

### 3. bom.csv
Bill of Materials with components grouped by value and package.

**Format**:
```csv
Item,Quantity,Designator,Description,Footprint,Value,Manufacturer,Part Number,Type
1,3,"R1, R2, R3","Current limiting","RES-0805","1K","","","resistor"
```

**Use**: 
- Component procurement
- Manufacturing documentation
- Cost estimation

### 4. component_placement.csv
PCB component placement coordinates and rotation.

**Format**:
```csv
Designator,Footprint,Mid X,Mid Y,Rotation,Layer,Comment
"R1","RES-0805",10.5,20.3,0,"Top","Pull-up resistor"
```

**Use**: Import into Altium PCB to automatically place components.

### 5. board_outline.txt
PCB physical dimensions and specifications.

**Content**:
```
Width:     60 mm
Height:    40 mm
Thickness: 1.6 mm
Layers:    2
Material:  FR4
```

**Use**: Reference when creating board outline in Altium.

### 6. design_rules.txt
Recommended design rules based on circuit specifications and EMI requirements.

**Content**:
```
EMI/EMC Compliance:
  Standard: FCC Part 15 Class B
  Trace Spacing: 0.2 mm
  Power Trace Width: 0.5 mm

Suggested Altium Design Rules:
  - Minimum clearance: 0.2 mm
  - Power nets: Min 0.5 mm
```

**Use**: Configure design rules in Altium PCB editor.

### 7. ALTIUM_IMPORT_GUIDE.txt
Step-by-step instructions for importing all files into Altium Designer.

**Use**: Follow this guide to complete the import process.

## Complete Workflow Example

### Step 1: Design Circuit in .circuit.json
```json
{
  "metadata": {
    "name": "led-blinker",
    "version": "1.0.0"
  },
  "components": [
    {
      "id": "R1",
      "type": "resistor",
      "package": "0805",
      "params": { "resistance_ohm": 1000 }
    }
  ]
}
```

### Step 2: Export to Altium
```bash
python3 adapters/circuit_to_altium.py my_circuit.circuit.json altium_files/
```

### Step 3: Import in Altium Designer

1. **Create Project**
   - File → New → Project → PCB Project
   - Name: led-blinker

2. **Import Component Library**
   - File → New → Library → Integrated Library
   - Tools → Import → CSV
   - Select: `altium_files/component_library.csv`

3. **Create Schematic**
   - File → New → Schematic
   - Design → Import Changes from → `altium_files/netlist.net`

4. **Create PCB**
   - File → New → PCB
   - Design → Board Shape → Define from selected objects
   - Use dimensions from `board_outline.txt`

5. **Import Component Placement**
   - File → Import → Component Positions
   - Select: `altium_files/component_placement.csv`

6. **Apply Design Rules**
   - Design → Rules
   - Refer to `design_rules.txt`

7. **Route and Finish**
   - Route traces
   - Add ground plane
   - Run DRC
   - Generate Gerbers

## Tips and Best Practices

### Component Footprints
The adapter automatically maps common packages to Altium footprints:
- `0805` → `RES-0805` or `CAP-0805` (depending on component type)
- `SOIC8` → `SOIC-8_3.9x4.9mm_P1.27mm`
- `QFN32` → `QFN-32-1EP_5x5mm_P0.5mm`

**Tip**: Verify footprints match your actual components before ordering PCBs.

### Value Formatting
Values are automatically formatted in standard notation:
- Resistors: `10K`, `1M`, `330R`
- Capacitors: `100nF`, `10uF`, `22pF`

### EMI/EMC Compliance
Design rules are exported based on the `design_rules` section in your `.circuit.json`:
```json
{
  "design_rules": {
    "emi_compliance": {
      "standard": "FCC Part 15 Class B",
      "trace_spacing_mm": 0.2,
      "power_trace_width_mm": 0.5
    }
  }
}
```

These are translated to Altium-compatible rule descriptions.

### Bill of Materials
Components with the same type, value, and package are automatically grouped in the BOM:
```csv
1,3,"R1, R2, R3","Current limiting","RES-0805","1K",...
```

This makes ordering components easier and more cost-effective.

## Troubleshooting

### Issue: Missing Footprints in Altium
**Solution**: Check `component_library.csv` and verify footprints exist in your Altium libraries. Update footprints manually if needed.

### Issue: Component Positions Incorrect
**Solution**: 
1. Verify units are set to millimeters when importing placement CSV
2. Check that coordinate system origin matches between circuit design and Altium

### Issue: Netlist Import Fails
**Solution**: 
1. Ensure component designators in schematic match those in netlist
2. Verify all components are in your library before importing netlist

### Issue: Design Rules Not Applied
**Solution**: 
1. Manually configure rules in Altium using `design_rules.txt` as reference
2. Test with DRC (Design Rule Check) after configuration

## Advanced Usage

### Custom Footprint Mapping
Edit the `_map_package_to_footprint()` method in `circuit_to_altium.py` to add custom mappings:

```python
footprint_map = {
    '0805': 'RES-0805',
    'MY_CUSTOM_PACKAGE': 'ALTIUM_FOOTPRINT_NAME',
}
```

### Adding Manufacturer Part Numbers
Include manufacturer data in your `.circuit.json`:

```json
{
  "params": {
    "resistance_ohm": 10000,
    "manufacturer": "Yageo",
    "part_number": "RC0805FR-0710KL"
  }
}
```

This will be included in the BOM and component library exports.

## Integration with Other Tools

### From KiCAD to Altium via .circuit.json
1. Export KiCAD schematic (future: use `kicad_to_circuit.py`)
2. Convert to `.circuit.json`
3. Export to Altium using this adapter

### From Blender 3D Models
If using the Blender 3D modeling system:
1. Generate circuit in Blender
2. Save as `.circuit.json` with 3D model references
3. Export to Altium
4. 3D positions are preserved in component placement

## Support and Contributions

### Report Issues
- GitHub Issues: https://github.com/Blackmvmba88/circuit/issues
- Include your `.circuit.json` file and error messages

### Contribute Improvements
- Add support for more component packages
- Improve footprint mapping
- Add more export formats
- Enhance BOM grouping logic

See `CONTRIBUTING.md` for contribution guidelines.

---

**Last Updated**: 2025-11-24
**Adapter Version**: 1.0
**Compatible with**: Altium Designer 20.x and later
