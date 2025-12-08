"""
Circuit file validator using JSON schema validation.
"""

import json
from pathlib import Path
from typing import Tuple, List, Optional
import jsonschema
from jsonschema import validate, ValidationError, Draft7Validator


def load_schema() -> dict:
    """Load the circuit.json schema."""
    schema_path = Path(__file__).parent.parent / "schema" / "circuit.schema.json"
    
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def validate_circuit_file(file_path: str, strict: bool = False) -> Tuple[bool, List[str], List[str]]:
    """
    Validate a .circuit.json file.
    
    Args:
        file_path: Path to the circuit file
        strict: Enable strict validation mode
        
    Returns:
        Tuple of (is_valid, errors, warnings)
    """
    errors = []
    warnings = []
    
    # Load circuit file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            circuit_data = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON: {e}")
        return False, errors, warnings
    except Exception as e:
        errors.append(f"Error loading file: {e}")
        return False, errors, warnings
    
    # Load schema
    try:
        schema = load_schema()
    except Exception as e:
        errors.append(f"Error loading schema: {e}")
        return False, errors, warnings
    
    # Validate against schema
    try:
        validator = Draft7Validator(schema)
        schema_errors = list(validator.iter_errors(circuit_data))
        
        if schema_errors:
            for error in schema_errors:
                path = ".".join(str(p) for p in error.path) if error.path else "root"
                errors.append(f"[{path}] {error.message}")
    except Exception as e:
        errors.append(f"Schema validation error: {e}")
        return False, errors, warnings
    
    # Semantic validation
    semantic_errors, semantic_warnings = validate_semantics(circuit_data, strict)
    errors.extend(semantic_errors)
    warnings.extend(semantic_warnings)
    
    is_valid = len(errors) == 0
    return is_valid, errors, warnings


def validate_semantics(circuit_data: dict, strict: bool = False) -> Tuple[List[str], List[str]]:
    """
    Perform semantic validation beyond schema validation.
    
    Args:
        circuit_data: Loaded circuit data
        strict: Enable strict validation mode
        
    Returns:
        Tuple of (errors, warnings)
    """
    errors = []
    warnings = []
    
    components = circuit_data.get('components', [])
    component_ids = set()
    
    # Check for duplicate component IDs
    for comp in components:
        comp_id = comp.get('id')
        if comp_id in component_ids:
            errors.append(f"Duplicate component ID: {comp_id}")
        component_ids.add(comp_id)
    
    # Validate connections/nets
    if 'connections' in circuit_data:
        connections = circuit_data['connections']
        for conn in connections:
            from_pin = conn.get('from', '')
            to_pin = conn.get('to', '')
            
            # Check if components exist
            from_comp = from_pin.split('.')[0] if '.' in from_pin else from_pin
            to_comp = to_pin.split('.')[0] if '.' in to_pin else to_pin
            
            if from_comp not in component_ids and from_comp not in ['VCC', 'GND']:
                errors.append(f"Connection references non-existent component: {from_comp}")
            if to_comp not in component_ids and to_comp not in ['VCC', 'GND']:
                errors.append(f"Connection references non-existent component: {to_comp}")
    
    if 'nets' in circuit_data:
        nets = circuit_data['nets']
        net_ids = set()
        
        for net in nets:
            net_id = net.get('id', '')
            
            # Check for duplicate net IDs
            if net_id in net_ids:
                errors.append(f"Duplicate net ID: {net_id}")
            net_ids.add(net_id)
            
            # Validate net connections
            connections = net.get('connections', [])
            if len(connections) < 2:
                warnings.append(f"Net '{net_id}' has fewer than 2 connections")
            
            for conn in connections:
                comp_id = conn.get('component', '')
                if comp_id not in component_ids:
                    errors.append(f"Net '{net_id}' references non-existent component: {comp_id}")
    
    # Check for components without connections
    if strict:
        connected_components = set()
        
        if 'connections' in circuit_data:
            for conn in circuit_data['connections']:
                from_pin = conn.get('from', '')
                to_pin = conn.get('to', '')
                from_comp = from_pin.split('.')[0] if '.' in from_pin else from_pin
                to_comp = to_pin.split('.')[0] if '.' in to_pin else to_pin
                connected_components.add(from_comp)
                connected_components.add(to_comp)
        
        if 'nets' in circuit_data:
            for net in circuit_data['nets']:
                for conn in net.get('connections', []):
                    connected_components.add(conn.get('component', ''))
        
        for comp_id in component_ids:
            if comp_id not in connected_components:
                comp_type = next((c.get('type') for c in components if c.get('id') == comp_id), 'unknown')
                # Power supplies and ground don't need explicit connections
                if comp_type not in ['power_supply', 'ground']:
                    warnings.append(f"Component '{comp_id}' is not connected to any net")
    
    # Validate component-specific constraints
    for comp in components:
        comp_id = comp.get('id', 'unknown')
        comp_type = comp.get('type', '')
        params = comp.get('params', {})
        
        # Check resistor values
        if comp_type == 'resistor':
            resistance = params.get('resistance_ohm')
            if resistance is not None and resistance <= 0:
                errors.append(f"Component '{comp_id}': resistance must be positive")
        
        # Check capacitor values
        if comp_type == 'capacitor':
            capacitance = params.get('capacitance_f')
            if capacitance is not None and capacitance <= 0:
                errors.append(f"Component '{comp_id}': capacitance must be positive")
        
        # Check voltage ratings
        voltage_rating = params.get('voltage_rating_v')
        if voltage_rating is not None and voltage_rating <= 0:
            errors.append(f"Component '{comp_id}': voltage rating must be positive")
    
    return errors, warnings


def validate_json_syntax(file_path: str) -> Tuple[bool, Optional[str]]:
    """
    Quick validation of JSON syntax only.
    
    Args:
        file_path: Path to the circuit file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        return True, None
    except json.JSONDecodeError as e:
        return False, f"JSON syntax error at line {e.lineno}, column {e.colno}: {e.msg}"
    except Exception as e:
        return False, str(e)
