# Revision History — BlackMamba Leonardo Lab Shield

This log records both physical revisions and architecture decisions that materially affect the board.

## 2026-08-10 — v0.1 architecture begins

**Origin**

Observation while working directly with an Arduino Leonardo: the 2x3 ICSP header highlighted how much easier hardware becomes when connectors are organized around actual functions instead of exposing raw MCU pins without a laboratory-oriented interface.

**Inherited ideas**

- From `circuit`: circuit-as-data, validation, BOM/netlist workflow, EMI review and 3D visualization.
- From `Arduino`: protocol abstraction, hardware registry, driver model and expansion strategy.
- From `C-Arduino`: deterministic embedded core, module lifecycle, diagnostics and host communication.
- From `DronReaper`: explicit power domains and integrated-PCB/system decomposition.

**Promoted contracts**

- `circuit` becomes the hardware source-of-truth layer.
- Arduino Leonardo / ATmega32U4 becomes the first Board Support Package target.
- The shield is defined as a laboratory motherboard, not a single-purpose accessory.
- Logic and actuator power are separate named domains.
- Servo/actuator connectors use an explicit ground/power/signal contract.
- SPI access must respect Leonardo's ICSP topology rather than assuming Uno-style pin placement.
- Future BlackMamba modules consume named capabilities instead of assuming one MCU pinout.

**Compatibility impact**

Additive. Existing repositories remain intact and continue to document their original evolutionary stages.

**Evidence / artifacts**

- `docs/BLACKMAMBA_EVOLUTION.md`
- `docs/BLACKMAMBA_ECOSYSTEM_ARCHITECTURE.md`
- `projects/blackmamba-leonardo-shield/README.md`

**Next evidence required**

- Authoritative Leonardo pin/capability map.
- Measured/selected actuator power target.
- Connector selection.
- First `.circuit.json` definition.
- Electrical validation before PCB layout.
