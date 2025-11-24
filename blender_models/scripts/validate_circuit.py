"""
Circuit Design Validator
=========================

This utility validates circuit designs against EMI/noise best practices.
It reads .circuit.json files and checks for common issues.

Usage:
    python validate_circuit.py path/to/circuit.circuit.json
"""

import json
import sys
import math
from typing import Dict, List, Tuple, Any


class CircuitValidator:
    """Validates circuit designs for EMI/noise compliance."""
    
    def __init__(self, circuit_data: Dict[str, Any]):
        self.circuit = circuit_data
        self.warnings = []
        self.errors = []
        self.info = []
        
    def validate(self) -> Tuple[List[str], List[str], List[str]]:
        """Run all validation checks."""
        self.check_decoupling_capacitors()
        self.check_component_spacing()
        self.check_power_distribution()
        self.check_ground_connections()
        self.check_design_rules()
        
        return self.errors, self.warnings, self.info
    
    def check_decoupling_capacitors(self):
        """Check if ICs have proper decoupling capacitors nearby."""
        self.info.append("Checking decoupling capacitors...")
        
        ics = [c for c in self.circuit.get('components', []) 
               if c.get('type') == 'ic']
        caps = [c for c in self.circuit.get('components', []) 
                if c.get('type') == 'capacitor']
        
        for ic in ics:
            ic_id = ic.get('id')
            ic_pos = self._get_component_position(ic)
            
            if not ic_pos:
                continue
            
            # Find nearby capacitors
            nearby_caps = []
            for cap in caps:
                cap_pos = self._get_component_position(cap)
                if cap_pos:
                    distance = self._calculate_distance(ic_pos, cap_pos)
                    if distance < 10:  # Within 10mm
                        nearby_caps.append((cap, distance))
            
            if not nearby_caps:
                self.warnings.append(
                    f"IC {ic_id} has no decoupling capacitor within 10mm. "
                    f"Add 100nF capacitor within 5mm of VCC pin."
                )
            else:
                # Check for 100nF cap
                has_100nf = False
                for cap, dist in nearby_caps:
                    cap_value = cap.get('params', {}).get('capacitance_f', 0)
                    if 80e-9 <= cap_value <= 120e-9:  # 80-120nF range
                        has_100nf = True
                        if dist > 5:
                            self.warnings.append(
                                f"Decoupling cap {cap.get('id')} for IC {ic_id} "
                                f"is {dist:.1f}mm away. Should be < 5mm."
                            )
                
                if not has_100nf:
                    self.warnings.append(
                        f"IC {ic_id} should have 100nF ceramic capacitor nearby."
                    )
    
    def check_component_spacing(self):
        """Check component spacing for EMI compliance."""
        self.info.append("Checking component spacing...")
        
        components = self.circuit.get('components', [])
        
        # Minimum spacing rules (in mm)
        SPACING_RULES = {
            ('ic', 'ic'): 5.0,
            ('connector', 'ic'): 15.0,
            ('led', 'ic'): 5.0,
            'default': 2.0
        }
        
        for i, comp1 in enumerate(components):
            pos1 = self._get_component_position(comp1)
            if not pos1:
                continue
                
            for comp2 in components[i+1:]:
                pos2 = self._get_component_position(comp2)
                if not pos2:
                    continue
                
                distance = self._calculate_distance(pos1, pos2)
                type1 = comp1.get('type')
                type2 = comp2.get('type')
                
                # Get minimum spacing
                min_spacing = SPACING_RULES.get(
                    tuple(sorted([type1, type2])),
                    SPACING_RULES['default']
                )
                
                if distance < min_spacing:
                    self.warnings.append(
                        f"Components {comp1.get('id')} and {comp2.get('id')} "
                        f"are only {distance:.1f}mm apart. "
                        f"Recommended minimum: {min_spacing}mm"
                    )
    
    def check_power_distribution(self):
        """Check power supply network."""
        self.info.append("Checking power distribution...")
        
        # Check for bulk capacitors
        caps = [c for c in self.circuit.get('components', []) 
                if c.get('type') == 'capacitor']
        
        bulk_caps = [c for c in caps 
                     if c.get('params', {}).get('capacitance_f', 0) >= 10e-6]
        
        if not bulk_caps:
            self.errors.append(
                "No bulk capacitor (≥10µF) found in power supply. "
                "Add bulk capacitor at power input."
            )
        
        # Check for HF bypass capacitors
        hf_caps = [c for c in caps 
                   if 80e-9 <= c.get('params', {}).get('capacitance_f', 0) <= 120e-9]
        
        if not hf_caps:
            self.warnings.append(
                "No 100nF bypass capacitors found. "
                "Add 100nF ceramic capacitors for high-frequency filtering."
            )
        
        # Check if VCC and GND nets exist
        nets = self.circuit.get('nets', [])
        net_names = [n.get('name', '').upper() for n in nets]
        
        has_power = any(name in ['VCC', 'VDD', 'V+', '+5V', '+3V3'] 
                       for name in net_names)
        has_ground = any(name in ['GND', 'VSS', 'V-', 'GROUND'] 
                        for name in net_names)
        
        if not has_power:
            self.errors.append("No power net (VCC/VDD) found in netlist.")
        if not has_ground:
            self.errors.append("No ground net (GND) found in netlist.")
    
    def check_ground_connections(self):
        """Check ground connectivity."""
        self.info.append("Checking ground connections...")
        
        # Find GND net
        nets = self.circuit.get('nets', [])
        gnd_net = None
        for net in nets:
            name = net.get('name', '').upper()
            if name in ['GND', 'VSS', 'V-', 'GROUND']:
                gnd_net = net
                break
        
        if not gnd_net:
            return
        
        # Check number of ground connections
        connections = gnd_net.get('connections', [])
        if len(connections) < 2:
            self.errors.append(
                "Ground net has fewer than 2 connections. "
                "All components should be connected to ground."
            )
        
        # Check if all ICs are connected to ground
        ics = [c.get('id') for c in self.circuit.get('components', []) 
               if c.get('type') == 'ic']
        
        gnd_components = [conn.get('component') for conn in connections]
        
        for ic in ics:
            if ic not in gnd_components:
                self.warnings.append(
                    f"IC {ic} does not appear to be connected to ground. "
                    f"Verify ground connection."
                )
    
    def check_design_rules(self):
        """Check if design follows specified rules."""
        self.info.append("Checking design rules...")
        
        rules = self.circuit.get('design_rules', {})
        
        if not rules:
            self.info.append(
                "No design_rules section found. "
                "Consider adding EMI compliance specifications."
            )
            return
        
        # Check EMI compliance
        emi = rules.get('emi_compliance', {})
        if emi:
            standard = emi.get('standard')
            if standard:
                self.info.append(f"Design targets {standard} compliance.")
            
            # Validate decoupling strategy
            strategy = emi.get('decoupling_strategy', '')
            if '100nF' not in strategy and '100n' not in strategy:
                self.warnings.append(
                    "Decoupling strategy should include 100nF capacitors."
                )
    
    def _get_component_position(self, component: Dict) -> Tuple[float, float] | None:
        """Extract component position from various sources."""
        # Try model_3d position first
        if 'model_3d' in component:
            pos = component['model_3d'].get('position')
            if pos and 'x' in pos and 'y' in pos:
                return (pos['x'], pos['y'])
        
        # Try first pin position
        pins = component.get('pins', {})
        if pins:
            first_pin = next(iter(pins.values()))
            if 'x' in first_pin and 'y' in first_pin:
                return (first_pin['x'], first_pin['y'])
        
        return None
    
    def _calculate_distance(self, pos1: Tuple[float, float], 
                           pos2: Tuple[float, float]) -> float:
        """Calculate Euclidean distance between two positions."""
        return math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)


def print_report(errors: List[str], warnings: List[str], info: List[str]):
    """Print validation report."""
    print("\n" + "="*70)
    print("CIRCUIT VALIDATION REPORT")
    print("="*70)
    
    if info:
        print("\n📋 INFO:")
        for msg in info:
            print(f"  ℹ️  {msg}")
    
    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for msg in warnings:
            print(f"  ⚠️  {msg}")
    else:
        print("\n✅ No warnings found.")
    
    if errors:
        print(f"\n❌ ERRORS ({len(errors)}):")
        for msg in errors:
            print(f"  ❌ {msg}")
        print("\n⛔ Circuit has critical errors. Fix before fabrication.")
    else:
        print("\n✅ No errors found.")
    
    print("\n" + "="*70)
    
    # Summary
    total_issues = len(errors) + len(warnings)
    if total_issues == 0:
        print("✅ Circuit validation PASSED. Design looks good!")
    elif len(errors) == 0:
        print(f"⚠️  Circuit validation passed with {len(warnings)} warning(s).")
        print("   Review warnings before fabrication.")
    else:
        print(f"❌ Circuit validation FAILED with {len(errors)} error(s).")
        print("   Fix errors before fabrication.")
    print("="*70 + "\n")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python validate_circuit.py <circuit.json>")
        print("\nExample:")
        print("  python validate_circuit.py examples/circuit_with_3d.circuit.json")
        sys.exit(1)
    
    circuit_file = sys.argv[1]
    
    try:
        with open(circuit_file, 'r') as f:
            circuit_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File '{circuit_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in '{circuit_file}': {e}")
        sys.exit(1)
    
    print(f"\n🔍 Validating circuit: {circuit_data.get('metadata', {}).get('name', 'Unknown')}")
    
    validator = CircuitValidator(circuit_data)
    errors, warnings, info = validator.validate()
    
    print_report(errors, warnings, info)
    
    # Exit code: 0 if no errors, 1 if errors found
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
