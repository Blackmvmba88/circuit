"""
Display circuit information and statistics.
"""

import json
from pathlib import Path
from typing import Dict, Any
from collections import Counter


def display_circuit_info(file_path: str, verbose: bool = False) -> None:
    """
    Display circuit information and statistics.
    
    Args:
        file_path: Path to the circuit file
        verbose: Show detailed information
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        circuit = json.load(f)
    
    metadata = circuit.get('metadata', {})
    components = circuit.get('components', [])
    nets = circuit.get('nets', [])
    connections = circuit.get('connections', [])
    board = circuit.get('board', {})
    
    # Header
    print("=" * 70)
    print(f"📋 Circuit Information: {Path(file_path).name}")
    print("=" * 70)
    print()
    
    # Metadata
    print("📌 Metadata")
    print("-" * 70)
    print(f"  Name:        {metadata.get('name', 'N/A')}")
    print(f"  Description: {metadata.get('description', 'N/A')}")
    print(f"  Author:      {metadata.get('author', 'N/A')}")
    print(f"  Version:     {metadata.get('version', 'N/A')}")
    print(f"  Created:     {metadata.get('created', 'N/A')}")
    if 'tags' in metadata:
        tags_str = ", ".join(metadata['tags'])
        print(f"  Tags:        {tags_str}")
    print()
    
    # Components summary
    print("🔌 Components")
    print("-" * 70)
    print(f"  Total Components: {len(components)}")
    
    # Count by type
    type_counts = Counter(comp.get('type', 'unknown') for comp in components)
    print(f"  By Type:")
    for comp_type, count in sorted(type_counts.items()):
        print(f"    - {comp_type}: {count}")
    
    # Count by package
    package_counts = Counter(comp.get('package', 'N/A') for comp in components)
    if verbose and any(pkg != 'N/A' for pkg in package_counts):
        print(f"  By Package:")
        for package, count in sorted(package_counts.items()):
            if package != 'N/A':
                print(f"    - {package}: {count}")
    
    print()
    
    # Connections/Nets
    print("🔗 Connectivity")
    print("-" * 70)
    if nets:
        print(f"  Total Nets:        {len(nets)}")
        total_connections = sum(len(net.get('connections', [])) for net in nets)
        print(f"  Total Connections: {total_connections}")
        
        if verbose:
            print(f"  Nets:")
            for net in nets[:10]:  # Show first 10
                net_id = net.get('id', net.get('name', 'unnamed'))
                conn_count = len(net.get('connections', []))
                print(f"    - {net_id}: {conn_count} connections")
            if len(nets) > 10:
                print(f"    ... and {len(nets) - 10} more")
    elif connections:
        print(f"  Total Connections: {len(connections)} (point-to-point)")
    else:
        print(f"  No connections defined")
    
    print()
    
    # Board info
    if board:
        print("📐 PCB Board")
        print("-" * 70)
        dimensions = board.get('dimensions', {})
        if dimensions:
            width = dimensions.get('width', 'N/A')
            height = dimensions.get('height', 'N/A')
            thickness = dimensions.get('thickness', 'N/A')
            print(f"  Dimensions: {width} x {height} mm")
            print(f"  Thickness:  {thickness} mm")
        
        layers = board.get('layers')
        if layers:
            print(f"  Layers:     {layers}")
        
        material = board.get('material')
        if material:
            print(f"  Material:   {material}")
        
        print()
    
    # Design rules
    design_rules = circuit.get('design_rules', {})
    if design_rules and verbose:
        print("📏 Design Rules")
        print("-" * 70)
        
        emi = design_rules.get('emi_compliance', {})
        if emi:
            print(f"  EMI Compliance:")
            print(f"    Standard:       {emi.get('standard', 'N/A')}")
            print(f"    Trace Spacing:  {emi.get('trace_spacing_mm', 'N/A')} mm")
            print(f"    Power Trace:    {emi.get('power_trace_width_mm', 'N/A')} mm")
        
        thermal = design_rules.get('thermal', {})
        if thermal:
            print(f"  Thermal:")
            print(f"    Max Ambient:    {thermal.get('max_ambient_temp_c', 'N/A')} °C")
            print(f"    Max Junction:   {thermal.get('max_junction_temp_c', 'N/A')} °C")
        
        print()
    
    # Properties
    properties = circuit.get('properties', {})
    if properties and verbose:
        print("⚡ Circuit Properties")
        print("-" * 70)
        for key, value in properties.items():
            print(f"  {key}: {value}")
        print()
    
    # Component details (if verbose)
    if verbose:
        print("📦 Component Details")
        print("-" * 70)
        for comp in components[:20]:  # Show first 20
            comp_id = comp.get('id', 'unknown')
            comp_type = comp.get('type', 'unknown')
            package = comp.get('package', 'N/A')
            value = comp.get('value', comp.get('params', {}).get('resistance_ohm', 
                           comp.get('params', {}).get('capacitance_f', 'N/A')))
            
            print(f"  {comp_id:8} [{comp_type:15}] {package:10} = {value}")
        
        if len(components) > 20:
            print(f"  ... and {len(components) - 20} more components")
        print()
    
    # Footer
    print("=" * 70)
    print(f"✅ Circuit file loaded successfully")
    print("=" * 70)
