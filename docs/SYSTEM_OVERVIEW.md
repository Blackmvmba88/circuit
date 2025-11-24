# Sistema Completo de Diseño de Circuitos con Blender

## Descripción General

Este sistema integra modelado 3D con Blender, diseño de circuitos basado en JSON, y guías de mejores prácticas para EMI/ruido. Es una solución completa para diseñadores de circuitos electrónicos que necesitan:

1. **Visualización 3D** de componentes y placas de circuito
2. **Validación de diseño** contra mejores prácticas de EMI
3. **Documentación técnica** completa
4. **Interoperabilidad** con herramientas CAD existentes

---

## Componentes del Sistema

### 1. Generador de Modelos 3D (Blender)
**Ubicación**: `blender_models/scripts/component_generator.py`

Características:
- Genera modelos 3D de componentes electrónicos con dimensiones estándar
- Componentes disponibles:
  - Resistores SMD (0805)
  - Condensadores SMD (0805)
  - LEDs SMD (0805) en múltiples colores
  - ICs (SOIC-8)
  - Conectores de pines (pitch 2.54mm)
  - Placas PCB personalizables
- Materiales realistas (metálicos, cerámicos, plásticos)
- Exportación a múltiples formatos (STL, OBJ, glTF, FBX)

**Uso rápido**:
```python
# En Blender, cargar el script y ejecutar:
create_example_circuit()
```

### 2. Formato de Circuito Extendido
**Ubicación**: `examples/circuit_with_3d.circuit.json`

Extensión del formato .circuit.json que incluye:
- Referencias a modelos 3D de componentes
- Posiciones y rotaciones 3D
- Reglas de diseño EMI
- Información de configuración de render

**Estructura**:
```json
{
  "metadata": {...},
  "board": {
    "dimensions": {...},
    "model_3d": {...}
  },
  "components": [
    {
      "id": "R1",
      "type": "resistor",
      "model_3d": {
        "generator": "create_resistor_smd_0805",
        "position": {"x": 0, "y": 0, "z": 0}
      }
    }
  ],
  "design_rules": {
    "emi_compliance": {...}
  }
}
```

### 3. Validador de Circuitos
**Ubicación**: `blender_models/scripts/validate_circuit.py`

Herramienta de línea de comandos que verifica:
- ✅ Condensadores de desacoplamiento cerca de ICs
- ✅ Espaciado adecuado entre componentes
- ✅ Red de distribución de alimentación
- ✅ Conectividad de tierra
- ✅ Cumplimiento de reglas de diseño

**Uso**:
```bash
python3 blender_models/scripts/validate_circuit.py examples/circuit_with_3d.circuit.json
```

### 4. Guías de Diseño EMI/Ruido
**Ubicación**: `docs/guidelines/emi_noise_prevention.md`

Documentación exhaustiva que cubre:
- Principios fundamentales de EMI
- Reglas de diseño de PCB (capas, planos de tierra, trazado)
- Técnicas de filtrado y desacoplamiento
- Cableado y conectores
- Consideraciones de señales específicas (I2C, SPI, USB, etc.)
- Circuitos analógicos vs digitales
- Técnicas avanzadas (shielding, guard rings)
- Testing y validación
- Estándares (FCC, CISPR, IEC)
- Ejemplos prácticos

### 5. Checklist de Diseño
**Ubicación**: `docs/guidelines/pcb_design_checklist.md`

Lista de verificación práctica con:
- 13 categorías de verificación
- Niveles de cumplimiento (Básico, Intermedio, Avanzado)
- Formato imprimible para certificación
- Referencias a herramientas y recursos

### 6. Guía de Uso de Blender
**Ubicación**: `docs/blender_usage_guide.md`

Tutorial completo que explica:
- Instalación y configuración
- Creación de componentes individuales
- Diseño de circuitos completos
- Principios de layout con consideraciones EMI
- Exportación de modelos
- Renderizado y animación
- Integración con .circuit.json
- Tips y solución de problemas

---

## Flujo de Trabajo Recomendado

### Fase 1: Diseño Conceptual
1. Definir requisitos del circuito
2. Seleccionar componentes principales
3. Consultar guías EMI para restricciones de diseño

### Fase 2: Diseño Esquemático
1. Crear archivo .circuit.json con componentes y conexiones
2. Agregar condensadores de desacoplamiento según guías
3. Definir reglas de diseño en `design_rules`

### Fase 3: Validación Temprana
```bash
# Validar diseño antes de layout
python3 blender_models/scripts/validate_circuit.py mi_circuito.circuit.json
```

### Fase 4: Layout y Visualización 3D
1. Abrir Blender
2. Cargar `component_generator.py`
3. Generar modelo 3D del circuito
4. Verificar espaciado y colocación visual
5. Ajustar posiciones si es necesario

### Fase 5: Revisión con Checklist
1. Imprimir `docs/guidelines/pcb_design_checklist.md`
2. Revisar cada punto
3. Corregir problemas identificados
4. Obtener aprobación de revisión

### Fase 6: Exportación a EDA Tools
1. Exportar a Altium Designer:
   ```bash
   python3 adapters/circuit_to_altium.py mi_circuito.circuit.json altium_export/
   ```
2. Importar en Altium siguiendo la guía generada
3. Revisar y ajustar footprints según componentes reales

### Fase 7: Fabricación
1. Generar Gerbers desde Altium/KiCAD/Eagle
2. Revisar archivos con visor de Gerber
3. Enviar a fabricación

### Fase 8: Documentación
1. Renderizar imágenes 3D del circuito
2. Exportar modelo 3D para manual de usuario
3. Documentar decisiones de diseño EMI

---

## Ejemplos de Uso

### Ejemplo 1: Crear Circuito Simple en Blender

```python
# En Blender Script Editor
import bpy

# Limpiar escena
clear_scene()

# Crear PCB
create_pcb_board("MyPCB", location=(0, 0, -1), size=(40, 30))

# Agregar componentes
create_ic_soic8("U1", location=(0, 0, 0))
create_capacitor_smd_0805("C1", location=(8, 0, 0), capacitance_value="100nF")
create_resistor_smd_0805("R1", location=(-10, 0, 0), resistance_value="10K")
create_led_smd_0805("LED1", location=(0, -10, 0), color="green")

# Configurar vista
bpy.ops.object.camera_add(location=(40, -40, 30))
camera = bpy.context.active_object
camera.rotation_euler = (1.1, 0, 0.785)
bpy.context.scene.camera = camera

# Renderizar
bpy.context.scene.render.filepath = "/tmp/circuit.png"
bpy.ops.render.render(write_still=True)
```

### Ejemplo 2: Validar Diseño Existente

```bash
# Terminal
cd /ruta/al/proyecto/circuit

# Validar diseño
python3 blender_models/scripts/validate_circuit.py examples/simple_circuit.circuit.json

# El script reportará errores y advertencias
```

### Ejemplo 3: Verificar Cumplimiento EMI

1. Abrir `docs/guidelines/pcb_design_checklist.md`
2. Para cada sección:
   - Verificar en el diseño
   - Marcar ✅ o ❌
   - Anotar observaciones
3. Corregir todos los ❌ antes de fabricar

---

## Reglas de Oro del Sistema

### Para Reducir EMI:
1. **Condensadores de desacoplamiento**: 100nF a <5mm de CADA IC
2. **Plano de tierra continuo**: Sin divisiones grandes
3. **Bucles pequeños**: Señal y retorno lo más cerca posible
4. **Filtrado en entrada**: Ferrite bead + condensadores
5. **Separación de dominios**: Analógico lejos de digital (>10mm)

### Para Visualización 3D:
1. **Dimensiones reales**: Todos los modelos usan medidas estándar
2. **Espaciado visible**: Verificar visualmente separaciones
3. **Orientación correcta**: Pin 1 de ICs siempre marcado
4. **Escala consistente**: 1 unidad Blender = 1mm

### Para Diseño General:
1. **Validar temprano**: Usar validate_circuit.py frecuentemente
2. **Seguir checklist**: Antes de cada fabricación
3. **Documentar decisiones**: Usar campo "design_notes" en JSON
4. **Revisar guías**: Consultar emi_noise_prevention.md para casos especiales
5. **Exportar a EDA**: Usar adaptadores para importar en herramientas CAD

---

## Integración con Herramientas Externas

### Altium Designer (✅ IMPLEMENTADO)
```bash
# Exportar circuito a formato Altium
python3 adapters/circuit_to_altium.py examples/circuit_with_3d.circuit.json altium_export/

# Archivos generados:
# - component_library.csv  : Biblioteca de componentes
# - netlist.net            : Netlist en formato Protel
# - bom.csv                : Bill of Materials
# - component_placement.csv: Coordenadas de componentes
# - board_outline.txt      : Dimensiones de PCB
# - design_rules.txt       : Reglas de diseño recomendadas
# - ALTIUM_IMPORT_GUIDE.txt: Guía de importación paso a paso
```

**Características**:
- ✅ Exportación de biblioteca de componentes
- ✅ Netlist en formato Protel (nativo de Altium)
- ✅ BOM con componentes agrupados
- ✅ Coordenadas de colocación para PCB
- ✅ Mapeo automático de footprints
- ✅ Conversión de valores (resistencias, capacitancias)
- ✅ Preservación de reglas de diseño EMI/EMC
- ✅ Guía completa de importación

### KiCAD (Planeado)
```python
# Script para exportar KiCAD a .circuit.json (futuro)
# kicad_to_circuit.py
```

### SPICE (Planeado)
```python
# Script para exportar .circuit.json a SPICE netlist (futuro)
# circuit_to_spice.py
```

### Fusion 360 / FreeCAD
1. Exportar modelo 3D de Blender como STEP
2. Importar en Fusion 360 / FreeCAD
3. Diseñar carcasa alrededor del PCB

---

## Extensibilidad

### Agregar Nuevo Tipo de Componente

1. Editar `blender_models/scripts/component_generator.py`
2. Agregar nueva función siguiendo el patrón:

```python
def create_mi_componente(name="Comp", location=(0, 0, 0), **params):
    """
    Descripción del componente.
    
    Args:
        name: Nombre del componente
        location: Posición (x, y, z) en mm
        **params: Parámetros específicos
    
    Returns:
        Objeto Blender creado
    """
    # Crear geometría
    # Aplicar materiales
    # Agrupar partes
    return objeto
```

3. Actualizar documentación
4. Agregar ejemplo de uso

### Agregar Nueva Regla de Validación

1. Editar `blender_models/scripts/validate_circuit.py`
2. Agregar método a clase `CircuitValidator`:

```python
def check_mi_regla(self):
    """Descripción de la regla."""
    self.info.append("Checking mi regla...")
    
    # Lógica de validación
    if condicion_error:
        self.errors.append("Mensaje de error")
    elif condicion_warning:
        self.warnings.append("Mensaje de advertencia")
```

3. Llamar en método `validate()`

---

## Recursos Adicionales

### Dentro del Proyecto
- `README.md`: Vista general del proyecto
- `ROADMAP.md`: Planes futuros
- `CONTRIBUTING.md`: Guía de contribución
- `examples/`: Circuitos de ejemplo

### Enlaces Externos
- **Blender**: https://www.blender.org/
- **Guías EMI**: 
  - Texas Instruments EMC/EMI Design Guide
  - Analog Devices PCB Design Guidelines
- **Estándares**:
  - FCC Part 15: https://www.fcc.gov/
  - CISPR 22: https://www.iec.ch/

### Comunidad
- Abrir Issues en GitHub para preguntas
- Contribuir mejoras vía Pull Requests
- Compartir diseños exitosos en Discussions

---

## Próximos Pasos (Roadmap)

### Corto Plazo
- [ ] Agregar más tipos de componentes (QFN, BGA, conectores USB)
- [ ] Script de importación desde KiCAD
- [ ] Mejorar validador con más reglas
- [ ] Tutoriales en video

### Medio Plazo
- [ ] Editor web interactivo
- [ ] Simulador SPICE integrado
- [ ] Biblioteca de componentes compartida
- [ ] Generación automática de documentación

### Largo Plazo
- [ ] Plugin para KiCAD
- [ ] Extensión para VS Code
- [ ] Marketplace de componentes
- [ ] Colaboración en tiempo real

---

## Soporte y Contribución

### Reportar Problemas
- Usar GitHub Issues
- Incluir archivo .circuit.json si es relevante
- Describir comportamiento esperado vs actual

### Contribuir Código
1. Fork del repositorio
2. Crear branch para feature
3. Seguir guías de código existentes
4. Agregar tests si aplica
5. Abrir Pull Request

### Mejorar Documentación
- Correcciones de typos: editar directamente
- Nuevas secciones: seguir estructura existente
- Ejemplos adicionales: muy bienvenidos

---

## Licencia

MIT License - Ver `LICENSE` en el directorio raíz.

Este sistema es open source y libre de usar para proyectos comerciales y personales.

---

## Contacto

- **GitHub**: https://github.com/Blackmvmba88/circuit
- **Issues**: https://github.com/Blackmvmba88/circuit/issues
- **Discussions**: https://github.com/Blackmvmba88/circuit/discussions

---

*Sistema diseñado y documentado para el proyecto "circuit"*
*Versión: 1.0*
*Última actualización: 2025-11-24*
