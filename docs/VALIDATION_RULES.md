# Circuit Validation Rules

**Version:** 1.0  
**Last Updated:** 2026-02-06

This document provides a comprehensive reference for all validation rules applied to `.circuit.json` files.

---

## Table of Contents

1. [Overview](#overview)
2. [JSON Schema Validation](#json-schema-validation)
3. [Semantic Validation Rules](#semantic-validation-rules)
4. [Component Validation](#component-validation)
5. [Connectivity Validation](#connectivity-validation)
6. [Error Messages Reference](#error-messages-reference)
7. [Validation Modes](#validation-modes)

---

## Overview

Circuit files undergo two levels of validation:

1. **Schema Validation**: Structural validation against the JSON Schema
2. **Semantic Validation**: Logical consistency checks beyond schema

The validator is available via CLI:

```bash
# Basic validation
circuit validate mycircuit.circuit.json

# Strict mode (additional warnings)
circuit validate mycircuit.circuit.json --strict
```

---

## JSON Schema Validation

### Required Fields

At the root level, these fields are **required**:
- `version` - Format version (e.g., "1.0")
- `metadata` - Circuit metadata object
- `components` - Array of components (minimum 1)

### Version Format

**Rule:** Version must match pattern `^\d+\.\d+$`

**Valid:**
```json
"version": "1.0"
"version": "2.1"
```

**Invalid:**
```json
"version": "1"        // Missing minor version
"version": "v1.0"     // Extra characters
"version": "1.0.0"    // Too many parts
```

### Metadata Requirements

**Required fields:**
- `name` (string, minimum length: 1)

**Optional fields:**
- `description` (string)
- `author` (string)
- `version` (string)
- `created` (string, pattern: YYYY-MM-DD)
- `modified` (string, pattern: YYYY-MM-DD)
- `tags` (array of strings)
- `license` (string)

**Date format:** YYYY-MM-DD or ISO 8601

**Example:**
```json
{
  "metadata": {
    "name": "My Circuit",
    "created": "2024-01-15",
    "modified": "2024-06-20"
  }
}
```

### Component Requirements

**Required for each component:**
- `id` (string, pattern: `^[A-Za-z][A-Za-z0-9_]*$`)
- `type` (string, must be one of the allowed types)

**Component ID pattern:**
- Must start with a letter
- Can contain letters, numbers, and underscores
- Examples: `R1`, `LED_STATUS`, `U1A`

**Allowed component types:**
```
resistor, capacitor, inductor, diode, led, transistor,
ic, connector, switch, relay, transformer, crystal,
fuse, battery, power_supply, ground, test_point,
mounting_hole, jumper, header, socket, potentiometer,
varistor, thermistor, photodiode, optocoupler, display,
buzzer, speaker, microphone, motor, sensor, antenna,
oscillator, voltage_regulator, bridge_rectifier, other
```

### Parameter Validation

Numeric parameters must satisfy minimum constraints:

| Parameter | Type | Constraint |
|-----------|------|------------|
| `resistance_ohm` | number | ≥ 0 |
| `capacitance_f` | number | ≥ 0 |
| `inductance_h` | number | ≥ 0 |
| `voltage_rating_v` | number | ≥ 0 |
| `current_rating_a` | number | ≥ 0 |
| `power_rating_w` | number | ≥ 0 |

---

## Semantic Validation Rules

These rules check logical consistency beyond schema structure.

### Rule 1: Unique Component IDs

**Requirement:** Each component ID must be unique within the circuit.

**Error:** "Duplicate component ID: {id}"

**Example violation:**
```json
{
  "components": [
    {"id": "R1", "type": "resistor"},
    {"id": "R1", "type": "capacitor"}  // ERROR: Duplicate R1
  ]
}
```

### Rule 2: Connection Component References

**Requirement:** All components referenced in connections must exist in the components array or be special components (VCC, GND, POWER, GROUND).

**Error:** "Connection references non-existent component: {id}"

**Special components** (allowed without definition):
- `VCC`
- `GND`
- `POWER`
- `GROUND`

**Example:**
```json
{
  "components": [
    {"id": "R1", "type": "resistor"}
  ],
  "connections": [
    {"from": "VCC", "to": "R1.1"},      // OK: VCC is special
    {"from": "R1.2", "to": "R2.1"}      // ERROR: R2 doesn't exist
  ]
}
```

### Rule 3: Net Component References

**Requirement:** All components referenced in nets must exist in the components array.

**Error:** "Net '{net_id}' references non-existent component: {component_id}"

**Example:**
```json
{
  "components": [
    {"id": "R1", "type": "resistor"}
  ],
  "nets": [
    {
      "id": "NET1",
      "connections": [
        {"component": "R1", "pin": "1"},
        {"component": "R2", "pin": "1"}  // ERROR: R2 doesn't exist
      ]
    }
  ]
}
```

### Rule 4: Unique Net IDs

**Requirement:** Each net ID must be unique within the circuit.

**Error:** "Duplicate net ID: {id}"

**Example violation:**
```json
{
  "nets": [
    {"id": "NET1", "connections": [...]},
    {"id": "NET1", "connections": [...]}  // ERROR: Duplicate NET1
  ]
}
```

### Rule 5: Minimum Net Connections

**Requirement:** Each net should have at least 2 connections.

**Warning:** "Net '{net_id}' has fewer than 2 connections"

**Rationale:** A net with only 1 connection serves no electrical purpose.

**Example:**
```json
{
  "nets": [
    {
      "id": "SIGNAL",
      "connections": [
        {"component": "R1", "pin": "1"}  // WARNING: Only 1 connection
      ]
    }
  ]
}
```

### Rule 6: Positive Resistance Values

**Requirement:** Resistance values must be positive (> 0).

**Error:** "Component '{id}': resistance must be positive"

**Example:**
```json
{
  "id": "R1",
  "type": "resistor",
  "params": {
    "resistance_ohm": -100  // ERROR: Negative resistance
  }
}
```

### Rule 7: Positive Capacitance Values

**Requirement:** Capacitance values must be positive (> 0).

**Error:** "Component '{id}': capacitance must be positive"

**Example:**
```json
{
  "id": "C1",
  "type": "capacitor",
  "params": {
    "capacitance_f": -0.000001  // ERROR: Negative capacitance
  }
}
```

### Rule 8: Positive Voltage Ratings

**Requirement:** Voltage ratings must be positive (> 0).

**Error:** "Component '{id}': voltage rating must be positive"

**Example:**
```json
{
  "id": "C1",
  "type": "capacitor",
  "params": {
    "voltage_rating_v": -25  // ERROR: Negative voltage rating
  }
}
```

---

## Component Validation

### Component ID Validation

**Pattern:** `^[A-Za-z][A-Za-z0-9_]*$`

**Valid IDs:**
- `R1`
- `LED_STATUS`
- `U1`
- `IC_MAIN`
- `Q2A`

**Invalid IDs:**
- `1R` - Starts with number
- `R-1` - Contains hyphen
- `R 1` - Contains space
- `_R1` - Starts with underscore

### Component Type Validation

**Rule:** Component type must be from the allowed enum list.

**Error:** Schema validation error

**Recommendation:** Use `"other"` for custom component types not in the standard list.

---

## Connectivity Validation

### Point-to-Point Connections

**Format:** `"ComponentID.pin"`

**Examples:**
- `R1.1` - Component R1, pin 1
- `LED1.anode` - Component LED1, anode pin
- `VCC` - Special component (no pin needed)
- `GND` - Special component (no pin needed)

### Net Connections

**Required fields:**
- `component` - Component ID
- `pin` - Pin identifier (string or number)

**Example:**
```json
{
  "component": "U1",
  "pin": "8"
}
```

---

## Error Messages Reference

### Schema Validation Errors

| Error Pattern | Meaning |
|---------------|---------|
| `'version' is a required property` | Missing version field |
| `'metadata' is a required property` | Missing metadata field |
| `'components' is a required property` | Missing components array |
| `[] is too short` | Components array is empty |
| `'invalid_type' is not one of [...]` | Invalid component type |
| `'...' does not match '^\\d+\\.\\d+$'` | Invalid version format |

### Semantic Validation Errors

| Error Pattern | Meaning |
|---------------|---------|
| `Duplicate component ID: {id}` | Component ID used more than once |
| `Connection references non-existent component: {id}` | Connection to undefined component |
| `Net '{net}' references non-existent component: {id}` | Net connection to undefined component |
| `Duplicate net ID: {id}` | Net ID used more than once |
| `Component '{id}': resistance must be positive` | Negative resistance value |
| `Component '{id}': capacitance must be positive` | Negative capacitance value |
| `Component '{id}': voltage rating must be positive` | Negative voltage rating |

### Warnings

| Warning Pattern | Meaning |
|-----------------|---------|
| `Net '{net}' has fewer than 2 connections` | Net with only 1 connection point |
| `Component '{id}' is not connected to any net` | Unconnected component (strict mode only) |

---

## Validation Modes

### Standard Mode

```bash
circuit validate mycircuit.circuit.json
```

Checks:
- ✅ JSON syntax
- ✅ Schema validation
- ✅ Component ID uniqueness
- ✅ Connection references
- ✅ Net references
- ✅ Parameter constraints

### Strict Mode

```bash
circuit validate mycircuit.circuit.json --strict
```

Additional checks:
- ✅ All standard mode checks
- ⚠️ Unconnected components warning

**Note:** Power supplies and ground components are exempt from unconnected warnings.

---

## Validation Workflow

```
┌─────────────────────────┐
│ Load circuit file       │
└──────────┬──────────────┘
           │
           v
┌─────────────────────────┐
│ Parse JSON              │
└──────────┬──────────────┘
           │
           v
┌─────────────────────────┐
│ Schema Validation       │
│ - Required fields       │
│ - Field types           │
│ - Value constraints     │
└──────────┬──────────────┘
           │
           v
┌─────────────────────────┐
│ Semantic Validation     │
│ - Unique IDs            │
│ - Reference integrity   │
│ - Logical consistency   │
└──────────┬──────────────┘
           │
           v
┌─────────────────────────┐
│ Report Results          │
│ - Errors (if any)       │
│ - Warnings (if any)     │
│ - Success message       │
└─────────────────────────┘
```

---

## Best Practices

### 1. Validate Early and Often

Run validation:
- Before committing changes
- In CI/CD pipelines
- After manual edits

### 2. Fix Errors Before Warnings

- Errors prevent the circuit from being valid
- Warnings indicate potential issues

### 3. Use Strict Mode for Production

```bash
circuit validate production.circuit.json --strict
```

### 4. Integrate with Git Hooks

Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
for file in *.circuit.json; do
  circuit validate "$file" || exit 1
done
```

### 5. Automate in CI

GitHub Actions example:
```yaml
- name: Validate circuits
  run: |
    for file in examples/*.circuit.json; do
      circuit validate "$file"
    done
```

---

## Future Validation Rules

Planned for future versions:

1. **Pin validation**: Verify that referenced pins exist on components
2. **Net naming conventions**: Check for reserved names
3. **Value unit consistency**: Ensure units match parameter types
4. **Cross-component validation**: Check voltage compatibility
5. **Design rule checks**: PCB-specific constraints
6. **Electrical rules checking**: KCL/KVL validation

---

**Copyright © 2026 Circuit Project Contributors**  
**License:** MIT
