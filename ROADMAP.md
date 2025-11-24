# Roadmap inicial

Fases propuestas:
1. ✅ Especificación del formato de archivo (v0.1) — objetivo: definir campos, validaciones y ejemplos.
2. ✅ Ejemplos y librería de componentes básicos — resistores, condensadores, fuentes y componentes lógicos.
3. ✅ Sistema de modelado 3D con Blender — generación automática de modelos de componentes.
4. ✅ Guías de diseño EMI/ruido — documentación completa sobre mejores prácticas.
5. ✅ **Adaptador para Altium Designer** — export completo a formato Altium con netlist, BOM, placement y guía de importación.
6. 🔄 Editor básico web y CLI (crear/editar/validar) — UI mínima para dibujar y JSON para guardar.
7. ⏳ Adaptadores de simulación (SPICE, Verilog) — export/import de formatos comunes.
8. ⏳ Adaptadores para otros EDA tools (KiCAD, EAGLE, EasyEDA).
9. ⏳ Sistema de plugins y marketplace de componentes.
10. ⏳ Integraciones con IDEs (extensión para VS Code) y plataformas colaborativas.

**Leyenda**: ✅ Completado | 🔄 En progreso | ⏳ Planeado

## Detalles de Integración con Altium

El adaptador para Altium Designer incluye:
- ✅ Exportación de biblioteca de componentes (CSV)
- ✅ Netlist en formato Protel (nativo de Altium)
- ✅ Bill of Materials con agrupación inteligente
- ✅ Coordenadas de colocación de componentes para PCB
- ✅ Dimensiones y especificaciones de la placa
- ✅ Reglas de diseño EMI/EMC traducidas a formato Altium
- ✅ Guía completa de importación paso a paso
- ✅ Mapeo automático de footprints estándar
- ✅ Formato de valores estándar (10K, 100nF, etc.)

Uso:
```bash
python3 adapters/circuit_to_altium.py examples/circuit_with_3d.circuit.json altium_export/
```

Cada fase se dividirá en issues y milestones; puedo crear esas issues automáticamente si quieres.

---