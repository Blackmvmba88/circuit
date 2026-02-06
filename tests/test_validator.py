"""
Comprehensive tests for circuit validator.

Tests JSON schema validation, semantic validation, and edge cases.
"""

import json
import os
import tempfile
import unittest
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cli.validator import (
    validate_circuit_file,
    validate_semantics,
    validate_json_syntax,
    load_schema
)


class TestSchemaValidation(unittest.TestCase):
    """Test JSON schema validation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.schema = load_schema()
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def _create_temp_circuit(self, data):
        """Helper to create temporary circuit file."""
        file_path = os.path.join(self.temp_dir, "test_circuit.circuit.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        return file_path
    
    def test_minimal_valid_circuit(self):
        """Test that a minimal valid circuit passes validation."""
        circuit = {
            "version": "1.0",
            "metadata": {
                "name": "Minimal Circuit"
            },
            "components": [
                {
                    "id": "R1",
                    "type": "resistor"
                }
            ]
        }
        file_path = self._create_temp_circuit(circuit)
        is_valid, errors, warnings = validate_circuit_file(file_path)
        self.assertTrue(is_valid, f"Validation failed: {errors}")
    
    def test_missing_version(self):
        """Test that missing version field fails validation."""
        circuit = {
            "metadata": {"name": "Test"},
            "components": [{"id": "R1", "type": "resistor"}]
        }
        file_path = self._create_temp_circuit(circuit)
        is_valid, errors, warnings = validate_circuit_file(file_path)
        self.assertFalse(is_valid)
        self.assertTrue(any("version" in err.lower() for err in errors))
    
    def test_missing_metadata(self):
        """Test that missing metadata field fails validation."""
        circuit = {
            "version": "1.0",
            "components": [{"id": "R1", "type": "resistor"}]
        }
        file_path = self._create_temp_circuit(circuit)
        is_valid, errors, warnings = validate_circuit_file(file_path)
        self.assertFalse(is_valid)
        self.assertTrue(any("metadata" in err.lower() for err in errors))
    
    def test_missing_components(self):
        """Test that missing components field fails validation."""
        circuit = {
            "version": "1.0",
            "metadata": {"name": "Test"}
        }
        file_path = self._create_temp_circuit(circuit)
        is_valid, errors, warnings = validate_circuit_file(file_path)
        self.assertFalse(is_valid)
        self.assertTrue(any("components" in err.lower() for err in errors))
    
    def test_empty_components(self):
        """Test that empty components array fails validation."""
        circuit = {
            "version": "1.0",
            "metadata": {"name": "Test"},
            "components": []
        }
        file_path = self._create_temp_circuit(circuit)
        is_valid, errors, warnings = validate_circuit_file(file_path)
        self.assertFalse(is_valid)
    
    def test_invalid_version_format(self):
        """Test that invalid version format fails validation."""
        circuit = {
            "version": "invalid",
            "metadata": {"name": "Test"},
            "components": [{"id": "R1", "type": "resistor"}]
        }
        file_path = self._create_temp_circuit(circuit)
        is_valid, errors, warnings = validate_circuit_file(file_path)
        self.assertFalse(is_valid)
    
    def test_invalid_component_type(self):
        """Test that invalid component type fails validation."""
        circuit = {
            "version": "1.0",
            "metadata": {"name": "Test"},
            "components": [
                {
                    "id": "X1",
                    "type": "invalid_type"
                }
            ]
        }
        file_path = self._create_temp_circuit(circuit)
        is_valid, errors, warnings = validate_circuit_file(file_path)
        self.assertFalse(is_valid)
    
    def test_component_missing_id(self):
        """Test that component missing ID fails validation."""
        circuit = {
            "version": "1.0",
            "metadata": {"name": "Test"},
            "components": [
                {
                    "type": "resistor"
                }
            ]
        }
        file_path = self._create_temp_circuit(circuit)
        is_valid, errors, warnings = validate_circuit_file(file_path)
        self.assertFalse(is_valid)
        self.assertTrue(any("id" in err.lower() for err in errors))
    
    def test_component_missing_type(self):
        """Test that component missing type fails validation."""
        circuit = {
            "version": "1.0",
            "metadata": {"name": "Test"},
            "components": [
                {
                    "id": "R1"
                }
            ]
        }
        file_path = self._create_temp_circuit(circuit)
        is_valid, errors, warnings = validate_circuit_file(file_path)
        self.assertFalse(is_valid)
        self.assertTrue(any("type" in err.lower() for err in errors))


class TestSemanticValidation(unittest.TestCase):
    """Test semantic validation beyond schema."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def _create_temp_circuit(self, data):
        """Helper to create temporary circuit file."""
        file_path = os.path.join(self.temp_dir, "test_circuit.circuit.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        return file_path
    
    def test_duplicate_component_ids(self):
        """Test that duplicate component IDs are detected."""
        circuit = {
            "version": "1.0",
            "metadata": {"name": "Test"},
            "components": [
                {"id": "R1", "type": "resistor"},
                {"id": "R1", "type": "resistor"}
            ]
        }
        file_path = self._create_temp_circuit(circuit)
        is_valid, errors, warnings = validate_circuit_file(file_path)
        self.assertFalse(is_valid)
        self.assertTrue(any("duplicate" in err.lower() and "R1" in err for err in errors))
    
    def test_connection_to_nonexistent_component(self):
        """Test that connections to non-existent components are detected."""
        circuit = {
            "version": "1.0",
            "metadata": {"name": "Test"},
            "components": [
                {"id": "R1", "type": "resistor"}
            ],
            "connections": [
                {"from": "R1.1", "to": "R2.1"}
            ]
        }
        file_path = self._create_temp_circuit(circuit)
        is_valid, errors, warnings = validate_circuit_file(file_path)
        self.assertFalse(is_valid)
        self.assertTrue(any("R2" in err for err in errors))
    
    def test_special_components_allowed_in_connections(self):
        """Test that special components (VCC, GND) are allowed in connections."""
        circuit = {
            "version": "1.0",
            "metadata": {"name": "Test"},
            "components": [
                {"id": "R1", "type": "resistor"}
            ],
            "connections": [
                {"from": "VCC", "to": "R1.1"},
                {"from": "R1.2", "to": "GND"}
            ]
        }
        file_path = self._create_temp_circuit(circuit)
        is_valid, errors, warnings = validate_circuit_file(file_path)
        self.assertTrue(is_valid, f"Should allow VCC and GND: {errors}")
    
    def test_net_with_nonexistent_component(self):
        """Test that nets referencing non-existent components are detected."""
        circuit = {
            "version": "1.0",
            "metadata": {"name": "Test"},
            "components": [
                {"id": "R1", "type": "resistor"}
            ],
            "nets": [
                {
                    "id": "NET1",
                    "connections": [
                        {"component": "R1", "pin": "1"},
                        {"component": "R2", "pin": "1"}
                    ]
                }
            ]
        }
        file_path = self._create_temp_circuit(circuit)
        is_valid, errors, warnings = validate_circuit_file(file_path)
        self.assertFalse(is_valid)
        self.assertTrue(any("R2" in err for err in errors))
    
    def test_duplicate_net_ids(self):
        """Test that duplicate net IDs are detected."""
        circuit = {
            "version": "1.0",
            "metadata": {"name": "Test"},
            "components": [
                {"id": "R1", "type": "resistor"},
                {"id": "R2", "type": "resistor"}
            ],
            "nets": [
                {
                    "id": "NET1",
                    "connections": [
                        {"component": "R1", "pin": "1"},
                        {"component": "R2", "pin": "1"}
                    ]
                },
                {
                    "id": "NET1",
                    "connections": [
                        {"component": "R1", "pin": "2"},
                        {"component": "R2", "pin": "2"}
                    ]
                }
            ]
        }
        file_path = self._create_temp_circuit(circuit)
        is_valid, errors, warnings = validate_circuit_file(file_path)
        self.assertFalse(is_valid)
        self.assertTrue(any("duplicate" in err.lower() and "NET1" in err for err in errors))
    
    def test_net_with_few_connections_warning(self):
        """Test that nets with < 2 connections generate a warning."""
        circuit = {
            "version": "1.0",
            "metadata": {"name": "Test"},
            "components": [
                {"id": "R1", "type": "resistor"}
            ],
            "nets": [
                {
                    "id": "NET1",
                    "connections": [
                        {"component": "R1", "pin": "1"}
                    ]
                }
            ]
        }
        file_path = self._create_temp_circuit(circuit)
        is_valid, errors, warnings = validate_circuit_file(file_path)
        self.assertTrue(is_valid)
        self.assertTrue(any("NET1" in warn and "fewer than 2" in warn.lower() for warn in warnings))
    
    def test_negative_resistance_error(self):
        """Test that negative resistance values are detected."""
        circuit = {
            "version": "1.0",
            "metadata": {"name": "Test"},
            "components": [
                {
                    "id": "R1",
                    "type": "resistor",
                    "params": {
                        "resistance_ohm": -100
                    }
                }
            ]
        }
        file_path = self._create_temp_circuit(circuit)
        is_valid, errors, warnings = validate_circuit_file(file_path)
        self.assertFalse(is_valid)
        self.assertTrue(any("R1" in err and "positive" in err.lower() for err in errors))
    
    def test_negative_capacitance_error(self):
        """Test that negative capacitance values are detected."""
        circuit = {
            "version": "1.0",
            "metadata": {"name": "Test"},
            "components": [
                {
                    "id": "C1",
                    "type": "capacitor",
                    "params": {
                        "capacitance_f": -0.000001
                    }
                }
            ]
        }
        file_path = self._create_temp_circuit(circuit)
        is_valid, errors, warnings = validate_circuit_file(file_path)
        self.assertFalse(is_valid)
        self.assertTrue(any("C1" in err and "positive" in err.lower() for err in errors))


class TestJSONSyntaxValidation(unittest.TestCase):
    """Test JSON syntax validation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_valid_json_syntax(self):
        """Test that valid JSON syntax passes."""
        file_path = os.path.join(self.temp_dir, "valid.json")
        with open(file_path, 'w') as f:
            f.write('{"version": "1.0", "metadata": {"name": "Test"}}')
        
        is_valid, error = validate_json_syntax(file_path)
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_invalid_json_syntax(self):
        """Test that invalid JSON syntax is detected."""
        file_path = os.path.join(self.temp_dir, "invalid.json")
        with open(file_path, 'w') as f:
            f.write('{"invalid": json}')
        
        is_valid, error = validate_json_syntax(file_path)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
        self.assertIn("syntax error", error.lower())


class TestExampleCircuits(unittest.TestCase):
    """Test that all example circuits are valid."""
    
    def test_simple_circuit_validation(self):
        """Test that simple_circuit.circuit.json validates correctly."""
        file_path = Path(__file__).parent.parent / "examples" / "simple_circuit.circuit.json"
        if file_path.exists():
            is_valid, errors, warnings = validate_circuit_file(str(file_path))
            self.assertTrue(is_valid, f"simple_circuit.circuit.json failed validation: {errors}")
    
    def test_all_examples_validate(self):
        """Test that all example circuits validate correctly."""
        examples_dir = Path(__file__).parent.parent / "examples"
        if not examples_dir.exists():
            self.skipTest("Examples directory not found")
        
        circuit_files = list(examples_dir.glob("*.circuit.json"))
        self.assertGreater(len(circuit_files), 0, "No example circuits found")
        
        for circuit_file in circuit_files:
            with self.subTest(circuit=circuit_file.name):
                is_valid, errors, warnings = validate_circuit_file(str(circuit_file))
                self.assertTrue(is_valid, 
                    f"{circuit_file.name} failed validation:\n" + 
                    "\n".join(f"  - {err}" for err in errors))


if __name__ == '__main__':
    unittest.main(verbosity=2)
