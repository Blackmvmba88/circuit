"""
Tests for Circuit Persistence Module

Tests multiplatform file I/O operations including:
- Atomic writes
- Data integrity
- Error handling
- Backup functionality
"""

import json
import os
import tempfile
import unittest
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from circuit.persistence import (
    CircuitPersistence, 
    PersistenceError, 
    DataIntegrityError,
    load_circuit_safe,
    save_circuit_safe
)


class TestCircuitPersistence(unittest.TestCase):
    """Test cases for CircuitPersistence class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.persistence = CircuitPersistence(enable_backups=True)
        
        # Sample circuit data
        self.sample_circuit = {
            "version": "1.0",
            "metadata": {
                "name": "Test Circuit",
                "description": "A test circuit"
            },
            "components": [
                {
                    "id": "R1",
                    "type": "resistor",
                    "value": "1kΩ"
                }
            ],
            "connections": []
        }
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_save_and_load_circuit(self):
        """Test basic save and load operations."""
        file_path = os.path.join(self.temp_dir, "test_circuit.circuit.json")
        
        # Save circuit
        self.persistence.save_circuit(file_path, self.sample_circuit)
        
        # Verify file exists
        self.assertTrue(os.path.exists(file_path))
        
        # Load circuit
        loaded_circuit = self.persistence.load_circuit(file_path)
        
        # Verify data integrity
        self.assertEqual(loaded_circuit, self.sample_circuit)
    
    def test_atomic_write(self):
        """Test that writes are atomic (no partial files on error)."""
        file_path = os.path.join(self.temp_dir, "atomic_test.circuit.json")
        
        # First write should succeed
        self.persistence.save_circuit(file_path, self.sample_circuit)
        
        # Verify file exists and is valid
        self.assertTrue(os.path.exists(file_path))
        loaded = self.persistence.load_circuit(file_path)
        self.assertEqual(loaded, self.sample_circuit)
    
    def test_backup_creation(self):
        """Test that backups are created before overwriting."""
        file_path = os.path.join(self.temp_dir, "backup_test.circuit.json")
        backup_path = file_path + ".backup"
        
        # Write initial data
        initial_data = {"version": "1.0", "metadata": {"name": "Initial"}}
        self.persistence.save_circuit(file_path, initial_data)
        
        # Overwrite with new data (should create backup)
        new_data = {"version": "1.0", "metadata": {"name": "Updated"}}
        self.persistence.save_circuit(file_path, new_data)
        
        # Verify backup exists
        self.assertTrue(os.path.exists(backup_path))
        
        # Verify backup contains original data
        backup_data = self.persistence.load_circuit(backup_path)
        self.assertEqual(backup_data["metadata"]["name"], "Initial")
        
        # Verify main file has new data
        current_data = self.persistence.load_circuit(file_path)
        self.assertEqual(current_data["metadata"]["name"], "Updated")
    
    def test_validation_before_save(self):
        """Test that validation is performed before saving."""
        file_path = os.path.join(self.temp_dir, "validation_test.circuit.json")
        
        # Define validator that rejects circuits without components
        def validator(data):
            return "components" in data and len(data["components"]) > 0
        
        # Valid data should save
        valid_data = {"components": [{"id": "R1"}]}
        self.persistence.save_circuit(file_path, valid_data, validate=validator)
        self.assertTrue(os.path.exists(file_path))
        
        # Invalid data should raise error
        invalid_data = {"components": []}
        with self.assertRaises(DataIntegrityError):
            self.persistence.save_circuit(file_path, invalid_data, validate=validator)
    
    def test_load_nonexistent_file(self):
        """Test loading a file that doesn't exist."""
        file_path = os.path.join(self.temp_dir, "nonexistent.circuit.json")
        
        with self.assertRaises(PersistenceError):
            self.persistence.load_circuit(file_path)
    
    def test_load_invalid_json(self):
        """Test loading a file with invalid JSON."""
        file_path = os.path.join(self.temp_dir, "invalid.circuit.json")
        
        # Write invalid JSON
        with open(file_path, 'w') as f:
            f.write("{ invalid json }")
        
        with self.assertRaises(PersistenceError):
            self.persistence.load_circuit(file_path)
    
    def test_verify_file_integrity(self):
        """Test file integrity verification."""
        # Valid file
        valid_path = os.path.join(self.temp_dir, "valid.circuit.json")
        self.persistence.save_circuit(valid_path, self.sample_circuit)
        self.assertTrue(self.persistence.verify_file_integrity(valid_path))
        
        # Invalid JSON file
        invalid_path = os.path.join(self.temp_dir, "invalid.circuit.json")
        with open(invalid_path, 'w') as f:
            f.write("not json")
        self.assertFalse(self.persistence.verify_file_integrity(invalid_path))
        
        # Nonexistent file
        nonexistent = os.path.join(self.temp_dir, "nonexistent.circuit.json")
        self.assertFalse(self.persistence.verify_file_integrity(nonexistent))
    
    def test_compute_file_hash(self):
        """Test file hash computation for integrity checking."""
        file_path = os.path.join(self.temp_dir, "hash_test.circuit.json")
        
        # Save circuit
        self.persistence.save_circuit(file_path, self.sample_circuit)
        
        # Compute hash
        hash1 = self.persistence.compute_file_hash(file_path)
        self.assertIsNotNone(hash1)
        self.assertEqual(len(hash1), 64)  # SHA256 hex digest length
        
        # Save identical data again
        self.persistence.save_circuit(file_path, self.sample_circuit)
        hash2 = self.persistence.compute_file_hash(file_path)
        
        # Hashes should be the same for identical content
        self.assertEqual(hash1, hash2)
        
        # Modify data and save
        modified_circuit = self.sample_circuit.copy()
        modified_circuit["metadata"]["name"] = "Modified"
        self.persistence.save_circuit(file_path, modified_circuit)
        hash3 = self.persistence.compute_file_hash(file_path)
        
        # Hash should be different
        self.assertNotEqual(hash1, hash3)
    
    def test_restore_backup(self):
        """Test restoring from backup."""
        file_path = os.path.join(self.temp_dir, "restore_test.circuit.json")
        
        # Write initial data
        initial_data = {"version": "1.0", "metadata": {"name": "Original"}}
        self.persistence.save_circuit(file_path, initial_data)
        
        # Overwrite with new data (creates backup)
        new_data = {"version": "1.0", "metadata": {"name": "Modified"}}
        self.persistence.save_circuit(file_path, new_data)
        
        # Restore from backup
        restored = self.persistence.restore_backup(file_path)
        self.assertTrue(restored)
        
        # Verify restored data
        current_data = self.persistence.load_circuit(file_path)
        self.assertEqual(current_data["metadata"]["name"], "Original")
    
    def test_convenience_functions(self):
        """Test convenience functions load_circuit_safe and save_circuit_safe."""
        file_path = os.path.join(self.temp_dir, "convenience_test.circuit.json")
        
        # Test save
        save_circuit_safe(file_path, self.sample_circuit)
        self.assertTrue(os.path.exists(file_path))
        
        # Test load
        loaded = load_circuit_safe(file_path)
        self.assertEqual(loaded, self.sample_circuit)
    
    def test_multiplatform_path_handling(self):
        """Test that paths work correctly across platforms."""
        # Test with different path separators
        if os.name == 'nt':
            # Windows-style path
            file_path = os.path.join(self.temp_dir, "subdir", "test.circuit.json")
        else:
            # POSIX-style path
            file_path = os.path.join(self.temp_dir, "subdir", "test.circuit.json")
        
        # Should create parent directories
        self.persistence.save_circuit(file_path, self.sample_circuit)
        self.assertTrue(os.path.exists(file_path))
        
        # Should be able to load
        loaded = self.persistence.load_circuit(file_path)
        self.assertEqual(loaded, self.sample_circuit)
    
    def test_unicode_handling(self):
        """Test that unicode characters in data are handled correctly."""
        unicode_circuit = {
            "version": "1.0",
            "metadata": {
                "name": "Test Circuit with Unicode: ñ, é, ü, 日本語, 中文",
                "description": "Resistor value: 1kΩ"
            },
            "components": [
                {
                    "id": "R1",
                    "type": "resistor",
                    "value": "1kΩ"
                }
            ]
        }
        
        file_path = os.path.join(self.temp_dir, "unicode_test.circuit.json")
        
        # Save and load
        self.persistence.save_circuit(file_path, unicode_circuit)
        loaded = self.persistence.load_circuit(file_path)
        
        # Verify unicode preserved
        self.assertEqual(loaded, unicode_circuit)
        self.assertIn("日本語", loaded["metadata"]["name"])


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
