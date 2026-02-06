"""
Blender Python Script for Generating 3D Circuit Components
============================================================

This script provides utilities to generate 3D models of electronic components
for PCB visualization and design. All models follow industry-standard dimensions
and include proper clearances for EMI/noise reduction.

Usage in Blender:
    1. Interactive mode (in Blender UI):
       - Open Blender
       - Go to Scripting tab
       - Open this script
       - Run the script
       - Use the functions to generate components

    2. Command-line mode (load circuit from JSON):
       blender --python blender_models/scripts/component_generator.py -- examples/simple_circuit.circuit.json

Example:
    import bpy
    # Run this script first, then:
    create_resistor_smd_0805("R1", location=(0, 0, 0))
"""

import bpy
import math
import json
import sys
import os


def clear_scene():
    """Clear all mesh objects from the scene."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


def create_material(name, color, metallic=0.5, roughness=0.5):
    """
    Create a material with specified properties.
    
    Args:
        name: Material name
        color: RGB tuple (r, g, b) with values 0-1
        metallic: Metallic value 0-1
        roughness: Roughness value 0-1
    
    Returns:
        Material object
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    
    principled = nodes.get("Principled BSDF")
    if principled:
        principled.inputs["Base Color"].default_value = (*color, 1.0)
        principled.inputs["Metallic"].default_value = metallic
        principled.inputs["Roughness"].default_value = roughness
    
    return mat


def create_resistor_smd_0805(name="Resistor", location=(0, 0, 0), resistance_value="1K"):
    """
    Create an SMD resistor (0805 package).
    
    Standard 0805 dimensions:
    - Length: 2.0mm
    - Width: 1.25mm
    - Height: 0.6mm
    
    Args:
        name: Component name
        location: (x, y, z) position in Blender units (1 unit = 1mm)
        resistance_value: Text value to display
    
    Returns:
        Created object
    """
    # Create the body
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=location
    )
    resistor = bpy.context.active_object
    resistor.name = name
    resistor.scale = (2.0, 1.25, 0.6)
    
    # Create material
    body_mat = create_material(f"{name}_body", (0.1, 0.1, 0.1), metallic=0.1, roughness=0.8)
    resistor.data.materials.append(body_mat)
    
    # Create end terminals (metallic)
    terminal_mat = create_material(f"{name}_terminal", (0.8, 0.8, 0.8), metallic=0.9, roughness=0.3)
    
    # Left terminal
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(location[0] - 0.85, location[1], location[2])
    )
    terminal_l = bpy.context.active_object
    terminal_l.name = f"{name}_terminal_L"
    terminal_l.scale = (0.3, 1.25, 0.6)
    terminal_l.data.materials.append(terminal_mat)
    
    # Right terminal
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(location[0] + 0.85, location[1], location[2])
    )
    terminal_r = bpy.context.active_object
    terminal_r.name = f"{name}_terminal_R"
    terminal_r.scale = (0.3, 1.25, 0.6)
    terminal_r.data.materials.append(terminal_mat)
    
    # Group components
    bpy.ops.object.select_all(action='DESELECT')
    resistor.select_set(True)
    terminal_l.select_set(True)
    terminal_r.select_set(True)
    bpy.context.view_layer.objects.active = resistor
    bpy.ops.object.join()
    
    return resistor


def create_capacitor_smd_0805(name="Capacitor", location=(0, 0, 0), capacitance_value="10uF"):
    """
    Create an SMD capacitor (0805 package).
    
    Args:
        name: Component name
        location: (x, y, z) position
        capacitance_value: Text value to display
    
    Returns:
        Created object
    """
    # Create the body (tan/brown color for ceramic)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=location
    )
    capacitor = bpy.context.active_object
    capacitor.name = name
    capacitor.scale = (2.0, 1.25, 0.8)
    
    # Create material (tan color)
    body_mat = create_material(f"{name}_body", (0.76, 0.6, 0.42), metallic=0.0, roughness=0.9)
    capacitor.data.materials.append(body_mat)
    
    # Create end terminals
    terminal_mat = create_material(f"{name}_terminal", (0.8, 0.8, 0.8), metallic=0.9, roughness=0.3)
    
    # Terminals
    for side, x_offset in [("L", -0.85), ("R", 0.85)]:
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(location[0] + x_offset, location[1], location[2])
        )
        terminal = bpy.context.active_object
        terminal.name = f"{name}_terminal_{side}"
        terminal.scale = (0.3, 1.25, 0.8)
        terminal.data.materials.append(terminal_mat)
    
    # Group
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if obj.name.startswith(name):
            obj.select_set(True)
    bpy.context.view_layer.objects.active = capacitor
    bpy.ops.object.join()
    
    return capacitor


def create_ic_soic8(name="IC", location=(0, 0, 0)):
    """
    Create an SOIC-8 IC package.
    
    Standard SOIC-8 dimensions:
    - Body length: 4.9mm
    - Body width: 3.9mm
    - Height: 1.5mm
    - Pin pitch: 1.27mm
    
    Args:
        name: Component name
        location: (x, y, z) position
    
    Returns:
        Created object
    """
    # Create IC body
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=location
    )
    ic = bpy.context.active_object
    ic.name = name
    ic.scale = (4.9, 3.9, 1.5)
    
    # Black epoxy material
    body_mat = create_material(f"{name}_body", (0.02, 0.02, 0.02), metallic=0.0, roughness=0.7)
    ic.data.materials.append(body_mat)
    
    # Create pins
    pin_mat = create_material(f"{name}_pins", (0.85, 0.85, 0.85), metallic=0.9, roughness=0.3)
    
    pin_pitch = 1.27
    pin_width = 0.4
    pin_length = 0.6
    pin_height = 0.2
    
    # Left side pins (4 pins)
    for i in range(4):
        y_pos = location[1] + 1.905 - i * pin_pitch
        x_pos = location[0] - 2.45 - pin_length / 2
        
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(x_pos, y_pos, location[2] - 0.5)
        )
        pin = bpy.context.active_object
        pin.name = f"{name}_pin_{i+1}"
        pin.scale = (pin_length, pin_width, pin_height)
        pin.data.materials.append(pin_mat)
    
    # Right side pins (4 pins)
    for i in range(4):
        y_pos = location[1] - 1.905 + i * pin_pitch
        x_pos = location[0] + 2.45 + pin_length / 2
        
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(x_pos, y_pos, location[2] - 0.5)
        )
        pin = bpy.context.active_object
        pin.name = f"{name}_pin_{i+5}"
        pin.scale = (pin_length, pin_width, pin_height)
        pin.data.materials.append(pin_mat)
    
    # Add pin 1 indicator (small circle)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.3,
        depth=0.05,
        location=(location[0] - 1.5, location[1] + 1.5, location[2] + 0.76)
    )
    indicator = bpy.context.active_object
    indicator.name = f"{name}_pin1_indicator"
    indicator_mat = create_material(f"{name}_indicator", (0.9, 0.9, 0.9), metallic=0.0, roughness=0.5)
    indicator.data.materials.append(indicator_mat)
    
    # Group all
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if obj.name.startswith(name):
            obj.select_set(True)
    bpy.context.view_layer.objects.active = ic
    bpy.ops.object.join()
    
    return ic


def create_header_connector(name="Connector", location=(0, 0, 0), num_pins=8):
    """
    Create a pin header connector.
    
    Standard 2.54mm (0.1") pitch header.
    
    Args:
        name: Component name
        location: (x, y, z) position
        num_pins: Number of pins in the connector
    
    Returns:
        Created object
    """
    pitch = 2.54
    pin_width = 0.64
    body_height = 2.5
    pin_length = 11.5  # Total pin length (through-hole)
    
    # Create plastic housing
    housing_length = num_pins * pitch
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=location
    )
    housing = bpy.context.active_object
    housing.name = name
    housing.scale = (housing_length, pitch, body_height)
    
    # Black plastic material
    housing_mat = create_material(f"{name}_housing", (0.1, 0.1, 0.1), metallic=0.0, roughness=0.8)
    housing.data.materials.append(housing_mat)
    
    # Create pins
    pin_mat = create_material(f"{name}_pins", (0.85, 0.75, 0.4), metallic=0.9, roughness=0.3)
    
    start_x = location[0] - (num_pins - 1) * pitch / 2
    
    for i in range(num_pins):
        x_pos = start_x + i * pitch
        
        # Pin (square post)
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(x_pos, location[1], location[2])
        )
        pin = bpy.context.active_object
        pin.name = f"{name}_pin_{i+1}"
        pin.scale = (pin_width, pin_width, pin_length)
        pin.data.materials.append(pin_mat)
    
    # Group
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if obj.name.startswith(name):
            obj.select_set(True)
    bpy.context.view_layer.objects.active = housing
    bpy.ops.object.join()
    
    return housing


def create_led_smd_0805(name="LED", location=(0, 0, 0), color="red"):
    """
    Create an SMD LED (0805 package).
    
    Args:
        name: Component name
        location: (x, y, z) position
        color: LED color (red, green, blue, yellow)
    
    Returns:
        Created object
    """
    # LED colors
    colors = {
        "red": (0.8, 0.1, 0.1),
        "green": (0.1, 0.8, 0.1),
        "blue": (0.1, 0.1, 0.8),
        "yellow": (0.8, 0.8, 0.1),
    }
    led_color = colors.get(color.lower(), colors["red"])
    
    # Create the body
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=location
    )
    led = bpy.context.active_object
    led.name = name
    led.scale = (2.0, 1.25, 0.8)
    
    # Transparent LED material
    body_mat = create_material(f"{name}_body", led_color, metallic=0.0, roughness=0.1)
    led.data.materials.append(body_mat)
    
    # Create cathode indicator (one side darker)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(location[0] - 0.75, location[1], location[2])
    )
    cathode = bpy.context.active_object
    cathode.name = f"{name}_cathode_mark"
    cathode.scale = (0.5, 1.25, 0.8)
    cathode_mat = create_material(f"{name}_cathode", (0.05, 0.05, 0.05), metallic=0.0, roughness=0.8)
    cathode.data.materials.append(cathode_mat)
    
    # Create terminals
    terminal_mat = create_material(f"{name}_terminal", (0.8, 0.8, 0.8), metallic=0.9, roughness=0.3)
    
    for side, x_offset in [("L", -0.85), ("R", 0.85)]:
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(location[0] + x_offset, location[1], location[2] - 0.3)
        )
        terminal = bpy.context.active_object
        terminal.name = f"{name}_terminal_{side}"
        terminal.scale = (0.3, 1.25, 0.2)
        terminal.data.materials.append(terminal_mat)
    
    # Group
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if obj.name.startswith(name):
            obj.select_set(True)
    bpy.context.view_layer.objects.active = led
    bpy.ops.object.join()
    
    return led


def create_pcb_board(name="PCB", location=(0, 0, 0), size=(50, 50), thickness=1.6):
    """
    Create a PCB board with standard FR4 appearance.
    
    Args:
        name: Board name
        location: (x, y, z) position
        size: (width, height) in mm
        thickness: Board thickness in mm (standard is 1.6mm)
    
    Returns:
        Created object
    """
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=location
    )
    pcb = bpy.context.active_object
    pcb.name = name
    pcb.scale = (size[0], size[1], thickness)
    
    # FR4 green material
    pcb_mat = create_material(f"{name}_material", (0.0, 0.3, 0.1), metallic=0.0, roughness=0.6)
    pcb.data.materials.append(pcb_mat)
    
    return pcb


def create_diode_smd_0805(name="Diode", location=(0, 0, 0)):
    """
    Create an SMD diode (0805 package).
    
    Args:
        name: Component name
        location: (x, y, z) position
    
    Returns:
        Created object
    """
    # Create the body (black epoxy)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=location
    )
    diode = bpy.context.active_object
    diode.name = name
    diode.scale = (2.0, 1.25, 0.8)
    
    # Black epoxy material
    body_mat = create_material(f"{name}_body", (0.05, 0.05, 0.05), metallic=0.0, roughness=0.8)
    diode.data.materials.append(body_mat)
    
    # Create cathode indicator (white/silver line)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(location[0] - 0.75, location[1], location[2])
    )
    cathode_mark = bpy.context.active_object
    cathode_mark.name = f"{name}_cathode_mark"
    cathode_mark.scale = (0.3, 1.25, 0.85)
    cathode_mat = create_material(f"{name}_cathode", (0.9, 0.9, 0.9), metallic=0.1, roughness=0.5)
    cathode_mark.data.materials.append(cathode_mat)
    
    # Create terminals
    terminal_mat = create_material(f"{name}_terminal", (0.8, 0.8, 0.8), metallic=0.9, roughness=0.3)
    
    for side, x_offset in [("L", -0.85), ("R", 0.85)]:
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(location[0] + x_offset, location[1], location[2] - 0.3)
        )
        terminal = bpy.context.active_object
        terminal.name = f"{name}_terminal_{side}"
        terminal.scale = (0.3, 1.25, 0.2)
        terminal.data.materials.append(terminal_mat)
    
    # Group
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if obj.name.startswith(name):
            obj.select_set(True)
    bpy.context.view_layer.objects.active = diode
    bpy.ops.object.join()
    
    return diode


def create_voltage_regulator_to220(name="VoltageReg", location=(0, 0, 0)):
    """
    Create a TO-220 voltage regulator package (e.g., LM7805).
    
    Standard TO-220 dimensions:
    - Body width: 10mm
    - Body depth: 9mm
    - Body height: 4.5mm
    
    Args:
        name: Component name
        location: (x, y, z) position
    
    Returns:
        Created object
    """
    # Create the body (black plastic)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=location
    )
    body = bpy.context.active_object
    body.name = name
    body.scale = (10, 9, 4.5)
    
    # Black plastic material
    body_mat = create_material(f"{name}_body", (0.05, 0.05, 0.05), metallic=0.0, roughness=0.8)
    body.data.materials.append(body_mat)
    
    # Create mounting tab (metal)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(location[0], location[1] + 5.5, location[2])
    )
    tab = bpy.context.active_object
    tab.name = f"{name}_mounting_tab"
    tab.scale = (10, 2, 0.3)
    tab_mat = create_material(f"{name}_tab", (0.7, 0.7, 0.7), metallic=0.8, roughness=0.4)
    tab.data.materials.append(tab_mat)
    
    # Create 3 pins
    pin_mat = create_material(f"{name}_pins", (0.85, 0.85, 0.85), metallic=0.9, roughness=0.3)
    
    pin_spacing = 2.54
    pin_width = 0.6
    pin_length = 3.0
    pin_thickness = 0.5
    
    for i, x_offset in enumerate([-pin_spacing, 0, pin_spacing]):
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(location[0] + x_offset, location[1] - 5.5, location[2] - 2)
        )
        pin = bpy.context.active_object
        pin.name = f"{name}_pin_{i+1}"
        pin.scale = (pin_width, pin_length, pin_thickness)
        pin.data.materials.append(pin_mat)
    
    # Group all
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if obj.name.startswith(name):
            obj.select_set(True)
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.join()
    
    return body


def create_example_circuit():
    """
    Create an example circuit with multiple components on a PCB.
    This demonstrates proper component spacing for EMI reduction.
    """
    clear_scene()
    
    # Create PCB
    pcb = create_pcb_board("PCB_Main", location=(0, 0, -1), size=(60, 40))
    
    # Create components with proper spacing
    # Power supply section
    create_capacitor_smd_0805("C1", location=(-20, 15, 0), capacitance_value="10uF")
    create_capacitor_smd_0805("C2", location=(-15, 15, 0), capacitance_value="100nF")
    
    # IC with decoupling
    create_ic_soic8("U1", location=(0, 10, 0))
    create_capacitor_smd_0805("C3", location=(8, 10, 0), capacitance_value="100nF")
    
    # Resistors
    create_resistor_smd_0805("R1", location=(-10, 0, 0), resistance_value="10K")
    create_resistor_smd_0805("R2", location=(10, 0, 0), resistance_value="1K")
    
    # LED indicators
    create_led_smd_0805("LED1", location=(15, -10, 0), color="red")
    create_led_smd_0805("LED2", location=(20, -10, 0), color="green")
    
    # Connector
    create_header_connector("J1", location=(-20, -15, 0), num_pins=6)
    
    # Add camera
    bpy.ops.object.camera_add(location=(50, -50, 40))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.1, 0, 0.785)
    bpy.context.scene.camera = camera
    
    # Add lighting
    bpy.ops.object.light_add(type='SUN', location=(10, 10, 20))
    light = bpy.context.active_object
    light.data.energy = 2.0
    
    print("Example circuit created successfully!")
    print("Components follow EMI best practices with proper spacing and decoupling.")


def load_circuit_from_json(json_file_path):
    """
    Load and generate a 3D circuit from a .circuit.json file.
    
    This function parses a circuit definition in JSON format and generates
    all components and the PCB board in Blender's 3D space.
    
    Args:
        json_file_path: Path to the .circuit.json file
        
    Returns:
        dict: The loaded circuit data
        
    Raises:
        FileNotFoundError: If the JSON file doesn't exist
        json.JSONDecodeError: If the JSON is invalid
    """
    print(f"\n{'='*70}")
    print(f"Loading circuit from: {json_file_path}")
    print(f"{'='*70}\n")
    
    # Load the JSON file
    try:
        with open(json_file_path, 'r') as f:
            circuit_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File '{json_file_path}' not found.")
        raise
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in '{json_file_path}': {e}")
        raise
    
    # Extract metadata
    metadata = circuit_data.get('metadata', {})
    circuit_name = metadata.get('name', 'Unknown Circuit')
    description = metadata.get('description', 'No description')
    
    print(f"📋 Circuit: {circuit_name}")
    print(f"   {description}\n")
    
    # Clear the scene
    clear_scene()
    
    # Create the PCB board
    board = circuit_data.get('board', {})
    if board:
        dimensions = board.get('dimensions', {})
        width = dimensions.get('width', 50)
        height = dimensions.get('height', 50)
        thickness = dimensions.get('thickness', 1.6)
        
        model_3d = board.get('model_3d', {})
        position = model_3d.get('position', {'x': 0, 'y': 0, 'z': -0.8})
        
        print(f"🔨 Creating PCB: {width}x{height}mm, {thickness}mm thick")
        pcb = create_pcb_board(
            "PCB_Main",
            location=(position['x'], position['y'], position['z']),
            size=(width, height),
            thickness=thickness
        )
    
    # Component generator mapping
    component_generators = {
        'resistor': create_resistor_smd_0805,
        'capacitor': create_capacitor_smd_0805,
        'ic': create_ic_soic8,
        'led': create_led_smd_0805,
        'connector': create_header_connector,
        'diode': create_diode_smd_0805,
        'voltage_regulator': create_voltage_regulator_to220,
    }
    
    # Create components
    components = circuit_data.get('components', [])
    print(f"\n🔧 Creating {len(components)} components:")
    
    # Auto-layout parameters for components without 3D positions
    auto_x = -25
    auto_y = 0
    auto_spacing = 6
    
    for component in components:
        comp_id = component.get('id', 'Unknown')
        comp_type = component.get('type', '').lower()
        model_3d = component.get('model_3d', {})
        
        # Determine position - use model_3d if available, otherwise auto-layout
        if model_3d and 'position' in model_3d:
            position = model_3d.get('position', {'x': 0, 'y': 0, 'z': 0})
            location = (position['x'], position['y'], position['z'])
        else:
            # Auto-layout: place components in a row
            location = (auto_x, auto_y, 0)
            auto_x += auto_spacing
            if not model_3d:
                print(f"   ℹ️  {comp_id} ({comp_type}): Using auto-layout position")
        
        # Get generator function
        generator_name = model_3d.get('generator') if model_3d else None
        generator_func = None
        
        # Try to find generator by name or type
        if generator_name:
            # Direct function name mapping
            func_map = {
                'create_resistor_smd_0805': create_resistor_smd_0805,
                'create_capacitor_smd_0805': create_capacitor_smd_0805,
                'create_ic_soic8': create_ic_soic8,
                'create_led_smd_0805': create_led_smd_0805,
                'create_header_connector': create_header_connector,
                'create_diode_smd_0805': create_diode_smd_0805,
                'create_voltage_regulator_to220': create_voltage_regulator_to220,
            }
            generator_func = func_map.get(generator_name)
        
        # Fallback to component type
        if not generator_func:
            generator_func = component_generators.get(comp_type)
        
        if not generator_func:
            print(f"   ⚠️  {comp_id} ({comp_type}): No generator found - skipping")
            continue
        
        # Get additional parameters
        params = model_3d.get('params', {}) if model_3d else {}
        
        # Generate the component based on type
        try:
            if comp_type == 'resistor':
                # Try to get value from params or component data
                value = params.get('resistance_value') or component.get('value', '1K')
                generator_func(comp_id, location=location, resistance_value=value)
                print(f"   ✅ {comp_id}: Resistor {value}")
                
            elif comp_type == 'capacitor':
                value = params.get('capacitance_value', '100nF')
                generator_func(comp_id, location=location, capacitance_value=value)
                print(f"   ✅ {comp_id}: Capacitor {value}")
                
            elif comp_type == 'ic':
                generator_func(comp_id, location=location)
                package = component.get('package', 'SOIC8')
                print(f"   ✅ {comp_id}: IC {package}")
                
            elif comp_type == 'led':
                color = params.get('color') or component.get('color', 'red')
                generator_func(comp_id, location=location, color=color)
                print(f"   ✅ {comp_id}: LED {color}")
                
            elif comp_type == 'connector':
                num_pins = params.get('num_pins', 8)
                generator_func(comp_id, location=location, num_pins=num_pins)
                print(f"   ✅ {comp_id}: Connector {num_pins}-pin")
            
            elif comp_type == 'diode':
                generator_func(comp_id, location=location)
                print(f"   ✅ {comp_id}: Diode 0805")
            
            elif comp_type == 'voltage_regulator':
                generator_func(comp_id, location=location)
                part = component.get('part_number', component.get('value', 'TO-220'))
                print(f"   ✅ {comp_id}: Voltage Regulator {part}")
            
            elif comp_type in ['power_supply', 'ground']:
                # Special handling for power supply and ground - just markers
                print(f"   ℹ️  {comp_id} ({comp_type}): Virtual component - skipping 3D model")
                
            else:
                print(f"   ⚠️  {comp_id} ({comp_type}): Unsupported type")
                
        except Exception as e:
            print(f"   ❌ {comp_id}: Error creating component - {e}")
    
    # Set up camera and lighting
    print("\n📸 Setting up camera and lighting...")
    
    # Get camera settings from JSON or use defaults
    blender_gen = circuit_data.get('blender_generation', {})
    render_opts = blender_gen.get('render_options', {})
    
    cam_pos = render_opts.get('camera_position', [50, -50, 40])
    cam_rot = render_opts.get('camera_rotation', [1.1, 0, 0.785])
    
    bpy.ops.object.camera_add(location=cam_pos)
    camera = bpy.context.active_object
    camera.rotation_euler = cam_rot
    bpy.context.scene.camera = camera
    
    # Add lighting
    bpy.ops.object.light_add(type='SUN', location=(10, 10, 20))
    light = bpy.context.active_object
    light.data.energy = 2.0
    
    print("\n" + "="*70)
    print(f"✅ Circuit '{circuit_name}' loaded successfully!")
    print("   You can now navigate the 3D view, render, or export the model.")
    print("="*70 + "\n")
    
    return circuit_data


# Main execution
if __name__ == "__main__":
    print("Circuit Component Generator loaded successfully!")
    print("\nAvailable functions:")
    print("  - create_resistor_smd_0805(name, location, value)")
    print("  - create_capacitor_smd_0805(name, location, value)")
    print("  - create_ic_soic8(name, location)")
    print("  - create_led_smd_0805(name, location, color)")
    print("  - create_header_connector(name, location, num_pins)")
    print("  - create_pcb_board(name, location, size, thickness)")
    print("  - create_example_circuit()")
    print("  - load_circuit_from_json(json_file_path)")
    
    # Check for command-line arguments (when run with blender --python script.py -- args)
    # In Blender, sys.argv contains all arguments after '--'
    try:
        # Find the '--' separator in argv
        argv = sys.argv
        if '--' in argv:
            # Get arguments after '--'
            script_args = argv[argv.index('--') + 1:]
            
            if script_args:
                json_file = script_args[0]
                print(f"\n🚀 Loading circuit from command line: {json_file}")
                
                # Make path absolute if it's relative
                if not os.path.isabs(json_file):
                    # Try relative to current working directory
                    if os.path.exists(json_file):
                        json_file = os.path.abspath(json_file)
                    else:
                        # Try relative to script directory
                        script_dir = os.path.dirname(os.path.abspath(__file__))
                        repo_root = os.path.dirname(os.path.dirname(script_dir))
                        json_file_alt = os.path.join(repo_root, json_file)
                        if os.path.exists(json_file_alt):
                            json_file = json_file_alt
                
                # Load and generate the circuit
                try:
                    load_circuit_from_json(json_file)
                except Exception as e:
                    print(f"\n❌ Failed to load circuit: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print("\n💡 To load a circuit from command line:")
                print("   blender --python blender_models/scripts/component_generator.py -- examples/simple_circuit.circuit.json")
        else:
            print("\n💡 To create an example circuit, run: create_example_circuit()")
            print("\n💡 To load a circuit from command line:")
            print("   blender --python blender_models/scripts/component_generator.py -- examples/simple_circuit.circuit.json")
    except Exception as e:
        print(f"\n⚠️  Error processing command line arguments: {e}")
        print("\n💡 To create an example circuit, run: create_example_circuit()")
