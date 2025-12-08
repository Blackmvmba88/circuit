"""
Circuit Diff Module

Compares two circuit files and identifies differences.
"""

from typing import Dict, List, Any


class CircuitDiff:
    """
    Compares two circuit designs and identifies differences.
    """
    
    def __init__(self, old_circuit: Dict[str, Any], new_circuit: Dict[str, Any]):
        """
        Initialize the diff engine.
        
        Args:
            old_circuit: The old/original circuit data
            new_circuit: The new/modified circuit data
        """
        self.old = old_circuit
        self.new = new_circuit
    
    def compute_diff(self) -> Dict[str, List]:
        """
        Compute differences between circuits.
        
        Returns:
            Dictionary containing lists of changes:
            - components_added: List of added components
            - components_removed: List of removed components
            - components_modified: List of modified components with changes
            - nets_changed: List of changed net IDs
        """
        results = {
            'components_added': [],
            'components_removed': [],
            'components_modified': [],
            'nets_changed': [],
            'metadata_changes': {},
        }
        
        # Compare metadata
        results['metadata_changes'] = self._diff_metadata()
        
        # Compare components
        comp_diff = self._diff_components()
        results['components_added'] = comp_diff['added']
        results['components_removed'] = comp_diff['removed']
        results['components_modified'] = comp_diff['modified']
        
        # Compare nets
        results['nets_changed'] = self._diff_nets()
        
        return results
    
    def _diff_metadata(self) -> Dict[str, tuple]:
        """Compare metadata between circuits."""
        old_meta = self.old.get('metadata', {})
        new_meta = self.new.get('metadata', {})
        
        changes = {}
        
        # Check all keys from both old and new
        all_keys = set(old_meta.keys()) | set(new_meta.keys())
        
        for key in all_keys:
            old_val = old_meta.get(key)
            new_val = new_meta.get(key)
            
            if old_val != new_val:
                changes[key] = (old_val, new_val)
        
        return changes
    
    def _diff_components(self) -> Dict[str, List]:
        """Compare components between circuits."""
        old_comps = {comp['id']: comp for comp in self.old.get('components', [])}
        new_comps = {comp['id']: comp for comp in self.new.get('components', [])}
        
        old_ids = set(old_comps.keys())
        new_ids = set(new_comps.keys())
        
        # Find added and removed
        added_ids = new_ids - old_ids
        removed_ids = old_ids - new_ids
        common_ids = old_ids & new_ids
        
        added = [new_comps[comp_id] for comp_id in added_ids]
        removed = [old_comps[comp_id] for comp_id in removed_ids]
        
        # Find modified
        modified = []
        for comp_id in common_ids:
            old_comp = old_comps[comp_id]
            new_comp = new_comps[comp_id]
            
            changes = self._compare_components(old_comp, new_comp)
            if changes:
                modified.append({
                    'id': comp_id,
                    'changes': changes
                })
        
        return {
            'added': added,
            'removed': removed,
            'modified': modified
        }
    
    def _compare_components(self, old_comp: Dict, new_comp: Dict) -> Dict[str, tuple]:
        """
        Compare two component definitions.
        
        Returns:
            Dictionary of changed fields with (old_value, new_value) tuples
        """
        changes = {}
        
        # Fields to compare
        compare_fields = ['type', 'value', 'package', 'description', 'tolerance', 
                         'power', 'voltage', 'color', 'notes']
        
        for field in compare_fields:
            old_val = old_comp.get(field)
            new_val = new_comp.get(field)
            
            if old_val != new_val and (old_val is not None or new_val is not None):
                changes[field] = (old_val, new_val)
        
        # Compare params dict
        old_params = old_comp.get('params', {})
        new_params = new_comp.get('params', {})
        
        if old_params != new_params:
            # Find specific param changes
            all_param_keys = set(old_params.keys()) | set(new_params.keys())
            for key in all_param_keys:
                old_val = old_params.get(key)
                new_val = new_params.get(key)
                if old_val != new_val:
                    changes[f'params.{key}'] = (old_val, new_val)
        
        # Compare pins
        old_pins = old_comp.get('pins', {})
        new_pins = new_comp.get('pins', {})
        
        if old_pins != new_pins:
            old_pin_ids = set(old_pins.keys())
            new_pin_ids = set(new_pins.keys())
            
            if old_pin_ids != new_pin_ids:
                changes['pins'] = (list(old_pin_ids), list(new_pin_ids))
            else:
                # Check individual pin changes
                for pin_id in old_pin_ids:
                    old_pin = old_pins[pin_id]
                    new_pin = new_pins[pin_id]
                    
                    # Check net assignment
                    old_net = old_pin.get('net')
                    new_net = new_pin.get('net')
                    if old_net != new_net:
                        changes[f'pin.{pin_id}.net'] = (old_net, new_net)
                    
                    # Check position
                    old_pos = (old_pin.get('x'), old_pin.get('y'))
                    new_pos = (new_pin.get('x'), new_pin.get('y'))
                    if old_pos != new_pos:
                        changes[f'pin.{pin_id}.position'] = (old_pos, new_pos)
        
        return changes
    
    def _diff_nets(self) -> List[str]:
        """
        Compare nets between circuits.
        
        Returns:
            List of net IDs that have changed
        """
        old_nets = {net['id']: net for net in self.old.get('nets', [])}
        new_nets = {net['id']: net for net in self.new.get('nets', [])}
        
        old_ids = set(old_nets.keys())
        new_ids = set(new_nets.keys())
        
        # Nets added or removed
        changed = list((new_ids - old_ids) | (old_ids - new_ids))
        
        # Nets with modified connections
        common_ids = old_ids & new_ids
        for net_id in common_ids:
            old_net = old_nets[net_id]
            new_net = new_nets[net_id]
            
            # Compare connections
            old_conns = self._normalize_connections(old_net.get('connections', []))
            new_conns = self._normalize_connections(new_net.get('connections', []))
            
            if old_conns != new_conns:
                changed.append(net_id)
        
        return changed
    
    def _normalize_connections(self, connections: List[Dict]) -> set:
        """
        Normalize connections to a set for comparison.
        
        Args:
            connections: List of connection dictionaries
            
        Returns:
            Set of (component, pin) tuples
        """
        return {
            (conn.get('component'), conn.get('pin'))
            for conn in connections
        }
