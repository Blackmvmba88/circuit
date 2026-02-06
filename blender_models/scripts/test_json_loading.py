#!/usr/bin/env python3
"""
Test script to verify .circuit.json files can be loaded and parsed correctly.
This tests the JSON parsing logic without requiring Blender.
"""

import json
import sys
import os

def test_json_loading(json_file_path):
    """Test loading and parsing a circuit JSON file."""
    print(f"\n{'='*70}")
    print(f"Testing JSON loading: {json_file_path}")
    print(f"{'='*70}\n")
    
    # Check if file exists
    if not os.path.exists(json_file_path):
        print(f"❌ Error: File '{json_file_path}' not found.")
        return False
    
    # Load the JSON file
    try:
        with open(json_file_path, 'r') as f:
            circuit_data = json.load(f)
        print("✅ JSON file loaded successfully")
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in '{json_file_path}': {e}")
        return False
    
    # Extract metadata
    metadata = circuit_data.get('metadata', {})
    circuit_name = metadata.get('name', 'Unknown Circuit')
    description = metadata.get('description', 'No description')
    
    print(f"\n📋 Circuit: {circuit_name}")
    print(f"   {description}")
    
    # Check board
    board = circuit_data.get('board', {})
    if board:
        dimensions = board.get('dimensions', {})
        width = dimensions.get('width', 50)
        height = dimensions.get('height', 50)
        thickness = dimensions.get('thickness', 1.6)
        print(f"\n🔨 PCB: {width}x{height}mm, {thickness}mm thick")
    else:
        print(f"\n⚠️  No board definition found, will use defaults")
    
    # Check components
    components = circuit_data.get('components', [])
    print(f"\n🔧 Found {len(components)} components:")
    
    supported_types = ['resistor', 'capacitor', 'ic', 'led', 'connector']
    virtual_types = ['power_supply', 'ground']
    
    for component in components:
        comp_id = component.get('id', 'Unknown')
        comp_type = component.get('type', '').lower()
        model_3d = component.get('model_3d', {})
        
        status = ""
        if comp_type in virtual_types:
            status = "ℹ️  (virtual component, no 3D model)"
        elif comp_type in supported_types:
            if model_3d:
                status = "✅ (has 3D position)"
            else:
                status = "📍 (will auto-layout)"
        else:
            status = "⚠️  (unsupported type)"
        
        print(f"   {comp_id} ({comp_type}): {status}")
    
    # Check for 3D generation config
    blender_gen = circuit_data.get('blender_generation', {})
    if blender_gen:
        print(f"\n📸 Blender generation config found:")
        render_opts = blender_gen.get('render_options', {})
        if render_opts:
            print(f"   Resolution: {render_opts.get('resolution', 'default')}")
            print(f"   Camera position: {render_opts.get('camera_position', 'default')}")
    
    print("\n" + "="*70)
    print(f"✅ Circuit '{circuit_name}' is ready for 3D generation!")
    print("\nTo generate in Blender, run:")
    print(f"   blender --python blender_models/scripts/component_generator.py -- {json_file_path}")
    print("="*70 + "\n")
    
    return True


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python test_json_loading.py <circuit.json>")
        print("\nExample:")
        print("  python test_json_loading.py examples/simple_circuit.circuit.json")
        sys.exit(1)
    
    json_file = sys.argv[1]
    success = test_json_loading(json_file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
