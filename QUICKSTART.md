# Guía de Inicio Rápido

## 🚀 Comenzar en 5 Minutos

### 1. Instalar Blender
```bash
# Ubuntu/Debian
sudo apt install blender

# macOS
brew install --cask blender

# Windows: Descargar desde https://www.blender.org/download/
```

### 2. Generar tu Primer Circuito 3D

1. Abrir Blender
2. Ir a la pestaña "Scripting"
3. Click "Open" y seleccionar: `blender_models/scripts/component_generator.py`
4. Click "Run Script" (▶)
5. En la consola de Python (abajo), escribir:
```python
create_example_circuit()
```
6. Presionar F12 para renderizar

¡Listo! Verás un circuito completo con componentes, PCB, LEDs e ICs.

### 3. Validar un Diseño

```bash
cd /ruta/al/proyecto/circuit
python3 blender_models/scripts/validate_circuit.py examples/circuit_with_3d.circuit.json
```

El validador verificará:
- ✅ Condensadores de desacoplamiento
- ✅ Espaciado entre componentes  
- ✅ Red de alimentación
- ✅ Conexiones a tierra

### 4. Exportar a Altium Designer

```bash
cd /ruta/al/proyecto/circuit
python3 adapters/circuit_to_altium.py examples/circuit_with_3d.circuit.json altium_export/
```

El adaptador generará:
- ✅ Biblioteca de componentes (CSV)
- ✅ Netlist en formato Protel
- ✅ Bill of Materials (BOM)
- ✅ Coordenadas de colocación
- ✅ Reglas de diseño
- ✅ Guía de importación completa

Ver `altium_export/ALTIUM_IMPORT_GUIDE.txt` para instrucciones de importación.

### 5. Usar el Checklist de Diseño

Antes de fabricar tu PCB:
1. Abrir `docs/guidelines/pcb_design_checklist.md`
2. Revisar cada punto
3. Marcar completados
4. Corregir problemas

---

## 📚 Documentación Completa

| Documento | Descripción |
|-----------|-------------|
| `docs/SYSTEM_OVERVIEW.md` | Vista completa del sistema |
| `docs/blender_usage_guide.md` | Tutorial detallado de Blender |
| `docs/guidelines/emi_noise_prevention.md` | Guía completa EMI/ruido |
| `docs/guidelines/pcb_design_checklist.md` | Checklist pre-fabricación |
| `blender_models/README.md` | Info sobre modelos 3D |
| `adapters/README.md` | Adaptadores para EDA tools (Altium, etc.) |

---

## 🎯 Casos de Uso Comunes

### Exportar a Altium Designer
```bash
# Circuito simple
python3 adapters/circuit_to_altium.py examples/simple_circuit.circuit.json my_project/

# Circuito con 3D y EMI
python3 adapters/circuit_to_altium.py examples/circuit_with_3d.circuit.json altium_output/
```

### Crear Resistor SMD
```python
create_resistor_smd_0805("R1", location=(0, 0, 0), resistance_value="10K")
```

### Crear Condensador
```python
create_capacitor_smd_0805("C1", location=(5, 0, 0), capacitance_value="100nF")
```

### Crear IC
```python
create_ic_soic8("U1", location=(10, 0, 0))
```

### Crear LED
```python
create_led_smd_0805("LED1", location=(15, 0, 0), color="red")
```

### Crear PCB
```python
create_pcb_board("PCB", location=(0, 0, -1), size=(60, 40), thickness=1.6)
```

---

## ⚡ Reglas de Oro para EMI

1. **Condensador 100nF a < 5mm de cada IC**
2. **Plano de tierra continuo sin divisiones**
3. **Separar analógico de digital > 10mm**
4. **Filtro en entrada de alimentación**
5. **Bucles de corriente lo más pequeños posible**

Ver guía completa en `docs/guidelines/emi_noise_prevention.md`

---

## 🛠️ Herramientas Incluidas

### component_generator.py
Script de Blender para generar modelos 3D de componentes electrónicos.

**Componentes disponibles:**
- Resistores SMD 0805
- Condensadores SMD 0805
- LEDs SMD 0805 (rojo, verde, azul, amarillo)
- ICs SOIC-8
- Conectores de pines (2.54mm pitch)
- PCBs personalizables

### validate_circuit.py
Validador de diseño de circuitos contra mejores prácticas EMI.

**Verificaciones:**
- Desacoplamiento de ICs
- Espaciado de componentes
- Red de alimentación
- Conectividad de tierra
- Reglas de diseño

---

## 📦 Formato .circuit.json Extendido

El sistema usa archivos JSON para definir circuitos:

```json
{
  "metadata": {
    "name": "mi-circuito",
    "version": "1.0.0"
  },
  "board": {
    "dimensions": {"width": 60, "height": 40, "thickness": 1.6}
  },
  "components": [
    {
      "id": "R1",
      "type": "resistor",
      "package": "0805",
      "model_3d": {
        "generator": "create_resistor_smd_0805",
        "position": {"x": 0, "y": 0, "z": 0}
      }
    }
  ],
  "design_rules": {
    "emi_compliance": {
      "standard": "FCC Part 15 Class B"
    }
  }
}
```

---

## 🤝 Contribuir

¿Encontraste un bug? ¿Tienes una idea?

1. Abre un Issue: https://github.com/Blackmvmba88/circuit/issues
2. O envía un Pull Request

---

## 📖 Siguiente Paso

Lee `docs/SYSTEM_OVERVIEW.md` para entender todo el sistema.

---

*Última actualización: 2025-11-24*
