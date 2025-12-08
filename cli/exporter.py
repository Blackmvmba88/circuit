"""
Export circuit to different formats.
"""

import json
import sys
from pathlib import Path
from typing import Optional


def export_circuit(file_path: str, format_type: str, output_dir: str) -> None:
    """
    Export circuit to different formats.
    
    Args:
        file_path: Path to the circuit file
        format_type: Export format (altium, kicad, eagle, spice, netlist, bom)
        output_dir: Output directory
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        circuit_data = json.load(f)
    
    if format_type == "altium":
        export_altium(circuit_data, file_path, output_dir)
    elif format_type == "kicad":
        raise NotImplementedError("KiCad export")
    elif format_type == "eagle":
        raise NotImplementedError("Eagle export")
    elif format_type == "spice":
        raise NotImplementedError("SPICE export")
    elif format_type == "netlist":
        export_netlist(circuit_data, output_dir)
    elif format_type == "bom":
        export_bom(circuit_data, output_dir)
    else:
        raise ValueError(f"Unknown export format: {format_type}")


def export_altium(circuit_data: dict, file_path: str, output_dir: str) -> None:
    """Export to Altium Designer format using the existing adapter."""
    # Import and use the existing Altium adapter
    adapters_path = Path(__file__).parent.parent / "adapters"
    
    # Temporarily add to path for import
    path_str = str(adapters_path)
    path_added = False
    
    try:
        if path_str not in sys.path:
            sys.path.insert(0, path_str)
            path_added = True
        
        from circuit_to_altium import AltiumExporter
        
        exporter = AltiumExporter(circuit_data, output_dir)
        exporter.export_all()
    except ImportError as e:
        raise ImportError(f"Could not import Altium adapter: {e}")
    finally:
        # Clean up path modification
        if path_added:
            try:
                sys.path.remove(path_str)
            except ValueError:
                pass  # Already removed or never added


def export_netlist(circuit_data: dict, output_dir: str) -> None:
    """Export simple netlist."""
    output_path = Path(output_dir) / "netlist.txt"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Circuit Netlist\n")
        f.write(f"# Circuit: {circuit_data.get('metadata', {}).get('name', 'unnamed')}\n")
        f.write("\n")
        
        # Components
        f.write("# Components\n")
        for comp in circuit_data.get('components', []):
            comp_id = comp.get('id', 'unknown')
            comp_type = comp.get('type', 'unknown')
            value = comp.get('value', '')
            f.write(f"{comp_id}\t{comp_type}\t{value}\n")
        
        f.write("\n")
        
        # Nets
        f.write("# Nets\n")
        if 'nets' in circuit_data:
            for net in circuit_data['nets']:
                net_id = net.get('id', net.get('name', 'unnamed'))
                connections = net.get('connections', [])
                conn_str = ", ".join(f"{c['component']}.{c['pin']}" for c in connections)
                f.write(f"{net_id}: {conn_str}\n")
        elif 'connections' in circuit_data:
            for conn in circuit_data['connections']:
                from_pin = conn.get('from', '')
                to_pin = conn.get('to', '')
                f.write(f"{from_pin} -> {to_pin}\n")
    
    print(f"  ✓ Netlist: {output_path}")


def export_bom(circuit_data: dict, output_dir: str) -> None:
    """Export Bill of Materials as CSV."""
    from collections import Counter
    
    output_path = Path(output_dir) / "bom.csv"
    
    # Group components
    bom_items = {}
    for comp in circuit_data.get('components', []):
        comp_type = comp.get('type', 'unknown')
        value = comp.get('value', '')
        package = comp.get('package', '')
        
        key = (comp_type, value, package)
        if key not in bom_items:
            bom_items[key] = {
                'designators': [],
                'type': comp_type,
                'value': value,
                'package': package,
                'description': comp.get('description', ''),
                'params': comp.get('params', {})
            }
        bom_items[key]['designators'].append(comp.get('id', 'unknown'))
    
    # Write BOM
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("Item,Quantity,Designators,Type,Value,Package,Description,Manufacturer,Part Number\n")
        
        item_num = 1
        for key, data in sorted(bom_items.items()):
            quantity = len(data['designators'])
            designators = ', '.join(sorted(data['designators']))
            comp_type = data['type']
            value = data['value']
            package = data['package']
            description = data['description']
            manufacturer = data['params'].get('manufacturer', '')
            part_number = data['params'].get('part_number', '')
            
            f.write(f'{item_num},{quantity},"{designators}","{comp_type}","{value}","{package}","{description}","{manufacturer}","{part_number}"\n')
            item_num += 1
    
    print(f"  ✓ Bill of Materials: {output_path}")
