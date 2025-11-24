# Checklist de Diseño de PCB para Reducción de EMI/Ruido

Use esta lista de verificación antes de enviar su diseño a fabricación para asegurar que sigue las mejores prácticas de EMI/ruido.

## 📋 Verificación Pre-Fabricación

### 1. Plano de Tierra ⚡
- [ ] El plano de tierra es continuo y sin divisiones grandes
- [ ] No hay islas de tierra aisladas
- [ ] Vías de conexión a tierra cada 6-10mm en perímetro del PCB
- [ ] Plano de tierra cubre al menos 80% del área del PCB
- [ ] Si hay múltiples planos de tierra (analógico/digital), están unidos en UN solo punto

### 2. Alimentación 🔌
- [ ] Condensadores de bulk (10-100µF) en la entrada de alimentación
- [ ] Filtro de entrada (ferrite bead o inductor) después del condensador de entrada
- [ ] Trazas de alimentación con ancho adecuado para la corriente:
  - [ ] < 0.5A: mínimo 0.3mm
  - [ ] 0.5-1A: mínimo 0.5mm
  - [ ] 1-2A: mínimo 1.0mm
  - [ ] > 2A: cálculo térmico específico
- [ ] Condensador de salida después de cada regulador

### 3. Desacoplamiento de ICs 🔲
Para CADA circuito integrado:
- [ ] Condensador 100nF cerámico (X7R o X5R) dentro de 5mm del pin VCC
- [ ] Condensador adicional 10µF si el IC es de alta velocidad o consume > 50mA
- [ ] Vías directas desde pads del condensador al plano de tierra (< 2mm)
- [ ] Sin trazas largas entre VCC del IC y el condensador
- [ ] Condensador bulk (100µF) compartido cada 4-5 ICs

### 4. Señales de Alta Velocidad ⚡
Aplicable si tiempo_de_subida < 10ns o frecuencia > 50MHz:
- [ ] Impedancia controlada (típicamente 50Ω single-ended, 90Ω differential)
- [ ] Pistas lo más cortas posible (< 5cm si es factible)
- [ ] Plano de referencia continuo debajo de las pistas
- [ ] Sin stubs (trazas muertas) > 1mm
- [ ] Longitudes pareadas para pares diferenciales (diferencia < 0.5mm)
- [ ] Terminación adecuada en extremo receptor o transmisor
- [ ] Separación 3x el ancho de pista entre señales rápidas

### 5. Relojes y Osciladores ⏱️
- [ ] Cristal/oscilador a < 10mm del pin de entrada del IC
- [ ] Plano de tierra sólido directamente debajo del cristal
- [ ] Guard ring de tierra conectado con vías cada 3-5mm
- [ ] Condensadores de carga (si aplica) cerca de los pines del cristal
- [ ] Sin pistas no relacionadas cruzando debajo o cerca del cristal
- [ ] Señal de reloj terminada si va a más de un destino

### 6. Trazado de Pistas 🛤️
- [ ] Ángulos de 45° o curvas suaves (no ángulos de 90°)
- [ ] Área de bucle mínima (señal y retorno lo más cercanos posible)
- [ ] Pistas paralelas largas (> 5cm) separadas al menos 3x su ancho
- [ ] Pistas de potencia/señal no corren paralelas por largas distancias
- [ ] Cambios de capa minimizados para señales críticas

### 7. Separación de Dominios 🔀
- [ ] Circuitos analógicos separados de digitales (> 10mm si es posible)
- [ ] Circuitos de alta potencia separados de señales sensibles (> 20mm)
- [ ] Módulos RF (si aplica) con guard ring y separación > 15mm
- [ ] Flujo de señal unidireccional sin cruces (entrada → procesamiento → salida)

### 8. Conectores y Cables 🔌
- [ ] Pin de tierra cada 3-5 pines de señal en conectores multi-pin
- [ ] Conectores de potencia con múltiples pines de tierra
- [ ] Filtros cerca de conectores que van a cables externos
- [ ] Protección ESD en pines expuestos (diodos TVS o varistores)

### 9. Componentes Críticos 🎯

#### Reguladores de Voltaje:
- [ ] Condensador de entrada (10µF) a < 5mm del pin de entrada
- [ ] Condensador de salida (10-100µF) a < 10mm del pin de salida
- [ ] Resistor de feedback (si aplica) lo más cerca posible

#### Circuitos de Switching (Buck/Boost):
- [ ] Loop de alta frecuencia (switch-inductor-cap-gnd) LO MÁS PEQUEÑO POSIBLE
- [ ] Condensadores de entrada/salida con baja ESR
- [ ] Snubber RC si hay ringing visible
- [ ] Plano de tierra sólido debajo de todo el circuito

#### ADC/DAC de Precisión:
- [ ] Plano de tierra analógico separado, unido en un punto
- [ ] Alimentación analógica filtrada (ferrite + condensadores)
- [ ] Guard traces alrededor de señales analógicas sensibles
- [ ] Sin señales digitales cerca de nodos de alta impedancia

### 10. Revisión de Layout 👁️
- [ ] Simulación de integridad de señal para pistas críticas (opcional pero recomendado)
- [ ] DRC (Design Rule Check) pasado sin errores
- [ ] ERC (Electrical Rule Check) pasado sin errores
- [ ] Revisión visual del layout completo
- [ ] Verificación de orientación de componentes polarizados (LEDs, electrolíticos, ICs)
- [ ] Verificación de footprints de componentes vs datasheets
- [ ] Referencias de componentes (R1, C2, etc.) visibles y legibles

### 11. Capa de Silkscreen 🖨️
- [ ] Referencias de componentes no cubiertas por los componentes mismos
- [ ] Indicadores de polaridad claros (LEDs, condensadores electrolíticos, diodos)
- [ ] Pin 1 de ICs claramente marcado
- [ ] Voltajes de alimentación etiquetados
- [ ] Información del proyecto: nombre, versión, fecha

### 12. Fabricación 🏭
- [ ] Clearances cumplen con capacidades del fabricante (típicamente ≥ 0.15mm)
- [ ] Ancho mínimo de pista cumple especificaciones (típicamente ≥ 0.15mm)
- [ ] Tamaño de vías dentro de especificaciones (drill ≥ 0.3mm)
- [ ] Máscara de soldadura y pasta están correctamente definidas
- [ ] Archivos Gerber generados y revisados con visor

### 13. Testing y Validación 🧪
Post-fabricación:
- [ ] Inspección visual de la placa fabricada
- [ ] Test de continuidad para nets críticos
- [ ] Test de aislamiento entre nets
- [ ] Medición de voltajes de alimentación antes de colocar ICs
- [ ] Escaneo con near-field probe (si disponible) para puntos calientes de EMI
- [ ] Medición de formas de onda en osciloscope para verificar integridad de señal

---

## 🎯 Niveles de Cumplimiento

### Nivel Básico (Obligatorio)
Completar al menos estas secciones:
- ✅ 1. Plano de Tierra
- ✅ 2. Alimentación
- ✅ 3. Desacoplamiento de ICs
- ✅ 10. Revisión de Layout

### Nivel Intermedio (Recomendado)
Todo lo anterior más:
- ✅ 4. Señales de Alta Velocidad (si aplica)
- ✅ 6. Trazado de Pistas
- ✅ 7. Separación de Dominios
- ✅ 8. Conectores y Cables

### Nivel Avanzado (Profesional)
Todo lo anterior más:
- ✅ 5. Relojes y Osciladores
- ✅ 9. Componentes Críticos
- ✅ 13. Testing y Validación

---

## 📝 Notas Adicionales

### Frecuencias Críticas a Revisar
Verificar que no hay componentes resonantes o bucles grandes en estas frecuencias:
- 30-88 MHz (FM radio)
- 88-108 MHz (FM broadcast)
- 174-230 MHz (TV broadcast)
- 470-890 MHz (TV/UHF)
- 2.4 GHz (WiFi, Bluetooth)

### Herramientas Recomendadas
- **Layout**: KiCAD, Altium, Eagle
- **Simulación**: LTSpice, HyperLynx
- **Visualización Gerber**: Gerbv, KiCAD Gerber Viewer
- **EMI Testing**: Near-field probe, spectrum analyzer

### Recursos
- **Guía completa EMI**: `docs/guidelines/emi_noise_prevention.md`
- **Estándares**: FCC Part 15, CISPR 22/32, IEC 61000-4-x
- **Calculadoras online**: 
  - Saturn PCB Toolkit (ancho de pistas)
  - EEWeb (impedancia controlada)

---

## ✅ Certificación de Revisión

**Proyecto**: ___________________________
**Diseñador**: ___________________________
**Revisor**: ___________________________
**Fecha**: ___________________________

**Nivel de cumplimiento**: [ ] Básico [ ] Intermedio [ ] Avanzado

**Observaciones**:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

**Aprobado para fabricación**: [ ] Sí [ ] No [ ] Con modificaciones

---

*Documento creado para el proyecto "circuit"*
*Última actualización: 2025-11-24*
