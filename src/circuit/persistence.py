"""
Circuit Persistence Module

Provides robust, multiplatform file I/O operations for circuit data with:
- Atomic writes (write to temp, then rename)
- File locking for concurrent access prevention
- Data integrity validation
- Automatic backups
- Comprehensive error handling

Author: circuit-project
License: MIT
"""

import json
import os
import shutil
import tempfile
import time
from pathlib import Path
from typing import Dict, Any, Optional, Callable
from contextlib import contextmanager
import hashlib


class PersistenceError(Exception):
    """Base exception for persistence operations."""
    pass


class FileLockedError(PersistenceError):
    """Exception raised when file is locked by another process."""
    pass


class DataIntegrityError(PersistenceError):
    """Exception raised when data validation fails."""
    pass


class CircuitPersistence:
    """
    Handles robust file I/O operations for circuit data.
    
    Features:
    - Atomic writes using temporary files
    - Optional file locking
    - Data validation before write
    - Automatic backups
    - Retry logic for transient failures
    """
    
    def __init__(
        self, 
        enable_backups: bool = True,
        backup_suffix: str = ".backup",
        max_retries: int = 3,
        retry_delay: float = 0.1
    ):
        """
        Initialize persistence handler.
        
        Args:
            enable_backups: Create backup before overwriting files
            backup_suffix: Suffix for backup files
            max_retries: Maximum retry attempts for transient errors
            retry_delay: Delay between retries in seconds
        """
        self.enable_backups = enable_backups
        self.backup_suffix = backup_suffix
        self.max_retries = max_retries
        self.retry_delay = retry_delay
    
    def load_circuit(
        self, 
        file_path: str,
        validate: Optional[Callable[[Dict], bool]] = None
    ) -> Dict[str, Any]:
        """
        Load circuit data from file with error handling.
        
        Args:
            file_path: Path to circuit file
            validate: Optional validation function for loaded data
            
        Returns:
            Circuit data dictionary
            
        Raises:
            PersistenceError: If file cannot be read
            DataIntegrityError: If validation fails
        """
        path = Path(file_path).resolve()
        
        if not path.exists():
            raise PersistenceError(f"File not found: {path}")
        
        if not path.is_file():
            raise PersistenceError(f"Not a file: {path}")
        
        # Retry logic for transient errors
        last_error = None
        for attempt in range(self.max_retries):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Validate data if validator provided
                if validate and not validate(data):
                    raise DataIntegrityError(f"Data validation failed for {path}")
                
                return data
                
            except json.JSONDecodeError as e:
                raise PersistenceError(f"Invalid JSON in {path}: {e}")
            
            except (IOError, OSError) as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                continue
        
        # All retries failed
        raise PersistenceError(f"Failed to read {path} after {self.max_retries} attempts: {last_error}")
    
    def save_circuit(
        self,
        file_path: str,
        data: Dict[str, Any],
        validate: Optional[Callable[[Dict], bool]] = None,
        create_backup: Optional[bool] = None
    ) -> None:
        """
        Save circuit data to file atomically with optional backup.
        
        Args:
            file_path: Path to save circuit file
            data: Circuit data dictionary
            validate: Optional validation function before save
            create_backup: Override instance backup setting
            
        Raises:
            PersistenceError: If file cannot be written
            DataIntegrityError: If validation fails
        """
        path = Path(file_path).resolve()
        
        # Validate data before writing
        if validate and not validate(data):
            raise DataIntegrityError(f"Data validation failed before saving to {path}")
        
        # Create parent directories if needed
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Determine if we should create backup
        should_backup = create_backup if create_backup is not None else self.enable_backups
        
        # Create backup if file exists
        if should_backup and path.exists():
            self._create_backup(path)
        
        # Atomic write using temporary file
        self._atomic_write(path, data)
    
    def _atomic_write(self, path: Path, data: Dict[str, Any]) -> None:
        """
        Perform atomic write operation.
        
        Writes to a temporary file first, then renames to target.
        This ensures the target file is never in a partially written state.
        """
        # Create temporary file in same directory for atomic rename
        temp_fd, temp_path = tempfile.mkstemp(
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp"
        )
        
        temp_file = Path(temp_path)
        
        try:
            # Write to temporary file
            with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                # Ensure data is written to disk
                f.flush()
                os.fsync(f.fileno())
            
            # Atomic rename (POSIX) or replace (Windows)
            # On Windows, need to remove target first if it exists
            if os.name == 'nt' and path.exists():
                # Windows: use replace for atomic operation
                temp_file.replace(path)
            else:
                # POSIX: rename is atomic
                temp_file.rename(path)
            
        except Exception as e:
            # Clean up temp file on error
            try:
                temp_file.unlink(missing_ok=True)
            except:
                pass
            raise PersistenceError(f"Failed to write {path}: {e}")
    
    def _create_backup(self, path: Path) -> Path:
        """
        Create backup of existing file.
        
        Args:
            path: Path to file to backup
            
        Returns:
            Path to backup file
        """
        backup_path = path.with_suffix(path.suffix + self.backup_suffix)
        
        try:
            shutil.copy2(path, backup_path)
            return backup_path
        except Exception as e:
            # Backup failure shouldn't prevent the write
            # Log warning but continue
            print(f"Warning: Failed to create backup of {path}: {e}")
            return None
    
    def verify_file_integrity(self, file_path: str) -> bool:
        """
        Verify file can be read and contains valid JSON.
        
        Args:
            file_path: Path to file to verify
            
        Returns:
            True if file is valid, False otherwise
        """
        try:
            path = Path(file_path).resolve()
            
            if not path.exists() or not path.is_file():
                return False
            
            with open(path, 'r', encoding='utf-8') as f:
                json.load(f)
            
            return True
            
        except Exception:
            return False
    
    def compute_file_hash(self, file_path: str) -> str:
        """
        Compute SHA256 hash of file for integrity checking.
        
        Args:
            file_path: Path to file
            
        Returns:
            Hex digest of file hash
        """
        path = Path(file_path).resolve()
        
        sha256 = hashlib.sha256()
        
        with open(path, 'rb') as f:
            # Read in chunks for large files
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        
        return sha256.hexdigest()
    
    def restore_backup(self, file_path: str) -> bool:
        """
        Restore file from backup.
        
        Args:
            file_path: Path to file to restore
            
        Returns:
            True if backup was restored, False if no backup exists
        """
        path = Path(file_path).resolve()
        backup_path = path.with_suffix(path.suffix + self.backup_suffix)
        
        if not backup_path.exists():
            return False
        
        try:
            shutil.copy2(backup_path, path)
            return True
        except Exception as e:
            raise PersistenceError(f"Failed to restore backup: {e}")


@contextmanager
def safe_file_lock(file_path: str, timeout: float = 5.0):
    """
    Context manager for file locking (simple implementation).
    
    This is a basic implementation using lock files.
    For production use, consider using the 'filelock' package.
    
    Args:
        file_path: Path to file to lock
        timeout: Maximum time to wait for lock
        
    Raises:
        FileLockedError: If lock cannot be acquired
    """
    path = Path(file_path).resolve()
    lock_path = path.with_suffix(path.suffix + '.lock')
    
    start_time = time.time()
    acquired = False
    
    try:
        # Try to acquire lock
        while time.time() - start_time < timeout:
            try:
                # Create lock file exclusively (fails if exists)
                lock_fd = os.open(
                    str(lock_path),
                    os.O_CREAT | os.O_EXCL | os.O_WRONLY
                )
                os.close(lock_fd)
                acquired = True
                break
            except FileExistsError:
                time.sleep(0.01)
        
        if not acquired:
            raise FileLockedError(f"Could not acquire lock for {file_path}")
        
        yield
        
    finally:
        # Release lock
        if acquired:
            try:
                lock_path.unlink(missing_ok=True)
            except:
                pass


# Convenience functions for backward compatibility
def load_circuit_safe(file_path: str) -> Dict[str, Any]:
    """
    Load circuit file with default safety features.
    
    Args:
        file_path: Path to circuit file
        
    Returns:
        Circuit data dictionary
    """
    persistence = CircuitPersistence()
    return persistence.load_circuit(file_path)


def save_circuit_safe(file_path: str, data: Dict[str, Any]) -> None:
    """
    Save circuit file with default safety features.
    
    Args:
        file_path: Path to save circuit file
        data: Circuit data dictionary
    """
    persistence = CircuitPersistence()
    persistence.save_circuit(file_path, data)
