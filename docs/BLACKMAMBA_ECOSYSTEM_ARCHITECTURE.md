# BlackMamba Hardware Ecosystem Architecture

## Purpose

Define one architecture that lets BlackMamba boards, firmware and modules evolve independently without becoming disconnected projects again.

## Architectural layers

### 1. Physical layer

Owns:

- PCB geometry and stack-up.
- Connectors and pin numbering.
- Power entry and regulation.
- Protection, grounding and decoupling.
- Test points.
- Mechanical constraints.

Canonical tooling: `circuit` plus EDA exports.

### 2. Board Support Package (BSP)

Owns:

- MCU/board identity.
- Pin capabilities.
- Bus availability.
- Electrical limits.
- Board-specific routing exceptions.

A BSP translates physical resources into stable names used by the firmware.

Example capability names:

```text
BUS_I2C_PRIMARY
BUS_SPI_PRIMARY
UART_HOST
PWM_SERVO_0
PWM_SERVO_1
ADC_0
POWER_LOGIC_5V
POWER_ACTUATOR_EXT
```

Application code should prefer capabilities over hard-coded pin numbers.

### 3. Deterministic embedded core

Inherited primarily from `C-Arduino`.

Owns:

- Boot and initialization.
- Error codes and recovery.
- Module lifecycle.
- Message/event transport.
- Diagnostics and health state.
- Stable host communication protocol.

This layer must remain small enough to reason about on constrained hardware.

### 4. Adaptive runtime

Inherited primarily from `Arduino`.

Owns:

- Hardware registry.
- Protocol handlers.
- Device discovery where electrically safe and technically possible.
- Driver selection.
- Persistent hardware fingerprints/configuration.
- Higher-level device events.

The adaptive layer may discover devices; it must not guess unsafe electrical properties.

### 5. Module layer

Owns reusable functional blocks such as:

- Servo bank.
- Motor driver.
- Sensor cluster.
- MIDI controller.
- DMX interface.
- Lighting module.
- Encoder/button panel.
- Audio control surface.

Each module declares:

- Required capabilities.
- Voltage/current needs.
- Protocol.
- Firmware driver/module.
- Failure behavior.

### 6. Product/experiment layer

Combines modules into a specific machine, instrument, robot, controller or experiment.

This is where projects such as robotics, musical controllers, lighting systems or future vehicle platforms consume the common stack.

## Contracts

### Connector contract

Every connector must document:

- Connector ID.
- Physical pin order.
- Signal names.
- Direction.
- Logic voltage.
- Power voltage.
- Maximum intended current.
- Whether hot-plugging is allowed.
- Protection present or absent.

### Power contract

Every board must publish a power tree and distinguish at minimum:

- MCU/logic domain.
- Sensor/peripheral domain when different.
- Actuator/high-current domain.
- External power input.
- Ground relationship.

### Module manifest

A future machine-readable module manifest should be able to express:

```json
{
  "module": "servo-bank",
  "requires": ["PWM_SERVO_0", "POWER_ACTUATOR_EXT", "GND_COMMON"],
  "logic_voltage": 5,
  "actuator_voltage_range": [5, 6],
  "driver": "ServoBank"
}
```

The exact schema will be finalized alongside the first board rather than guessed in advance.

## First BSP: Arduino Leonardo / ATmega32U4

The Leonardo is the first platform used to prove the architecture.

Design constraints to encode explicitly:

- Native USB is a first-class host interface.
- SPI routing differs from assumptions commonly made from Uno-style header layouts; the ICSP header is part of the board contract.
- Servo/actuator power must be separable from the Leonardo's logic supply.
- Shared ground is required when external actuator power is used, unless a future isolated module explicitly changes that contract.
- Expansion buses should remain accessible after the shield is installed.

## Compatibility rule

A new board can join the ecosystem when it provides a BSP that satisfies the same capability contracts. This allows later carriers such as ESP32, STM32, RP2040 or custom BlackMamba PCBs without rewriting module-level software.

## Design review gates

Before a physical board revision is considered ready:

1. Circuit schema/semantic validation passes.
2. Power tree is documented.
3. Connector contracts are complete.
4. EMI/noise checklist is reviewed.
5. Firmware BSP compiles for the target.
6. Diagnostic strategy exists for first power-on.
7. BOM and assembly assumptions are captured.
8. Revision history states what changed and why.
