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
- Librería de componentes básicos (resistores, condensadores, fuentes, puertas lógicas)

## Formato de archivo (breve)
Usaremos JSON con:
- metadata: nombre, autor, versión, fecha
- components: lista con ids, tipo, parámetros, posición
- nets: conexiones entre pines
- sim_config (opcional): parámetros de simulación

Ejemplo: ver `examples/simple_circuit.circuit.json`.

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