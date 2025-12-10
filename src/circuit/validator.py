"""
Circuit Validator Module

Validates .circuit.json files against the JSON schema and performs semantic validation.
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
import jsonschema
from jsonschema import validate, ValidationError


class CircuitValidator:
    """
    Validates circuit files for both schema compliance and semantic correctness.
    """
    
    def __init__(self, circuit_data: Dict[str, Any], schema_path: Optional[str] = None):
        """
        Initialize the validator.
        
        Args:
            circuit_data: The circuit data to validate
            schema_path: Optional path to custom schema file
        """
        self.circuit = circuit_data
        self.schema_path = schema_path
        self.errors = []
        self.warnings = []
        self.info = []
        
    def validate(self) -> Tuple[bool, Dict[str, List[str]]]:
        """
        Run all validation checks.
        
        Returns:
            Tuple of (is_valid, results_dict)
        """
        # Schema validation
        self._validate_schema()
        
        # Semantic validation
        if not self.errors:  # Only continue if schema is valid
            self._validate_components()
            self._validate_connections()
            self._validate_nets()
            self._validate_component_values()
            self._validate_pins()
        
        results = {
            'errors': self.errors,
            'warnings': self.warnings,
            'info': self.info
        }
        
        is_valid = len(self.errors) == 0
        return is_valid, results
    
    def _validate_schema(self):
        """Validate against JSON schema."""
        self.info.append("Validating against JSON schema...")
        
        try:
            # Load schema
            if self.schema_path:
                schema_file = Path(self.schema_path)
            else:
                schema_file = Path(__file__).parent / 'schema.json'
            
            if not schema_file.exists():
                self.warnings.append(f"Schema file not found at {schema_file}, skipping schema validation")
                return
            
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema = json.load(f)
            
            # Validate
            validate(instance=self.circuit, schema=schema)
            self.info.append("✓ Schema validation passed")
            
        except ValidationError as e:
            self.errors.append(f"Schema validation failed: {e.message}")
            if e.path:
                path = '.'.join(str(p) for p in e.path)
                self.errors.append(f"  At: {path}")
        except Exception as e:
            self.warnings.append(f"Schema validation error: {str(e)}")
    
    def _validate_components(self):
        """Validate component definitions."""
        self.info.append("Validating components...")
        
        components = self.circuit.get('components', [])
        
        if not components:
            self.errors.append("No components defined in circuit")
            return
        
        # Track component IDs to check for duplicates
        component_ids = set()
        
        for i, comp in enumerate(components):
            comp_id = comp.get('id')
            
            # Check for duplicate IDs
            if comp_id in component_ids:
                self.errors.append(f"Duplicate component ID: {comp_id}")
            else:
                component_ids.add(comp_id)
            
            # Check component type
            comp_type = comp.get('type')
            if not comp_type:
                self.errors.append(f"Component {comp_id} has no type specified")
            
            # Type-specific validation
            if comp_type == 'resistor':
                self._validate_resistor(comp)
            elif comp_type == 'capacitor':
                self._validate_capacitor(comp)
            elif comp_type == 'led':
                self._validate_led(comp)
        
        self.info.append(f"✓ Found {len(components)} components")
    
    def _validate_resistor(self, comp: Dict):
        """Validate resistor component."""
        comp_id = comp.get('id')
        
        # Check for value or params.resistance_ohm
        value = comp.get('value')
        resistance = comp.get('params', {}).get('resistance_ohm')
        
        if not value and not resistance:
            self.warnings.append(f"Resistor {comp_id} has no value specified")
        
        # Check power rating
        power = comp.get('power') or comp.get('params', {}).get('power_rating_w')
        if not power:
            self.warnings.append(f"Resistor {comp_id} has no power rating specified")
    
    def _validate_capacitor(self, comp: Dict):
        """Validate capacitor component."""
        comp_id = comp.get('id')
        
        # Check for value or params.capacitance_f
        value = comp.get('value')
        capacitance = comp.get('params', {}).get('capacitance_f')
        
        if not value and not capacitance:
            self.warnings.append(f"Capacitor {comp_id} has no value specified")
        
        # Check voltage rating
        voltage = comp.get('params', {}).get('voltage_rating_v')
        if not voltage:
            self.warnings.append(f"Capacitor {comp_id} has no voltage rating specified")
    
    def _validate_led(self, comp: Dict):
        """Validate LED component."""
        comp_id = comp.get('id')
        
        # Check for color
        color = comp.get('color') or comp.get('params', {}).get('color')
        if not color:
            self.warnings.append(f"LED {comp_id} has no color specified")
        
        # Check forward voltage
        fv = comp.get('forward_voltage') or comp.get('params', {}).get('forward_voltage_v')
        if not fv:
            self.warnings.append(f"LED {comp_id} has no forward voltage specified")
    
    def _validate_connections(self):
        """Validate connections (legacy format)."""
        connections = self.circuit.get('connections', [])
        
        if not connections:
            # This is OK if nets are used instead
            return
        
        self.info.append("Validating connections...")
        
        # Get all component IDs
        component_ids = {comp.get('id') for comp in self.circuit.get('components', [])}
        
        for conn in connections:
            from_point = conn.get('from', '')
            to_point = conn.get('to', '')
            
            # Parse connection points (format: "COMP.pin" or "NET")
            from_comp = from_point.split('.')[0] if '.' in from_point else from_point
            to_comp = to_point.split('.')[0] if '.' in to_point else to_point
            
            # Check if components exist
            if from_comp not in component_ids and from_comp not in ['VCC', 'GND']:
                self.errors.append(f"Connection references unknown component: {from_comp}")
            
            if to_comp not in component_ids and to_comp not in ['VCC', 'GND']:
                self.errors.append(f"Connection references unknown component: {to_comp}")
        
        self.info.append(f"✓ Found {len(connections)} connections")
    
    def _validate_nets(self):
        """Validate net definitions."""
        nets = self.circuit.get('nets', [])
        
        if not nets:
            # This is OK if using legacy connections format
            return
        
        self.info.append("Validating nets...")
        
        # Get all component IDs and their pins
        component_pins = {}
        for comp in self.circuit.get('components', []):
            comp_id = comp.get('id')
            pins = comp.get('pins', {})
            component_pins[comp_id] = set(pins.keys())
        
        # Track net names for duplicates
        net_names = set()
        
        for net in nets:
            net_id = net.get('id')
            net_name = net.get('name', net_id)
            
            # Check for duplicate net names
            if net_name in net_names:
                self.warnings.append(f"Duplicate net name: {net_name}")
            else:
                net_names.add(net_name)
            
            # Validate connections
            connections = net.get('connections', [])
            
            if len(connections) < 2:
                self.warnings.append(f"Net {net_id} has fewer than 2 connections")
            
            for conn in connections:
                comp_id = conn.get('component')
                pin = conn.get('pin')
                
                # Check if component exists
                if comp_id not in component_pins:
                    self.errors.append(f"Net {net_id} references unknown component: {comp_id}")
                    continue
                
                # Check if pin exists
                if pin not in component_pins[comp_id]:
                    self.errors.append(
                        f"Net {net_id} references undeclared pin {pin} on component {comp_id}"
                    )
        
        self.info.append(f"✓ Found {len(nets)} nets")
    
    def _validate_component_values(self):
        """Validate component values for correctness."""
        self.info.append("Validating component values...")
        
        for comp in self.circuit.get('components', []):
            comp_id = comp.get('id')
            comp_type = comp.get('type')
            
            # Validate numeric parameters
            params = comp.get('params', {})
            
            # Check for negative values where they don't make sense
            if comp_type == 'resistor':
                resistance = params.get('resistance_ohm', 0)
                if isinstance(resistance, (int, float)) and resistance < 0:
                    self.errors.append(f"Component {comp_id} has negative resistance: {resistance}")
            
            elif comp_type == 'capacitor':
                capacitance = params.get('capacitance_f', 0)
                if isinstance(capacitance, (int, float)) and capacitance < 0:
                    self.errors.append(f"Component {comp_id} has negative capacitance: {capacitance}")
            
            # Check voltage ratings
            voltage_rating = params.get('voltage_rating_v', 0)
            if isinstance(voltage_rating, (int, float)) and voltage_rating < 0:
                self.warnings.append(f"Component {comp_id} has negative voltage rating")
    
    def _validate_pins(self):
        """Validate pin definitions and check for undeclared pads."""
        self.info.append("Validating pins and pads...")
        
        # Build a set of all declared pins
        declared_pins = set()
        for comp in self.circuit.get('components', []):
            comp_id = comp.get('id')
            pins = comp.get('pins', {})
            for pin_name in pins.keys():
                declared_pins.add(f"{comp_id}.{pin_name}")
        
        # Check nets for references to undeclared pins
        for net in self.circuit.get('nets', []):
            net_id = net.get('id')
            for conn in net.get('connections', []):
                comp_id = conn.get('component')
                pin = conn.get('pin')
                pin_ref = f"{comp_id}.{pin}"
                
                # We already check this in _validate_nets, so skip
                pass
        
        # Check connections for references to undeclared pins
        for conn in self.circuit.get('connections', []):
            from_point = conn.get('from', '')
            to_point = conn.get('to', '')
            
            # Check if these reference specific pins
            for point in [from_point, to_point]:
                if '.' in point and point not in ['VCC.positive', 'GND']:
                    comp_id, pin = point.split('.', 1)
                    if point not in declared_pins:
                        # Find component to check if it exists
                        comp_exists = any(c.get('id') == comp_id 
                                        for c in self.circuit.get('components', []))
                        if comp_exists:
                            self.warnings.append(
                                f"Connection uses undeclared pin: {point}"
                            )
