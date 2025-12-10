# Circuit Format Specification v1.0

**Status:** Draft  
**Version:** 1.0  
**Last Updated:** 2024-12-08  
**Authors:** Circuit Project Contributors

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Format Overview](#2-format-overview)
3. [File Format](#3-file-format)
4. [Metadata](#4-metadata)
5. [Components](#5-components)
6. [Connectivity](#6-connectivity)
7. [Board Specifications](#7-board-specifications)
8. [Design Rules](#8-design-rules)
9. [Validation](#9-validation)
10. [Best Practices](#10-best-practices)
11. [Examples](#11-examples)

---

## 1. Introduction

### 1.1 Purpose

The Circuit format (`.circuit.json`) is a universal, human-readable JSON-based format for describing electronic circuits and printed circuit board (PCB) designs. It aims to provide:

- **Interoperability** between different EDA tools
- **Version control** compatibility with Git and other VCS
- **Human readability** for manual editing and review
- **Machine parsability** for automated tooling

### 1.2 Goals

- Provide a standardized way to represent electronic circuits
- Enable collaboration using standard software development workflows
- Support both simple and complex circuit designs
- Facilitate automated validation and testing
- Enable conversion to/from various EDA tool formats

### 1.3 Scope

This specification covers:
- Circuit schematic representation
- Component definitions
- Connectivity (nets and connections)
- PCB layout information
- Design rules and constraints
- Metadata and documentation

Out of scope:
- Detailed PCB routing paths
- Manufacturing-specific data (Gerber files)
- Simulation models (SPICE syntax)

---

## 2. Format Overview

### 2.1 File Extension

Circuit files **MUST** use the `.circuit.json` extension.

Example: `my_circuit.circuit.json`

### 2.2 Encoding

Files **MUST** be encoded in UTF-8.

### 2.3 MIME Type

Recommended MIME type: `application/vnd.circuit+json`

### 2.4 JSON Schema

The format is formally defined by a JSON Schema available at:
`schema/circuit.schema.json`

---

## 3. File Format

### 3.1 Root Structure

A circuit file is a JSON object with the following required top-level properties:

```json
{
  "version": "1.0",
  "metadata": { ... },
  "components": [ ... ]
}
```

### 3.2 Required Properties

- `version` (string): Format version number (e.g., "1.0")
- `metadata` (object): Circuit metadata
- `components` (array): List of electronic components

### 3.3 Optional Properties

- `connections` (array): Point-to-point connections (deprecated, use `nets`)
- `nets` (array): Electrical nets
- `board` (object): PCB board specifications
- `design_rules` (object): Design rules and constraints
- `properties` (object): Circuit properties
- `notes` (array): General circuit notes
- `sim_config` (object): Simulation configuration
- `blender_generation` (object): 3D rendering configuration

---

## 4. Metadata

### 4.1 Structure

The `metadata` object **MUST** contain at minimum:

```json
{
  "metadata": {
    "name": "Circuit Name"
  }
}
```

### 4.2 Standard Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Human-readable circuit name |
| `description` | string | No | Circuit description |
| `author` | string | No | Author name or organization |
| `version` | string | No | Circuit design version |
| `created` | string | No | Creation date (YYYY-MM-DD or ISO 8601) |
| `modified` | string | No | Last modification date |
| `tags` | array | No | Categorization tags |
| `license` | string | No | License (e.g., "MIT", "CC-BY-SA") |

### 4.3 Example

```json
{
  "metadata": {
    "name": "USB-C Power Delivery Controller",
    "description": "5V/3A USB-C PD sink with automatic negotiation",
    "author": "Jane Doe",
    "version": "2.1",
    "created": "2024-01-15",
    "modified": "2024-06-20",
    "tags": ["usb-c", "power", "pd"],
    "license": "MIT"
  }
}
```

---

## 5. Components

### 5.1 Component Definition

Each component is defined as an object in the `components` array.

**Required fields:**
- `id` (string): Unique component identifier
- `type` (string): Component type

**Optional fields:**
- `package` (string): Physical package/footprint
- `value` (string): Component value
- `description` (string): Human-readable description
- `params` (object): Component-specific parameters
- `pins` (object): Pin definitions
- `model_3d` (object): 3D model information
- `notes` (string): Design notes

### 5.2 Component ID

Component IDs **MUST**:
- Be unique within the circuit
- Start with a letter
- Contain only alphanumeric characters and underscores
- Follow standard reference designator conventions

**Standard prefixes:**
- `R` - Resistor (R1, R2, ...)
- `C` - Capacitor (C1, C2, ...)
- `L` - Inductor (L1, L2, ...)
- `D` - Diode (D1, D2, ...)
- `Q` - Transistor (Q1, Q2, ...)
- `U` - Integrated Circuit (U1, U2, ...)
- `J` - Connector (J1, J2, ...)
- `LED` - LED (LED1, LED2, ...)
- `SW` - Switch (SW1, SW2, ...)

### 5.3 Component Types

Standard component types (enum):

```
resistor, capacitor, inductor, diode, led, transistor, ic, connector,
switch, relay, transformer, crystal, fuse, battery, power_supply,
ground, test_point, mounting_hole, jumper, header, socket,
potentiometer, varistor, thermistor, photodiode, optocoupler,
display, buzzer, speaker, microphone, motor, sensor, antenna,
oscillator, voltage_regulator, bridge_rectifier, other
```

### 5.4 Component Parameters

The `params` object contains component-specific technical parameters:

**Common parameters:**
- `resistance_ohm` (number): Resistance in ohms
- `capacitance_f` (number): Capacitance in farads
- `inductance_h` (number): Inductance in henries
- `voltage_rating_v` (number): Voltage rating in volts
- `current_rating_a` (number): Current rating in amps
- `power_rating_w` (number): Power rating in watts
- `tolerance` (string): Tolerance (e.g., "5%", "1%")
- `manufacturer` (string): Manufacturer name
- `part_number` (string): Manufacturer part number
- `datasheet_url` (string): URL to datasheet

### 5.5 Component Example

```json
{
  "id": "R1",
  "type": "resistor",
  "package": "0805",
  "value": "10K",
  "description": "Pull-up resistor",
  "params": {
    "resistance_ohm": 10000,
    "power_rating_w": 0.125,
    "tolerance": "1%",
    "manufacturer": "Yageo",
    "part_number": "RC0805FR-0710KL"
  },
  "pins": {
    "1": { "net": "VCC" },
    "2": { "net": "SIGNAL" }
  }
}
```

---

## 6. Connectivity

### 6.1 Nets vs Connections

Two methods are supported for defining connectivity:

1. **Nets** (preferred): Multi-point electrical nets
2. **Connections** (deprecated): Point-to-point connections

### 6.2 Nets

Nets represent electrical connections between multiple component pins.

**Structure:**

```json
{
  "nets": [
    {
      "id": "VCC",
      "name": "VCC",
      "connections": [
        { "component": "U1", "pin": "8" },
        { "component": "C1", "pin": "1" },
        { "component": "R1", "pin": "1" }
      ],
      "design_notes": "Power rail - use wide traces"
    }
  ]
}
```

**Required fields:**
- `id` (string): Unique net identifier
- `connections` (array): List of connected pins (minimum 2)

**Connection object:**
- `component` (string): Component ID
- `pin` (string/number): Pin identifier

### 6.3 Point-to-Point Connections (Deprecated)

```json
{
  "connections": [
    {
      "from": "VCC.positive",
      "to": "R1.1",
      "notes": "Power connection"
    }
  ]
}
```

**Note:** Use nets instead for better representation of multi-point connections.

### 6.4 Pin Naming Conventions

Pins can be identified by:
- **Number**: `"1"`, `"2"`, `"14"`
- **Name**: `"VCC"`, `"GND"`, `"anode"`, `"cathode"`
- **Function**: `"input"`, `"output"`, `"enable"`

---

## 7. Board Specifications

### 7.1 Board Object

PCB-specific information:

```json
{
  "board": {
    "dimensions": {
      "width": 100,
      "height": 80,
      "thickness": 1.6
    },
    "layers": 2,
    "material": "FR4",
    "finish": "HASL"
  }
}
```

### 7.2 Dimensions

- **Units**: Millimeters (mm)
- `width`: Board width
- `height`: Board height  
- `thickness`: Board thickness (standard: 1.6mm)

### 7.3 Standard Values

**Layers:** 1, 2, 4, 6, 8, 10, ...

**Materials:**
- FR4 (most common)
- CEM-1
- CEM-3
- Aluminum
- Rogers

**Finishes:**
- HASL (Hot Air Solder Leveling)
- ENIG (Electroless Nickel Immersion Gold)
- OSP (Organic Solderability Preservative)
- Immersion Silver
- Immersion Tin

---

## 8. Design Rules

### 8.1 EMI Compliance

```json
{
  "design_rules": {
    "emi_compliance": {
      "standard": "FCC Part 15 Class B",
      "decoupling_strategy": "100nF within 5mm of each IC",
      "ground_plane": "Continuous on bottom layer",
      "trace_spacing_mm": 0.2,
      "power_trace_width_mm": 0.5
    }
  }
}
```

### 8.2 Thermal Management

```json
{
  "thermal": {
    "max_ambient_temp_c": 70,
    "max_junction_temp_c": 125,
    "heatsink_required": true
  }
}
```

---

## 9. Validation

### 9.1 Schema Validation

All circuit files **MUST** validate against the JSON Schema:
`schema/circuit.schema.json`

### 9.2 Semantic Validation

Additional semantic rules:
1. Component IDs must be unique
2. Net connections must reference existing components
3. Each net must have at least 2 connections
4. Numeric values must be positive (resistance, capacitance, etc.)

### 9.3 CLI Validation

```bash
circuit validate mycircuit.circuit.json
```

---

## 10. Best Practices

### 10.1 Naming Conventions

- Use descriptive component IDs: `LED_POWER` instead of `LED1`
- Use meaningful net names: `VCC_5V`, `GND`, `I2C_SDA`
- Include units in values: `"10K"`, `"100nF"`, `"5V"`

### 10.2 Documentation

- Add `notes` arrays to document complex circuits
- Use `design_notes` on nets for routing guidelines
- Include manufacturer part numbers for production

### 10.3 Version Control

- Use meaningful commit messages
- Tag releases with semantic versioning
- Review circuit changes in PRs like code

---

## 11. Examples

See the `examples/` directory for reference implementations:

- `simple_circuit.circuit.json` - Basic LED circuit
- `circuit_with_3d.circuit.json` - Circuit with 3D models
- `voltage_regulator_lm7805.circuit.json` - Linear voltage regulator
- `h_bridge_motor_driver.circuit.json` - H-bridge motor driver

---

## Appendix A: JSON Schema

See `schema/circuit.schema.json` for the complete formal specification.

## Appendix B: Change Log

### Version 1.0 (2024-12-08)
- Initial specification
- Component types defined
- Net and connection formats
- Board specifications
- Design rules structure

---

**Copyright © 2024 Circuit Project Contributors**  
**License:** MIT
