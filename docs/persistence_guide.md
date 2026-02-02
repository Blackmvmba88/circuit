# Circuit Persistence Module Documentation

## Overview

The Circuit Persistence Module provides robust, multiplatform file I/O operations for circuit data with enhanced reliability and data integrity features.

## Features

### 1. Atomic Writes
Files are written atomically using a temporary file and rename operation. This ensures that:
- Target files are never in a partially written state
- Power failures or crashes don't corrupt existing files
- Concurrent access is safer

### 2. Automatic Backups
Before overwriting an existing file, a backup is automatically created with the `.backup` suffix. This allows easy recovery if needed.

### 3. Data Validation
Optional validation functions can be provided to verify data before saving, preventing invalid data from being persisted.

### 4. Retry Logic
Transient I/O errors are automatically retried with exponential backoff, improving reliability on network filesystems or busy systems.

### 5. Platform-Agnostic
The module handles platform-specific differences automatically:
- Windows vs POSIX file operations
- Different path separators
- Line ending conventions
- Unicode handling

### 6. File Integrity Checking
Built-in functions for verifying file integrity and computing checksums for change detection.

## Usage

### Basic Usage

```python
from circuit.persistence import CircuitPersistence

# Create persistence handler
persistence = CircuitPersistence(enable_backups=True)

# Load circuit
circuit_data = persistence.load_circuit("my_circuit.circuit.json")

# Modify data
circuit_data["metadata"]["version"] = "2.0"

# Save atomically with backup
persistence.save_circuit("my_circuit.circuit.json", circuit_data)
```

### Convenience Functions

For quick operations, use the convenience functions:

```python
from circuit.persistence import load_circuit_safe, save_circuit_safe

# Load
data = load_circuit_safe("circuit.json")

# Save
save_circuit_safe("circuit.json", data)
```

### With Data Validation

```python
def validate_circuit(data):
    """Ensure circuit has required fields."""
    return (
        "version" in data and
        "components" in data and
        len(data["components"]) > 0
    )

# Save with validation
persistence.save_circuit(
    "circuit.json",
    circuit_data,
    validate=validate_circuit
)
```

### File Integrity Checks

```python
# Verify file can be loaded
if persistence.verify_file_integrity("circuit.json"):
    print("File is valid")

# Compute checksum for change detection
hash1 = persistence.compute_file_hash("circuit.json")
# ... make changes ...
hash2 = persistence.compute_file_hash("circuit.json")
if hash1 != hash2:
    print("File has been modified")
```

### Backup and Restore

```python
# Backups are created automatically when overwriting
persistence.save_circuit("circuit.json", updated_data)

# Restore from backup if needed
if persistence.restore_backup("circuit.json"):
    print("Backup restored successfully")
else:
    print("No backup available")
```

## Configuration Options

```python
persistence = CircuitPersistence(
    enable_backups=True,      # Create backups before overwriting
    backup_suffix=".backup",  # Suffix for backup files
    max_retries=3,            # Maximum retry attempts
    retry_delay=0.1           # Initial delay between retries (seconds)
)
```

## Error Handling

The module defines specific exception types:

```python
from circuit.persistence import (
    PersistenceError,      # Base exception
    FileLockedError,       # File locked by another process
    DataIntegrityError     # Validation failed
)

try:
    data = persistence.load_circuit("circuit.json")
except PersistenceError as e:
    print(f"Failed to load: {e}")
except DataIntegrityError as e:
    print(f"Data validation failed: {e}")
```

## Platform-Specific Notes

### Windows
- Uses `replace()` for atomic file operations
- Handles backslash path separators
- Supports Unicode filenames

### Linux/macOS
- Uses atomic `rename()` operation
- Handles forward slash path separators
- Full POSIX compatibility

### All Platforms
- UTF-8 encoding for all files
- Consistent line ending handling
- Path operations use `pathlib.Path` for compatibility

## Integration with Circuit CLI

The Circuit CLI tool automatically uses the persistence module for all file operations:

```bash
# All commands use safe persistence
circuit validate my_circuit.circuit.json
circuit diff old.circuit.json new.circuit.json
circuit export circuit.json --format bom
```

## Performance Considerations

- Atomic writes require a temporary file, using slightly more disk I/O
- Backups double disk space usage temporarily
- File hashing requires reading the entire file
- Retry logic may add latency on slow or busy filesystems

For maximum performance on trusted systems, you can disable backups:

```python
persistence = CircuitPersistence(enable_backups=False)
```

## Best Practices

1. **Always use validation** when saving critical data
2. **Monitor backup files** and clean up old backups periodically
3. **Use file hashing** for change detection in version control scenarios
4. **Handle PersistenceError** exceptions appropriately in production code
5. **Test on target platforms** to ensure compatibility

## Advanced: File Locking

For concurrent access scenarios, use the file locking context manager:

```python
from circuit.persistence import safe_file_lock, PersistenceError

try:
    with safe_file_lock("circuit.json", timeout=5.0):
        # File is locked for exclusive access
        data = persistence.load_circuit("circuit.json")
        # Modify data
        persistence.save_circuit("circuit.json", data)
except FileLockedError:
    print("File is locked by another process")
```

**Note:** The file locking implementation is basic and uses lock files. For production use with heavy concurrent access, consider using the `filelock` package.

## Testing

Run the test suite to verify persistence functionality:

```bash
python3 test_persistence.py
```

Tests cover:
- Atomic writes
- Backup creation and restoration
- Data validation
- Error handling
- Unicode support
- Cross-platform compatibility

## Changelog

### Version 0.2.0
- Initial release with robust persistence features
- Atomic write operations
- Automatic backup creation
- Data validation support
- Retry logic for transient errors
- File integrity checking
- Full multiplatform support

## Contributing

When adding new persistence features:
1. Maintain backward compatibility
2. Add tests for new functionality
3. Update this documentation
4. Test on Windows, Linux, and macOS if possible
5. Handle errors gracefully

## License

MIT License - See LICENSE file for details
