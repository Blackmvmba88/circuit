# BlackMamba Hardware Evolution

This document records how the BlackMamba electronics stack evolved from several independent experiments into one coherent hardware platform. The goal is consolidation without erasing lineage: each repository remains evidence of a design stage, while the shared architecture inherits the strongest ideas from each one.

## Principle

**Do not rewrite history. Promote proven ideas into shared contracts.**

The BlackMamba hardware ecosystem is not a replacement for the earlier repositories. It is the layer that connects them.

## Evolutionary lineage

### Stage 1 — `circuit`: electronics as version-controlled data

Repository: `Blackmvmba88/circuit`

What it introduced:

- Human-readable `.circuit.json` circuit descriptions.
- Schema and semantic validation.
- Nets, components, board data and design rules as source-controlled artifacts.
- BOM and netlist generation.
- Altium export, with KiCad and other adapters as extensibility targets.
- PCB design checklists and EMI/noise guidance.
- 3D visualization and board/component rendering through Blender.

What becomes canonical:

- `circuit` is the **hardware source-of-truth format and tooling layer**.
- New BlackMamba boards should be representable as version-controlled circuit data.
- Design rules, power domains, connector contracts and physical constraints belong here.

### Stage 2 — `Arduino`: adaptive hardware abstraction

Repository: `Blackmvmba88/Arduino`

What it introduced:

- Hardware discovery and a live hardware registry.
- Unified handling of I2C, SPI, UART, analog and PWM resources.
- Event-driven device lifecycle.
- Persistent configuration and hardware fingerprints.
- Driver management for generic and specific devices.
- A path for expansion devices such as PCA9685 and PCF8574.

What becomes canonical:

- A **board-independent hardware registry**.
- Protocol capabilities described by role instead of scattered pin assumptions.
- Drivers as modular software components.
- Runtime events for device addition, removal and state change.

### Stage 3 — `C-Arduino`: deterministic low-level BlackMamba firmware

Repository: `Blackmvmba88/C-Arduino`

What it introduced:

- A compact BlackMamba firmware core.
- Module lifecycle and message bus.
- Structured serial API.
- Diagnostics, health checks and error recovery.
- Persistent configuration.
- A separation between the embedded runtime and a higher-level master program.

What becomes canonical:

- A **small deterministic firmware substrate** beneath higher-level adaptive behavior.
- Stable wire/API contracts between boards and host software.
- Diagnostics and health state as first-class platform features.
- Explicit module lifecycle rather than ad-hoc setup/loop coupling.

### Stage 4 — `DronReaper`: power and system-level hardware discipline

Repository: `Blackmvmba88/DronReaper`

What it introduced that generalizes beyond the aircraft use case:

- Explicit power-distribution architecture.
- Multiple regulated voltage domains.
- Separation between compute, sensors, communications and high-current loads.
- BOM-oriented hardware documentation.
- Integrated PCB thinking instead of loose breadboard wiring.
- Failsafe-oriented system decomposition.

What becomes canonical:

- Power is a **designed subsystem**, not an afterthought.
- Logic and actuator power domains must be explicit.
- Every board should define power entry, regulation, protection, grounding and load assumptions.
- High-current devices must not silently depend on MCU-board regulator capacity.

## Convergence

The repositories now map into one layered architecture:

```text
BlackMamba product / experiment
            │
            ▼
BlackMamba modules and device roles
            │
            ▼
Adaptive runtime (`Arduino` concepts)
            │
            ▼
Deterministic embedded core (`C-Arduino` concepts)
            │
            ▼
Board Support Package / pin and bus contracts
            │
            ▼
Circuit definition + validation (`circuit`)
            │
            ▼
PCB / connectors / power / physical implementation
```

`DronReaper` contributes system-level power and integration patterns across the lower layers.

## First converged hardware: BlackMamba Leonardo Lab Shield

The Arduino Leonardo / ATmega32U4 is the first concrete carrier targeted by the converged architecture.

The shield is intentionally not a single-purpose controller. It is the first **BlackMamba laboratory motherboard**:

- Stackable on Arduino Leonardo.
- Clear three-pin actuator/sensor connection patterns where appropriate.
- Dedicated logic and actuator power domains.
- Common ground with explicit power-routing rules.
- I2C, UART and analog breakout.
- SPI routed according to Leonardo/ATmega32U4 board topology, including the ICSP header dependency.
- Expansion path for additional PWM/GPIO controllers.
- Test points and diagnostics designed in from revision 0.1.
- Circuit definition, BOM, validation and future PCB artifacts kept together in this repository.

See `projects/blackmamba-leonardo-shield/README.md`.

## Repository policy going forward

1. **Preserve ancestral repositories.** Do not delete or rewrite them solely because their ideas are promoted here.
2. **Promote contracts, not duplicated code.** Shared concepts should gain documented interfaces before code is copied.
3. **Record provenance.** When a subsystem is derived from an earlier repository, state where the idea came from.
4. **Hardware definitions live with `circuit`.** Board schematics, nets, BOM, power trees and physical constraints belong here.
5. **Firmware remains layered.** Low-level deterministic functionality and adaptive orchestration should stay separable.
6. **Every physical revision is traceable.** Board revisions must record electrical changes, firmware compatibility and migration notes.
7. **No hidden power assumptions.** Voltage, current, ground reference and source selection must be documented for each connector.

## Evolution log format

Future architecture changes should append an entry using this structure:

```markdown
### YYYY-MM-DD — Change title

Origin:
- repo / experiment / observation

Inherited idea:
- what proved useful

Promoted contract:
- what becomes shared

Compatibility impact:
- none / additive / breaking

Evidence:
- files, tests, measurements or hardware revision
```

This turns BlackMamba's history into engineering evidence rather than forgotten iterations.
