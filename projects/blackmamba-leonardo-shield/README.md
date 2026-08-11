# BlackMamba Leonardo Lab Shield

**Status:** architecture / revision 0.1 planning

The BlackMamba Leonardo Lab Shield is the first physical board built from the converged BlackMamba hardware architecture. It mounts on an Arduino Leonardo and turns the carrier board into a modular laboratory motherboard rather than a collection of loose jumper wires.

## Why Leonardo first

The Leonardo is useful as the first carrier because it gives the project a concrete, inexpensive board on which to prove:

- Native USB host/device interaction through the ATmega32U4 platform.
- A real Board Support Package instead of generic Arduino assumptions.
- Stackable shield mechanics.
- Explicit SPI handling through the board's ICSP topology.
- Servo, sensor and expansion connectors.
- Separation of low-current logic power from actuator power.

This is a proving platform, not a permanent dependency. Future BlackMamba boards should reuse the same capability contracts on other MCUs.

## Revision 0.1 goals

### Core breakout

Expose organized access to:

- Digital I/O.
- Analog inputs.
- I2C.
- UART.
- SPI/ICSP.
- 5 V logic.
- Ground.

### Servo / actuator bank

Provide repeated three-pin connectors using an explicit convention such as:

```text
GND | V_ACT | SIGNAL
```

The final signal pin assignments will be recorded in `pinout.md` after electrical review.

Requirements:

- Clearly keyed/silkscreened polarity.
- Separate actuator power rail.
- Common ground with the logic domain for the non-isolated revision.
- Source-selection mechanism so high-current servo loads do not silently draw through the Leonardo regulator.
- Bulk capacitance near the actuator connector bank.

### Power architecture

Planned domains:

```text
USB / Leonardo supply ──> LOGIC_5V

External actuator input ──> protection ──> ACTUATOR_V

LOGIC_GND ─────────────────────────────── ACTUATOR_GND
                  common reference
```

Revision 0.1 should favor visibility and safety over maximum compactness.

Candidate features for review:

- External 5–6 V actuator input.
- Reverse-polarity protection.
- Fuse or resettable protection.
- Power-present LEDs.
- Logic/actuator rail selection jumper where safe.
- Test points for each rail and ground.

### Expansion

Keep room for:

- PCA9685-class PWM expansion.
- PCF8574-class GPIO expansion.
- Additional I2C modules.
- Motor-driver daughterboards.
- MIDI/DMX/control-surface modules.

The base shield should expose stable buses instead of baking every future function into revision 0.1.

## Architectural inheritance

This board deliberately combines ideas proven in previous BlackMamba repositories:

| Source | Inherited idea |
|---|---|
| `circuit` | Version-controlled circuit definition, validation, BOM, PCB/3D workflow, EMI rules |
| `Arduino` | Capability-oriented buses, adaptive registry, driver model, expansion devices |
| `C-Arduino` | Deterministic embedded core, diagnostics, module lifecycle, host protocol |
| `DronReaper` | Explicit power domains, system decomposition, integrated-PCB discipline |

See `../../docs/BLACKMAMBA_EVOLUTION.md` for the full lineage.

## Planned project files

```text
projects/blackmamba-leonardo-shield/
├── README.md
├── REVISION_HISTORY.md
├── pinout.md
├── power-tree.md
├── connectors.md
├── blackmamba-leonardo-shield.circuit.json
├── bom/
├── schematic/
├── pcb/
├── renders/
└── tests/
```

Only files backed by reviewed design decisions should be added. Placeholders should not masquerade as validated electrical design.

## Revision policy

### v0.1 — laboratory proof board

Primary objective: prove the electrical and software contracts with real hardware.

### v0.2 — measured correction

Changes should be driven by bench measurements, assembly feedback and first-power-on diagnostics.

### v1.0 — stable BlackMamba laboratory carrier

A board reaches 1.0 only after its connector, power, BSP and firmware contracts have survived physical testing.

## Immediate next design decisions

1. Freeze Leonardo mechanical/header footprint.
2. Build the authoritative Leonardo capability/pin map.
3. Define the actuator power input range and current target.
4. Select connector families and pin-order convention.
5. Decide which expansion ICs belong on the base board versus daughterboards.
6. Encode revision 0.1 as `.circuit.json`.
7. Run validation and EMI/power review before PCB layout.
