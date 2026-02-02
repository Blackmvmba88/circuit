#!/usr/bin/env python3
"""
Altium Designer Export Adapter for .circuit.json format

This script converts the open .circuit.json format to Altium Designer compatible formats:
- Component library CSV (for import into Altium)
- Netlist in Protel format (for PCB import)
- Bill of Materials (BOM) CSV
- Layout coordinates CSV (for component placement)

Usage:
    python3 circuit_to_altium.py input.circuit.json output_directory/

Author: circuit-project
License: MIT
"""

import json
import sys
import os
import tempfile
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class AltiumExporter:
    """Exports .circuit.json to Altium Designer compatible formats."""
    
    def __init__(self, circuit_data: Dict[str, Any], output_dir: str):
        self.circuit = circuit_data
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.metadata = circuit_data.get('metadata', {})
        self.components = circuit_data.get('components', [])
        self.nets = circuit_data.get('nets', [])
        self.board = circuit_data.get('board', {})
    
    def _atomic_write(self, file_path: Path, content: str):
        """
        Perform atomic write operation for text files.
        
        Writes to a temporary file first, then renames to target.
        This ensures the target file is never in a partially written state.
        """
        # Create temporary file in same directory for atomic rename
        temp_fd, temp_path = tempfile.mkstemp(
            dir=file_path.parent,
            prefix=f".{file_path.name}.",
            suffix=".tmp"
        )
        
        temp_file = Path(temp_path)
        
        try:
            # Write to temporary file
            with os.fdopen(temp_fd, 'w', encoding='utf-8', newline='') as f:
                f.write(content)
                # Ensure data is written to disk
                f.flush()
                os.fsync(f.fileno())
            
            # Atomic rename (POSIX) or replace (Windows)
            if os.name == 'nt' and file_path.exists():
                temp_file.replace(file_path)
            else:
                temp_file.rename(file_path)
            
        except Exception as e:
            # Clean up temp file on error
            try:
                temp_file.unlink(missing_ok=True)
            except:
                pass
            raise RuntimeError(f"Failed to write {file_path}: {e}")
        
    def export_all(self):
        """Export all Altium-compatible files."""
        print(f"Exporting circuit '{self.metadata.get('name', 'unnamed')}' to Altium format...")
        
        self.export_component_library()
        self.export_netlist()
        self.export_bom()
        self.export_pcb_layout()
        self.export_design_rules()
        self.create_import_guide()
        
        print(f"\n✅ Export complete! Files saved to: {self.output_dir}")
        print("\n📖 See 'ALTIUM_IMPORT_GUIDE.txt' for instructions on importing into Altium Designer.")
    
    def export_component_library(self):
        """Export component library as CSV for Altium import."""
        output_file = self.output_dir / "component_library.csv"
        
        # Build content
        lines = []
        # Altium library CSV format
        # Format: Designator, Description, Footprint, Value, Manufacturer, Part Number, Quantity
        lines.append("Designator,Description,Footprint,Value,Manufacturer,PartNumber,Type,Package\n")
        
        for comp in self.components:
            designator = comp.get('id', '')
            comp_type = comp.get('type', '')
            package = comp.get('package', 'UNKNOWN')
            description = comp.get('description', f'{comp_type.upper()}')
            params = comp.get('params', {})
            
            # Determine value based on component type
            value = self._get_component_value(comp_type, params)
            
            # Get manufacturer info if available
            manufacturer = params.get('manufacturer', '')
            part_number = params.get('part_number', '')
            
            # Map package to Altium footprint
            footprint = self._map_package_to_footprint(package, comp_type)
            
            lines.append(f'"{designator}","{description}","{footprint}","{value}","{manufacturer}","{part_number}","{comp_type}","{package}"\n')
        
        # Write atomically
        self._atomic_write(output_file, ''.join(lines))
        
        print(f"  ✓ Component library: {output_file}")
    
    def export_netlist(self):
        """Export netlist in Protel format (Altium's native format)."""
        output_file = self.output_dir / "netlist.net"
        
        lines = []
        # Protel netlist header
        lines.append("[\n")
        lines.append(f"  Circuit exported from {self.metadata.get('name', 'circuit')}\n")
        lines.append(f"  Generated: {datetime.now().isoformat()}\n")
        lines.append("  Format: Protel Netlist\n")
        lines.append("]\n\n")
        
        # Write components section
        lines.append("(\n")
        for comp in self.components:
            designator = comp.get('id', '')
            comp_type = comp.get('type', 'COMPONENT')
            package = comp.get('package', 'UNKNOWN')
            footprint = self._map_package_to_footprint(package, comp_type)
            
            lines.append(f" ( {designator} {footprint}\n")
            
            # Write pins for this component
            pins = comp.get('pins', {})
            for pin_name, pin_data in pins.items():
                net = pin_data.get('net', f'N{designator}_{pin_name}')
                # Sanitize net name to ensure valid identifiers
                net = net.replace(' ', '_').replace('-', '_').replace('+', 'P')
                lines.append(f"  {pin_name} {net}\n")
            
            lines.append(" )\n")
        
        lines.append(")\n")
        
        # Write atomically
        self._atomic_write(output_file, ''.join(lines))
        
        print(f"  ✓ Netlist (Protel format): {output_file}")
    
    def export_bom(self):
        """Export Bill of Materials as CSV."""
        output_file = self.output_dir / "bom.csv"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # BOM header compatible with Altium
            f.write("Item,Quantity,Designator,Description,Footprint,Value,Manufacturer,Part Number,Type\n")
            
            # Group components by value for BOM
            bom_groups = {}
            for comp in self.components:
                comp_type = comp.get('type', '')
                params = comp.get('params', {})
                value = self._get_component_value(comp_type, params)
                package = comp.get('package', 'UNKNOWN')
                
                key = (comp_type, value, package)
                if key not in bom_groups:
                    bom_groups[key] = {
                        'designators': [],
                        'description': comp.get('description', ''),
                        'params': params,
                        'package': package,
                        'type': comp_type
                    }
                bom_groups[key]['designators'].append(comp.get('id', ''))
            
            # Write BOM entries
            item_num = 1
            for (comp_type, value, package), data in bom_groups.items():
                quantity = len(data['designators'])
                designators = ', '.join(data['designators'])
                description = data['description']
                footprint = self._map_package_to_footprint(package, comp_type)
                manufacturer = data['params'].get('manufacturer', '')
                part_number = data['params'].get('part_number', '')
                
                f.write(f'{item_num},{quantity},"{designators}","{description}","{footprint}","{value}","{manufacturer}","{part_number}","{comp_type}"\n')
                item_num += 1
        
        print(f"  ✓ Bill of Materials: {output_file}")
    
    def export_pcb_layout(self):
        """Export PCB layout coordinates for component placement in Altium."""
        output_file = self.output_dir / "component_placement.csv"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Placement file format for Altium
            f.write("Designator,Footprint,Mid X,Mid Y,Rotation,Layer,Comment\n")
            
            for comp in self.components:
                designator = comp.get('id', '')
                package = comp.get('package', 'UNKNOWN')
                comp_type = comp.get('type', '')
                footprint = self._map_package_to_footprint(package, comp_type)
                
                # Get position from model_3d or pins
                position = self._get_component_position(comp)
                x = position.get('x', 0)
                y = position.get('y', 0)
                
                # Get rotation from model_3d if available
                rotation = 0
                if 'model_3d' in comp:
                    rot_data = comp['model_3d'].get('rotation', {})
                    rotation = rot_data.get('z', 0)  # Use Z-axis rotation for PCB
                
                # Determine layer (Top or Bottom)
                layer = "Top"
                
                # Description/comment
                comment = comp.get('description', comp_type)
                
                f.write(f'"{designator}","{footprint}",{x},{y},{rotation},"{layer}","{comment}"\n')
        
        print(f"  ✓ Component placement: {output_file}")
        
        # Also export board dimensions
        self._export_board_outline()
    
    def _export_board_outline(self):
        """Export PCB board outline dimensions."""
        output_file = self.output_dir / "board_outline.txt"
        
        dimensions = self.board.get('dimensions', {})
        width = dimensions.get('width', 100)
        height = dimensions.get('height', 100)
        thickness = dimensions.get('thickness', 1.6)
        layers = self.board.get('layers', 2)
        material = self.board.get('material', 'FR4')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("PCB Board Specifications for Altium Designer\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Width:     {width} mm\n")
            f.write(f"Height:    {height} mm\n")
            f.write(f"Thickness: {thickness} mm\n")
            f.write(f"Layers:    {layers}\n")
            f.write(f"Material:  {material}\n\n")
            f.write("Board Outline Coordinates (mm):\n")
            f.write(f"  Bottom-Left:  (0, 0)\n")
            f.write(f"  Bottom-Right: ({width}, 0)\n")
            f.write(f"  Top-Right:    ({width}, {height})\n")
            f.write(f"  Top-Left:     (0, {height})\n")
        
        print(f"  ✓ Board outline: {output_file}")
    
    def export_design_rules(self):
        """Export design rules as Altium-compatible text."""
        output_file = self.output_dir / "design_rules.txt"
        
        design_rules = self.circuit.get('design_rules', {})
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("Design Rules for Altium Designer\n")
            f.write("=" * 50 + "\n\n")
            
            # EMI compliance rules
            if 'emi_compliance' in design_rules:
                emi = design_rules['emi_compliance']
                f.write("EMI/EMC Compliance:\n")
                f.write(f"  Standard: {emi.get('standard', 'N/A')}\n")
                f.write(f"  Decoupling Strategy: {emi.get('decoupling_strategy', 'N/A')}\n")
                f.write(f"  Ground Plane: {emi.get('ground_plane', 'N/A')}\n")
                f.write(f"  Trace Spacing: {emi.get('trace_spacing_mm', 0.2)} mm\n")
                f.write(f"  Power Trace Width: {emi.get('power_trace_width_mm', 0.5)} mm\n\n")
            
            # Thermal rules
            if 'thermal' in design_rules:
                thermal = design_rules['thermal']
                f.write("Thermal Management:\n")
                f.write(f"  Max Ambient Temperature: {thermal.get('max_ambient_temp_c', 'N/A')} °C\n")
                f.write(f"  Max Junction Temperature: {thermal.get('max_junction_temp_c', 'N/A')} °C\n\n")
            
            # Suggested Altium Design Rules
            f.write("Suggested Altium Design Rules:\n")
            f.write("--------------------------------\n")
            f.write("1. Clearance Constraint:\n")
            f.write(f"   - Minimum clearance: {design_rules.get('emi_compliance', {}).get('trace_spacing_mm', 0.2)} mm\n\n")
            f.write("2. Width Constraint:\n")
            f.write(f"   - Power nets: Min {design_rules.get('emi_compliance', {}).get('power_trace_width_mm', 0.5)} mm\n")
            f.write("   - Signal nets: Min 0.2 mm\n\n")
            f.write("3. Via Style:\n")
            f.write("   - Drill diameter: 0.3 mm\n")
            f.write("   - Pad diameter: 0.6 mm\n\n")
        
        print(f"  ✓ Design rules: {output_file}")
    
    def create_import_guide(self):
        """Create a guide for importing files into Altium Designer."""
        output_file = self.output_dir / "ALTIUM_IMPORT_GUIDE.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("ALTIUM DESIGNER IMPORT GUIDE\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Circuit: {self.metadata.get('name', 'unnamed')}\n")
            f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Version: {self.metadata.get('version', 'N/A')}\n")
            f.write("\n")
            
            f.write("OVERVIEW\n")
            f.write("-" * 70 + "\n")
            f.write("This export contains the following files for importing into Altium:\n\n")
            f.write("  1. component_library.csv     - Component library definitions\n")
            f.write("  2. netlist.net               - Circuit connectivity (Protel format)\n")
            f.write("  3. bom.csv                   - Bill of Materials\n")
            f.write("  4. component_placement.csv   - PCB component placement coordinates\n")
            f.write("  5. board_outline.txt         - PCB dimensions and specifications\n")
            f.write("  6. design_rules.txt          - Recommended design rules\n\n")
            
            f.write("IMPORT INSTRUCTIONS\n")
            f.write("-" * 70 + "\n\n")
            
            f.write("Step 1: Create New PCB Project\n")
            f.write("  1. Open Altium Designer\n")
            f.write("  2. File → New → Project → PCB Project\n")
            f.write(f"  3. Name it: {self.metadata.get('name', 'MyCircuit')}\n\n")
            
            f.write("Step 2: Import Component Library\n")
            f.write("  1. Create a new Integrated Library (File → New → Library → Integrated Library)\n")
            f.write("  2. Add a Schematic Library to it\n")
            f.write("  3. Tools → Import → CSV\n")
            f.write("  4. Select: component_library.csv\n")
            f.write("  5. Map CSV columns to library fields\n")
            f.write("  6. Compile the library\n\n")
            
            f.write("Step 3: Create Schematic\n")
            f.write("  1. Add new schematic to project (File → New → Schematic)\n")
            f.write("  2. Place components from your imported library\n")
            f.write("  3. Or import the netlist:\n")
            f.write("     - Design → Import Changes from → netlist.net\n")
            f.write("     - Select 'Protel' as the netlist format\n\n")
            
            f.write("Step 4: Create PCB\n")
            f.write("  1. Add new PCB to project (File → New → PCB)\n")
            f.write("  2. Design → Board Shape → Define from selected objects\n")
            f.write(f"  3. Create rectangular board: {self.board.get('dimensions', {}).get('width', 100)} x {self.board.get('dimensions', {}).get('height', 100)} mm\n")
            f.write(f"  4. Set board thickness: {self.board.get('dimensions', {}).get('thickness', 1.6)} mm\n")
            f.write(f"  5. Configure layer stack: {self.board.get('layers', 2)} layers\n\n")
            
            f.write("Step 5: Import Component Placement\n")
            f.write("  1. In PCB editor: File → Import → Component Positions\n")
            f.write("  2. Select: component_placement.csv\n")
            f.write("  3. Set units to millimeters\n")
            f.write("  4. Verify component positions\n\n")
            
            f.write("Step 6: Update PCB from Schematic\n")
            f.write("  1. Design → Update PCB Document\n")
            f.write("  2. Review and execute changes\n")
            f.write("  3. Components will be placed according to the coordinates\n\n")
            
            f.write("Step 7: Apply Design Rules\n")
            f.write("  1. Design → Rules (in PCB editor)\n")
            f.write("  2. Refer to design_rules.txt for recommended settings\n")
            f.write("  3. Add clearance, width, and routing constraints\n")
            f.write("  4. Enable DRC (Design Rule Check)\n\n")
            
            f.write("Step 8: Route the PCB\n")
            f.write("  1. Auto-route or manually route traces\n")
            f.write("  2. Create ground plane (Place → Polygon Pour)\n")
            f.write("  3. Connect to GND net\n")
            f.write("  4. Run DRC to verify\n\n")
            
            f.write("Step 9: Generate Production Files\n")
            f.write("  1. File → Fabrication Outputs → Gerber Files\n")
            f.write("  2. File → Fabrication Outputs → NC Drill Files\n")
            f.write("  3. File → Assembly Outputs → Pick and Place Files\n")
            f.write("  4. Use bom.csv for component ordering\n\n")
            
            f.write("NOTES\n")
            f.write("-" * 70 + "\n")
            f.write("• Make sure to verify all component footprints match your parts\n")
            f.write("• Review the netlist carefully before routing\n")
            f.write("• Apply EMI/EMC design rules from design_rules.txt\n")
            f.write("• Double-check component placement before fabrication\n")
            f.write("• Run Design Rule Check (DRC) frequently\n\n")
            
            f.write("SUPPORT\n")
            f.write("-" * 70 + "\n")
            f.write("For issues or questions:\n")
            f.write("• GitHub: https://github.com/Blackmvmba88/circuit\n")
            f.write("• Documentation: docs/SYSTEM_OVERVIEW.md\n\n")
            
            f.write("=" * 70 + "\n")
        
        print(f"  ✓ Import guide: {output_file}")
    
    def _get_component_value(self, comp_type: str, params: Dict) -> str:
        """Extract component value based on type."""
        if comp_type == 'resistor':
            resistance = params.get('resistance_ohm', 0)
            return self._format_resistance(resistance)
        elif comp_type == 'capacitor':
            capacitance = params.get('capacitance_f', 0)
            return self._format_capacitance(capacitance)
        elif comp_type == 'led':
            return params.get('color', 'LED')
        elif comp_type == 'ic':
            return params.get('part_number', 'IC')
        elif comp_type == 'connector':
            num_pins = params.get('num_pins', 0)
            return f'{num_pins}P' if num_pins else 'CONN'
        else:
            return comp_type.upper()
    
    def _format_resistance(self, ohms: float) -> str:
        """Format resistance value with appropriate suffix."""
        if ohms >= 1e6:
            value = ohms / 1e6
            return f'{value:g}M'
        elif ohms >= 1e3:
            value = ohms / 1e3
            return f'{value:g}K'
        else:
            return f'{ohms:g}R'
    
    def _format_capacitance(self, farads: float) -> str:
        """Format capacitance value with appropriate suffix."""
        if farads >= 1e-6:
            value = farads * 1e6
            return f'{value:g}uF'
        elif farads >= 1e-9:
            value = farads * 1e9
            return f'{value:g}nF'
        elif farads >= 1e-12:
            value = farads * 1e12
            return f'{value:g}pF'
        else:
            return f'{farads:.2e}F'
    
    def _map_package_to_footprint(self, package: str, comp_type: str) -> str:
        """Map component package to Altium footprint name."""
        # Standard footprint mappings
        footprint_map = {
            '0805': 'RES-0805',  # or CAP-0805 depending on type
            '0603': 'RES-0603',
            '1206': 'RES-1206',
            'SOIC8': 'SOIC-8_3.9x4.9mm_P1.27mm',
            'SOIC16': 'SOIC-16_3.9x9.9mm_P1.27mm',
            'QFN32': 'QFN-32-1EP_5x5mm_P0.5mm',
            'HEADER_2.54MM': 'PinHeader_1x',
            'UNKNOWN': 'UNKNOWN'
        }
        
        # Adjust based on component type
        if package == '0805':
            if comp_type == 'resistor':
                return 'RES-0805'
            elif comp_type == 'capacitor':
                return 'CAP-0805'
            elif comp_type == 'led':
                return 'LED-0805'
        
        return footprint_map.get(package, package)
    
    def _get_component_position(self, comp: Dict) -> Dict[str, float]:
        """Get component position from model_3d or pins."""
        # Try model_3d first
        if 'model_3d' in comp:
            return comp['model_3d'].get('position', {'x': 0, 'y': 0, 'z': 0})
        
        # Otherwise, calculate from pins
        pins = comp.get('pins', {})
        if pins:
            x_coords = [pin.get('x', 0) for pin in pins.values()]
            y_coords = [pin.get('y', 0) for pin in pins.values()]
            
            if x_coords and y_coords:
                return {
                    'x': sum(x_coords) / len(x_coords),
                    'y': sum(y_coords) / len(y_coords),
                    'z': 0
                }
        
        return {'x': 0, 'y': 0, 'z': 0}


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python3 circuit_to_altium.py <input.circuit.json> [output_directory]")
        print("\nExample:")
        print("  python3 circuit_to_altium.py examples/simple_circuit.circuit.json altium_export/")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "altium_export"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: Input file '{input_file}' not found!")
        sys.exit(1)
    
    # Load circuit data
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            circuit_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in '{input_file}': {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        sys.exit(1)
    
    # Export to Altium format
    try:
        exporter = AltiumExporter(circuit_data, output_dir)
        exporter.export_all()
        print("\n✅ Success! Import the files into Altium Designer following the guide.")
    except Exception as e:
        print(f"\n❌ Export failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
