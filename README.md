# Circuit

**A universal format for describing electronic circuits and logic designs**

## Overview

Circuit is an open-source project that aims to create a universal, human-readable format for describing electronic circuits and logic designs. The goal is to provide a standardized way to represent circuits that can be:

- **Portable**: Work across different tools and platforms
- **Version-controllable**: Track circuit changes with Git
- **Human-readable**: Easy to understand and edit manually
- **Machine-friendly**: Simple to parse and validate

## Vision

We envision a world where electronic circuit designs are as easy to share, collaborate on, and version-control as software code. Circuit aims to bridge the gap between visual circuit design tools and text-based workflows, enabling:

- Collaboration on circuit designs using standard Git workflows
- CI/CD pipelines for circuit validation and testing
- Interoperability between different EDA (Electronic Design Automation) tools
- Educational resources that are accessible and easy to understand

## The .circuit.json Format

Circuit files use the `.circuit.json` extension and follow a simple JSON schema that describes:

- **Components**: Electronic parts (resistors, capacitors, ICs, etc.)
- **Connections**: How components are wired together
- **Metadata**: Project information, version, author, etc.

### Example

```json
{
  "version": "1.0",
  "metadata": {
    "name": "Simple LED Circuit",
    "description": "A basic LED circuit with a resistor"
  },
  "components": [
    {
      "id": "R1",
      "type": "resistor",
      "value": "220Ω"
    },
    {
      "id": "LED1",
      "type": "led",
      "color": "red"
    }
  ],
  "connections": [
    {
      "from": "VCC",
      "to": "R1.1"
    },
    {
      "from": "R1.2",
      "to": "LED1.anode"
    },
    {
      "from": "LED1.cathode",
      "to": "GND"
    }
  ]
}
```

## Getting Started

### For Users

1. Browse the [examples/](examples/) directory to see sample circuits
2. Try creating your own `.circuit.json` files
3. Share feedback and suggestions via [Issues](../../issues)

### For Contributors

We welcome contributions! Whether you're interested in:

- Defining the circuit format specification
- Building tooling (validators, converters, visualizers)
- Creating adapters for popular EDA tools
- Writing documentation and examples

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to get involved.

## Roadmap

Check out our [ROADMAP.md](ROADMAP.md) for planned features and milestones.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Community

- **Issues**: Report bugs or request features via [GitHub Issues](../../issues)
- **Discussions**: Join conversations in [GitHub Discussions](../../discussions)
- **Code of Conduct**: Please read our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## Status

⚠️ **This project is in early development.** The format specification and tooling are still evolving. We encourage early feedback and contributions!
