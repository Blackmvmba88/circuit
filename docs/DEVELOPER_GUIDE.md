# Developer Guide

This guide helps developers contribute to the Circuit project and extend its functionality.

---

## Table of Contents

1. [Development Setup](#development-setup)
2. [Running Tests](#running-tests)
3. [Adding New Validation Rules](#adding-new-validation-rules)
4. [Creating Examples](#creating-examples)
5. [Git Hooks](#git-hooks)
6. [CI/CD Integration](#cicd-integration)

---

## Development Setup

### Prerequisites

- Python 3.7 or higher
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/Blackmvmba88/circuit.git
cd circuit

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Verify Installation

```bash
# Check CLI is working
circuit --version

# Validate an example
circuit validate examples/simple_circuit.circuit.json
```

---

## Running Tests

### Run All Tests

```bash
# Using unittest (no additional dependencies)
python -m unittest discover tests -v

# Run specific test file
python -m unittest tests.test_validator -v
```

### Run Validator Tests Only

```bash
python -m unittest tests.test_validator -v
```

### Run Persistence Tests

```bash
python -m unittest test_persistence -v
```

### Test Coverage

To check test coverage:

```bash
# Install coverage tool
pip install coverage

# Run tests with coverage
coverage run -m unittest discover tests
coverage report
coverage html  # Generate HTML report
```

---

## Adding New Validation Rules

### 1. Update JSON Schema (if structural)

Edit `schema/circuit.schema.json`:

```json
{
  "properties": {
    "new_field": {
      "type": "string",
      "description": "Description of new field"
    }
  }
}
```

### 2. Add Semantic Validation (if logical)

Edit `cli/validator.py`, add to `validate_semantics()`:

```python
def validate_semantics(circuit_data: dict, strict: bool = False) -> Tuple[List[str], List[str]]:
    errors = []
    warnings = []
    
    # ... existing validation ...
    
    # Add your new validation rule
    if 'new_field' in circuit_data:
        value = circuit_data['new_field']
        if not value.startswith('prefix_'):
            errors.append("new_field must start with 'prefix_'")
    
    return errors, warnings
```

### 3. Add Tests

Edit `tests/test_validator.py`:

```python
def test_new_validation_rule(self):
    """Test that new validation rule works."""
    circuit = {
        "version": "1.0",
        "metadata": {"name": "Test"},
        "components": [{"id": "R1", "type": "resistor"}],
        "new_field": "invalid_value"
    }
    file_path = self._create_temp_circuit(circuit)
    is_valid, errors, warnings = validate_circuit_file(file_path)
    self.assertFalse(is_valid)
    self.assertTrue(any("prefix_" in err for err in errors))
```

### 4. Update Documentation

Edit `docs/VALIDATION_RULES.md` to document the new rule:

```markdown
### Rule N: New Validation Rule

**Requirement:** Description of the rule

**Error:** "Error message pattern"

**Example:**
...
```

### 5. Run Tests

```bash
python -m unittest tests.test_validator -v
```

---

## Creating Examples

### Example Template

Create a new file `examples/your_circuit.circuit.json`:

```json
{
  "version": "1.0",
  "metadata": {
    "name": "Your Circuit Name",
    "description": "Description of what this circuit does",
    "author": "Your Name",
    "created": "2026-02-06",
    "tags": ["tag1", "tag2"]
  },
  "components": [
    {
      "id": "R1",
      "type": "resistor",
      "value": "10K",
      "params": {
        "resistance_ohm": 10000,
        "power_rating_w": 0.125
      }
    }
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
```

### Validate Your Example

```bash
circuit validate examples/your_circuit.circuit.json
```

### Add to CI

Examples are automatically validated by GitHub Actions. Just ensure the file is in the `examples/` directory.

---

## Git Hooks

### Pre-Commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Pre-commit hook to validate circuit files

echo "🔍 Validating circuit files before commit..."

# Find all staged .circuit.json files
staged_files=$(git diff --cached --name-only --diff-filter=ACM | grep '.circuit.json$')

if [ -z "$staged_files" ]; then
  echo "No circuit files to validate"
  exit 0
fi

# Validate each file
exit_code=0
for file in $staged_files; do
  if [ -f "$file" ]; then
    echo "Validating: $file"
    if python -m cli.main validate "$file"; then
      echo "✅ $file passed validation"
    else
      echo "❌ $file failed validation"
      exit_code=1
    fi
  fi
done

if [ $exit_code -eq 0 ]; then
  echo "✅ All circuit files validated successfully"
else
  echo "❌ Some circuit files failed validation"
  echo "Fix the errors and try again, or use 'git commit --no-verify' to skip validation"
fi

exit $exit_code
```

Make it executable:

```bash
chmod +x .git/hooks/pre-commit
```

### Pre-Push Hook

Create `.git/hooks/pre-push`:

```bash
#!/bin/bash
# Pre-push hook to run tests

echo "🧪 Running tests before push..."

# Run validator tests
if ! python -m unittest tests.test_validator -v; then
  echo "❌ Tests failed"
  exit 1
fi

echo "✅ All tests passed"
exit 0
```

Make it executable:

```bash
chmod +x .git/hooks/pre-push
```

---

## CI/CD Integration

### GitHub Actions

The project uses GitHub Actions for continuous integration. The workflow is defined in `.github/workflows/ci.yml`.

**Triggered on:**
- Push to `main`, `develop`, or `copilot/**` branches
- Pull requests to `main` or `develop`
- Manual workflow dispatch

**Jobs:**
1. **validate-circuits** - Validates all example circuits
2. **run-tests** - Runs the test suite
3. **test-adapters** - Tests export adapters
4. **lint-python** - Lints Python code
5. **validate-schema** - Validates JSON schema
6. **build-docs** - Checks documentation
7. **security-scan** - Runs security scans
8. **summary** - Provides overall status

### Local CI Simulation

Run the same checks locally:

```bash
# Validate all examples
for file in examples/*.circuit.json; do
  python circuit validate "$file"
done

# Run tests
python -m unittest discover tests -v

# Test exports
mkdir -p test_exports
python circuit export examples/simple_circuit.circuit.json --format altium --output test_exports/

# Lint code
pip install flake8
flake8 cli/ adapters/ --max-line-length=127
```

---

## Common Development Tasks

### Adding a New Component Type

1. Edit `schema/circuit.schema.json`:
```json
{
  "type": {
    "enum": [
      "resistor",
      "capacitor",
      "your_new_type",  // Add here
      "..."
    ]
  }
}
```

2. Add example circuit using the new type

3. Update documentation in `docs/FORMAT_SPECIFICATION.md`

### Adding a New Export Format

1. Create adapter in `adapters/your_format.py`:

```python
def export_to_your_format(circuit_data: dict, output_dir: str):
    """Export circuit to your format."""
    # Implementation
    pass
```

2. Register in `cli/exporter.py`:

```python
EXPORT_FORMATS = {
    'altium': export_to_altium,
    'your_format': export_to_your_format,  # Add here
}
```

3. Add tests

4. Update documentation

---

## Best Practices

### Code Style

- Follow PEP 8 style guide
- Use type hints where possible
- Add docstrings to functions
- Keep functions focused and small

### Testing

- Write tests for all new features
- Aim for >80% code coverage
- Test both success and failure cases
- Use descriptive test names

### Documentation

- Update docs when adding features
- Include examples in documentation
- Keep README.md up to date
- Document validation rules

### Git Workflow

- Create feature branches
- Write clear commit messages
- Keep commits focused
- Squash before merging

---

## Getting Help

- **Issues**: https://github.com/Blackmvmba88/circuit/issues
- **Discussions**: https://github.com/Blackmvmba88/circuit/discussions
- **Contributing Guide**: [CONTRIBUTING.md](../CONTRIBUTING.md)

---

**Happy coding! 🚀**
