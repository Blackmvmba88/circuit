# Guía de Uso del Sistema de Modelado 3D con Blender para Circuitos

## Introducción

Este documento explica cómo usar el sistema de generación de modelos 3D de componentes electrónicos con Blender. Los modelos generados siguen dimensiones industriales estándar y pueden exportarse para visualización, documentación técnica y diseño de PCB.

---

## Requisitos Previos

### Software Necesario
- **Blender 3.0 o superior** (recomendado 4.0+)
- **Python 3.10+** (incluido con Blender)

### Conocimientos Básicos
- Familiaridad básica con la interfaz de Blender
- Comprensión de componentes electrónicos
- Opcional: Python básico para personalización

---

## Instalación y Configuración

### 1. Instalar Blender

```bash
# Ubuntu/Debian
sudo apt install blender

# macOS (usando Homebrew)
brew install --cask blender

# Windows
# Descargar desde https://www.blender.org/download/
```

### 2. Cargar el Script de Generación

Hay tres métodos para usar el script:

#### Método A: Ejecutar desde el Editor de Scripts (Recomendado)

1. Abrir Blender
2. Cambiar a la pestaña "Scripting" (en la parte superior)
3. Click en "Open" y seleccionar `blender_models/scripts/component_generator.py`
4. Click en "Run Script" (botón ▶ o Alt+P)

#### Método B: Ejecutar desde la Consola de Python

1. En Blender, abrir Window → Toggle System Console (Windows) o ver terminal (Linux/Mac)
2. Cambiar a pestaña "Scripting"
3. En la consola de Python (parte inferior):

```python
import sys
sys.path.append('/ruta/al/proyecto/circuit/blender_models/scripts')
import component_generator
```

#### Método C: Agregar al Directorio de Scripts de Blender

```bash
# Copiar el script al directorio de scripts de usuario
cp blender_models/scripts/component_generator.py ~/.config/blender/3.x/scripts/addons/
```

---

## Uso Básico

### Crear Componentes Individuales

Después de cargar el script, puedes crear componentes usando las funciones disponibles:

#### Resistor SMD (0805)

```python
# Crear un resistor en el origen
create_resistor_smd_0805("R1", location=(0, 0, 0), resistance_value="10K")

# Crear múltiples resistores
create_resistor_smd_0805("R2", location=(5, 0, 0), resistance_value="1K")
create_resistor_smd_0805("R3", location=(10, 0, 0), resistance_value="100R")
```

**Parámetros:**
- `name`: Nombre del componente (string)
- `location`: Tupla (x, y, z) en milímetros
- `resistance_value`: Valor para referencia (string, no afecta el modelo)

#### Condensador SMD (0805)

```python
# Condensador cerámico
create_capacitor_smd_0805("C1", location=(0, 5, 0), capacitance_value="100nF")

# Condensador de desacoplamiento
create_capacitor_smd_0805("C2", location=(5, 5, 0), capacitance_value="10uF")
```

**Parámetros:**
- `name`: Nombre del componente
- `location`: Posición (x, y, z) en mm
- `capacitance_value`: Valor para referencia

#### Circuito Integrado (SOIC-8)

```python
# IC estándar de 8 pines
create_ic_soic8("U1", location=(0, 10, 0))

# Múltiples ICs
create_ic_soic8("U2", location=(15, 10, 0))
```

**Parámetros:**
- `name`: Nombre del componente
- `location`: Posición (x, y, z) en mm

**Nota**: El IC incluye un indicador de pin 1 (círculo blanco en la esquina)

#### LED SMD (0805)

```python
# LED rojo
create_led_smd_0805("LED1", location=(0, -5, 0), color="red")

# Otros colores disponibles
create_led_smd_0805("LED2", location=(5, -5, 0), color="green")
create_led_smd_0805("LED3", location=(10, -5, 0), color="blue")
create_led_smd_0805("LED4", location=(15, -5, 0), color="yellow")
```

**Parámetros:**
- `name`: Nombre del componente
- `location`: Posición (x, y, z) en mm
- `color`: Color del LED ("red", "green", "blue", "yellow")

#### Conector de Pines

```python
# Conector de 6 pines
create_header_connector("J1", location=(20, 0, 0), num_pins=6)

# Conector de 8 pines
create_header_connector("J2", location=(20, 10, 0), num_pins=8)
```

**Parámetros:**
- `name`: Nombre del conector
- `location`: Posición (x, y, z) en mm
- `num_pins`: Número de pines (entero)

#### Placa PCB

```python
# PCB estándar de 50x50mm
create_pcb_board("PCB_Main", location=(0, 0, -1), size=(50, 50), thickness=1.6)

# PCB rectangular de 60x40mm
create_pcb_board("PCB_Custom", location=(0, 0, -1), size=(60, 40), thickness=1.6)
```

**Parámetros:**
- `name`: Nombre del PCB
- `location`: Posición (x, y, z) en mm (típicamente z=-1 para estar debajo)
- `size`: Tupla (ancho, alto) en mm
- `thickness`: Grosor en mm (estándar: 1.6mm)

---

## Crear Circuitos Completos

### Circuito de Ejemplo

El script incluye una función para crear un circuito de ejemplo completo:

```python
# Limpiar escena y crear circuito de demostración
create_example_circuit()
```

Este comando crea:
- Una placa PCB de 60x40mm
- Condensadores de desacoplamiento en la sección de alimentación
- Un IC SOIC-8 con condensador cercano
- Resistores y LEDs
- Conector de 6 pines
- Cámara y luz configuradas automáticamente

### Crear tu Propio Circuito

```python
# 1. Limpiar la escena
clear_scene()

# 2. Crear el PCB base
create_pcb_board("PCB", location=(0, 0, -1), size=(80, 60))

# 3. Agregar componentes según tu diseño
# Sección de alimentación
create_capacitor_smd_0805("C1", location=(-30, 20, 0), capacitance_value="10uF")
create_capacitor_smd_0805("C2", location=(-25, 20, 0), capacitance_value="100nF")

# Microcontrolador
create_ic_soic8("U1", location=(0, 15, 0))
create_capacitor_smd_0805("C3", location=(8, 15, 0), capacitance_value="100nF")

# Resistencias pull-up
create_resistor_smd_0805("R1", location=(-10, 5, 0), resistance_value="10K")
create_resistor_smd_0805("R2", location=(-5, 5, 0), resistance_value="10K")

# LEDs indicadores
create_resistor_smd_0805("R3", location=(10, -10, 0), resistance_value="330R")
create_led_smd_0805("LED1", location=(15, -10, 0), color="green")

# Conector
create_header_connector("J1", location=(-30, -20, 0), num_pins=8)

# 4. Configurar vista
bpy.ops.object.camera_add(location=(60, -60, 50))
camera = bpy.context.active_object
camera.rotation_euler = (1.0, 0, 0.785)
bpy.context.scene.camera = camera

bpy.ops.object.light_add(type='SUN', location=(20, 20, 30))
```

---

## Principios de Layout con EMI en Mente

Al crear modelos 3D de tus circuitos, sigue estas reglas para espaciado (consulta `docs/guidelines/emi_noise_prevention.md` para detalles completos):

### Espaciado Mínimo entre Componentes

```python
# Espaciado recomendado (en mm)
SPACING_RULES = {
    "smd_to_smd": 2.0,           # Entre componentes SMD generales
    "ic_to_decoupling": 5.0,     # IC al condensador de desacoplamiento
    "power_to_signal": 10.0,     # Componentes de potencia a señales
    "analog_to_digital": 10.0,   # Circuitos analógicos a digitales
    "connector_clearance": 15.0, # Espacio libre alrededor de conectores
}

# Ejemplo de uso:
ic_position = (0, 0, 0)
decoupling_cap_position = (
    ic_position[0] + SPACING_RULES["ic_to_decoupling"],
    ic_position[1],
    ic_position[2]
)
create_ic_soic8("U1", location=ic_position)
create_capacitor_smd_0805("C1", location=decoupling_cap_position)
```

### Agrupación por Función

```python
# Grupo de alimentación
power_x = -20
create_capacitor_smd_0805("C_bulk", location=(power_x, 20, 0), capacitance_value="100uF")
create_capacitor_smd_0805("C_filter", location=(power_x + 5, 20, 0), capacitance_value="100nF")

# Grupo de señal digital
digital_x = 0
create_ic_soic8("MCU", location=(digital_x, 10, 0))
create_capacitor_smd_0805("C_dec", location=(digital_x + 8, 10, 0), capacitance_value="100nF")

# Grupo analógico (separado)
analog_x = 20
create_ic_soic8("ADC", location=(analog_x, 10, 0))
create_capacitor_smd_0805("C_analog", location=(analog_x + 8, 10, 0), capacitance_value="10uF")
```

---

## Exportación de Modelos

### Exportar a Formatos Comunes

#### STL (Para impresión 3D)

```python
# Seleccionar todos los objetos
bpy.ops.object.select_all(action='SELECT')

# Exportar
bpy.ops.export_mesh.stl(
    filepath="/ruta/salida/circuit_model.stl",
    use_selection=True
)
```

En la interfaz de Blender:
1. File → Export → STL (.stl)
2. Seleccionar ubicación
3. Click "Export STL"

#### OBJ (Para visualización general)

```python
# Exportar como OBJ
bpy.ops.export_scene.obj(
    filepath="/ruta/salida/circuit_model.obj",
    use_selection=True,
    use_materials=True
)
```

#### glTF/GLB (Para web y AR/VR)

```python
# Exportar como glTF
bpy.ops.export_scene.gltf(
    filepath="/ruta/salida/circuit_model.glb",
    export_format='GLB'
)
```

En la interfaz:
1. File → Export → glTF 2.0 (.glb/.gltf)
2. Seleccionar formato GLB para archivo único
3. Click "Export glTF 2.0"

#### FBX (Para software CAD/CAM)

```python
# Exportar como FBX
bpy.ops.export_scene.fbx(
    filepath="/ruta/salida/circuit_model.fbx"
)
```

---

## Renderizado

### Render Rápido (Vista Previa)

```python
# Configurar render básico
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.filepath = "/ruta/salida/render.png"

# Renderizar
bpy.ops.render.render(write_still=True)
```

En la interfaz:
1. Presionar F12 para renderizar
2. Imagen → Save As para guardar

### Render de Alta Calidad

```python
# Configurar Cycles para calidad fotorrealista
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = 256  # Más samples = mejor calidad
bpy.context.scene.render.resolution_x = 3840  # 4K
bpy.context.scene.render.resolution_y = 2160
bpy.context.scene.cycles.use_denoising = True

# Renderizar
bpy.ops.render.render(write_still=True)
```

### Animación de Rotación

```python
import math

# Función para crear animación orbital
def create_turntable_animation(frames=120):
    """Crea animación de 360° alrededor del circuito"""
    camera = bpy.data.objects.get("Camera")
    if not camera:
        return
    
    radius = 50
    height = 30
    
    for frame in range(frames):
        angle = 2 * math.pi * frame / frames
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        
        camera.location = (x, y, height)
        camera.rotation_euler = (1.0, 0, angle + math.pi/2)
        
        # Insertar keyframe
        camera.keyframe_insert(data_path="location", frame=frame)
        camera.keyframe_insert(data_path="rotation_euler", frame=frame)
    
    bpy.context.scene.frame_end = frames

# Usar la función
create_turntable_animation(frames=240)  # 10 segundos @ 24fps
```

---

## Integración con el Formato .circuit.json

### Agregar Referencias 3D al Formato

Puedes extender el formato de circuito para incluir referencias a modelos 3D:

```json
{
  "metadata": {
    "name": "circuit-con-3d",
    "author": "tu-nombre",
    "version": "0.2.0",
    "created_at": "2025-11-24T00:00:00Z"
  },
  "components": [
    {
      "id": "R1",
      "type": "resistor",
      "package": "0805",
      "params": { "resistance_ohm": 1000 },
      "pins": { "1": { "x": 10, "y": 10 }, "2": { "x": 20, "y": 10 } },
      "model_3d": {
        "file": "blender_models/components/resistor_0805.blend",
        "position": { "x": 10, "y": 10, "z": 0 },
        "rotation": { "x": 0, "y": 0, "z": 0 }
      }
    },
    {
      "id": "U1",
      "type": "ic",
      "package": "SOIC8",
      "params": { "part_number": "LM358" },
      "pins": {
        "1": { "x": 0, "y": 10 },
        "8": { "x": 5, "y": 10 }
      },
      "model_3d": {
        "file": "blender_models/components/ic_soic8.blend",
        "position": { "x": 0, "y": 15, "z": 0 },
        "rotation": { "x": 0, "y": 0, "z": 0 }
      }
    }
  ],
  "board": {
    "dimensions": { "width": 60, "height": 40, "thickness": 1.6 },
    "model_3d": {
      "file": "blender_models/components/pcb_board.blend",
      "color": "green"
    }
  }
}
```

### Script para Generar Circuito desde JSON

```python
import json
import bpy

def load_circuit_from_json(json_file):
    """
    Carga un circuito desde un archivo .circuit.json y genera
    el modelo 3D en Blender.
    """
    with open(json_file, 'r') as f:
        circuit_data = json.load(f)
    
    clear_scene()
    
    # Crear PCB si está definido
    if 'board' in circuit_data:
        board = circuit_data['board']
        dims = board['dimensions']
        create_pcb_board(
            "PCB",
            location=(0, 0, -dims['thickness']/2),
            size=(dims['width'], dims['height']),
            thickness=dims['thickness']
        )
    
    # Crear componentes
    for comp in circuit_data['components']:
        comp_type = comp['type']
        comp_id = comp['id']
        
        if 'model_3d' in comp:
            pos = comp['model_3d']['position']
            location = (pos['x'], pos['y'], pos['z'])
        else:
            # Usar posición del primer pin
            pin_pos = list(comp['pins'].values())[0]
            location = (pin_pos['x'], pin_pos['y'], 0)
        
        # Crear según tipo
        if comp_type == 'resistor':
            value = f"{comp['params'].get('resistance_ohm', 0)}Ω"
            create_resistor_smd_0805(comp_id, location, value)
        elif comp_type == 'capacitor':
            value = f"{comp['params'].get('capacitance_f', 0)}F"
            create_capacitor_smd_0805(comp_id, location, value)
        elif comp_type == 'ic':
            create_ic_soic8(comp_id, location)
        elif comp_type == 'led':
            color = comp['params'].get('color', 'red')
            create_led_smd_0805(comp_id, location, color)
    
    print(f"Circuit '{circuit_data['metadata']['name']}' loaded successfully!")

# Uso:
# load_circuit_from_json('/ruta/al/archivo.circuit.json')
```

---

## Tips y Trucos

### Optimización de Rendimiento

1. **Usar instancias para componentes repetidos:**
```python
# Crear un componente maestro
master = create_resistor_smd_0805("R_master", (0, 0, 0))

# Crear instancias (más eficiente)
for i in range(10):
    instance = master.copy()
    instance.location = (i * 5, 0, 0)
    bpy.context.collection.objects.link(instance)
```

2. **Simplificar geometría para escenas grandes:**
```python
# Reducir subdivisiones en cilindros/esferas si es necesario
bpy.ops.mesh.primitive_cylinder_add(vertices=16)  # En lugar de 32
```

### Automatización Avanzada

```python
def create_resistor_array(start_pos, count, spacing, prefix="R"):
    """Crea un array de resistores"""
    for i in range(count):
        pos = (
            start_pos[0] + i * spacing,
            start_pos[1],
            start_pos[2]
        )
        name = f"{prefix}{i+1}"
        create_resistor_smd_0805(name, pos, "10K")

# Uso
create_resistor_array(start_pos=(0, 0, 0), count=8, spacing=5)
```

---

## Solución de Problemas

### El script no se ejecuta

**Problema**: Error al cargar el script
**Solución**: 
1. Verificar que la ruta al script es correcta
2. Asegurar que Python está habilitado en Blender
3. Verificar la consola de Python para errores

### Componentes no visibles

**Problema**: Los objetos se crean pero no se ven
**Solución**:
1. Presionar Home o `.` (punto) en el teclado numérico para enfocar
2. Verificar que la cámara está correctamente posicionada
3. Cambiar a vista de cámara (Numpad 0)

### Render muy lento

**Problema**: El render tarda mucho tiempo
**Solución**:
1. Usar EEVEE en lugar de Cycles para previews rápidas
2. Reducir el número de samples
3. Reducir la resolución para pruebas
4. Desactivar efectos avanzados temporalmente

---

## Próximos Pasos

1. **Explorar componentes adicionales**: Agregar más tipos de paquetes (QFN, BGA, etc.)
2. **Personalizar materiales**: Crear materiales personalizados para diferentes acabados
3. **Automatización completa**: Script para importar KiCAD/Eagle y generar 3D automáticamente
4. **Biblioteca de componentes**: Construir una biblioteca compartida de modelos 3D

---

## Recursos Adicionales

- **Documentación de Blender Python API**: https://docs.blender.org/api/current/
- **Tutoriales de Blender**: https://www.blender.org/support/tutorials/
- **Guía EMI del proyecto**: `docs/guidelines/emi_noise_prevention.md`

---

*Documento creado para el proyecto "circuit"*
*Última actualización: 2025-11-24*
