# circuit

Bienvenido a "circuit" — un entorno open-source para creación, edición y seguimiento de circuitos electrónicos y digitales, diseñado para ser interoperable con cualquier herramienta que quiera sumarse a la aventura. Piensa en un "Visual Studio Code" para circuitos: extensible, modular y colaborativo.

## Visión
Crear un ecosistema abierto para diseñar, simular, documentar y compartir circuitos, donde herramientas externas puedan integrarse mediante adaptadores o plugins y donde la comunidad construya una librería común de componentes y formatos.

## Qué es
- Un formato de intercambio de circuitos (JSON legible por máquinas).
- Un conjunto de especificaciones para adaptadores (simuladores, CAD, visualizadores).
- Plantillas y guía para construir editores y plugins.
- Un repositorio central para bibliotecas de componentes reutilizables.

## Características iniciales (MVP)
- Formato de archivo interoperable (.circuit.json)
- Editor básico (web/CLI) para crear y editar esquemas simples
- Adaptador de ejemplo para exportar a un simulador popular (por ejemplo, SPICE)
- **Adaptador para Altium Designer** - exporta circuitos al formato Altium
- Librería de componentes básicos (resistores, condensadores, fuentes, puertas lógicas)
- **Sistema de modelado 3D con Blender** para visualización de componentes
- **Guías de diseño EMI/ruido** para crear circuitos robustos

## Formato de archivo (breve)
Usaremos JSON con:
- metadata: nombre, autor, versión, fecha
- components: lista con ids, tipo, parámetros, posición
- nets: conexiones entre pines
- sim_config (opcional): parámetros de simulación
- model_3d (opcional): referencias a modelos 3D de Blender

Ejemplo: ver `examples/simple_circuit.circuit.json`.

## Sistema de Modelado 3D con Blender
El proyecto incluye un sistema completo para generar modelos 3D de componentes electrónicos:
- Scripts Python para Blender que crean componentes con dimensiones estándar
- Modelos de resistores, condensadores, ICs, LEDs, conectores y PCBs
- Exportación a múltiples formatos (STL, OBJ, glTF, FBX)
- Integración con el formato .circuit.json

Ver `blender_models/README.md` y `docs/blender_usage_guide.md` para más información.

## Guías de Diseño EMI/Ruido
Documentación completa sobre cómo diseñar circuitos sin interferencias electromagnéticas:
- Principios de layout de PCB
- Técnicas de conexión a tierra
- Filtrado y desacoplamiento
- Separación de señales analógicas/digitales
- Estándares internacionales (FCC, CISPR)

Ver `docs/guidelines/emi_noise_prevention.md` para la guía completa.

## Exportación a Altium Designer
El proyecto incluye un adaptador completo para exportar circuitos a Altium Designer:

```bash
python3 adapters/circuit_to_altium.py examples/simple_circuit.circuit.json altium_export/
```

Genera archivos compatibles con Altium:
- Biblioteca de componentes (CSV)
- Netlist en formato Protel
- Bill of Materials (BOM)
- Coordenadas de colocación de componentes
- Reglas de diseño
- Guía de importación paso a paso

Ver `adapters/README.md` para más información.

## Cómo empezar (desarrolladores)
1. Clona el repo:
   git clone https://github.com/Blackmvmba88/circuit
2. Revisa `/examples` y `/specs` para entender el formato.
3. Añade componentes en `/components` o crea adaptadores en `/adapters`.

## Contribuir
Lee `CONTRIBUTING.md` y `CODE_OF_CONDUCT.md`. Usaremos PRs y ramas temáticas; puedes proponer mejoras en Issues o abrir PRs directamente.

## Licencia
MIT — ver `LICENSE`.

## Roadmap
Ver `ROADMAP.md` para las etapas planificadas.

---