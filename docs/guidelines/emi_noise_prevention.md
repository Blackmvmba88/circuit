# Guía de Prevención de Interferencias Electromagnéticas (EMI) y Ruido en Circuitos

## Introducción

Esta guía proporciona las mejores prácticas para diseñar circuitos electrónicos que minimicen las interferencias electromagnéticas (EMI) y el ruido eléctrico. Seguir estas reglas es esencial para crear circuitos confiables y compatibles con estándares internacionales.

---

## 1. Principios Fundamentales de EMI

### 1.1 Fuentes de EMI
- **Radiación electromagnética**: Generada por señales de alta frecuencia y transiciones rápidas
- **Acoplamiento conductivo**: Transmitido a través de cables de alimentación y señales
- **Acoplamiento capacitivo**: Entre pistas paralelas y componentes cercanos
- **Acoplamiento inductivo**: Bucles de corriente grandes y cables no apantallados

### 1.2 Modos de Interferencia
- **Modo común**: Corriente que fluye en la misma dirección en múltiples conductores
- **Modo diferencial**: Corriente que fluye en direcciones opuestas entre conductores

---

## 2. Reglas de Diseño de PCB

### 2.1 Distribución de Capas

**Para PCB de 2 capas:**
- Capa superior: Señales y componentes
- Capa inferior: Plano de tierra continuo y pistas de señal críticas

**Para PCB de 4 capas (recomendado):**
```
Capa 1: Señales de alta velocidad
Capa 2: Plano de tierra (GND)
Capa 3: Plano de alimentación (VCC/VDD)
Capa 4: Señales de baja velocidad y retorno
```

**Para PCB de 6+ capas:**
- Alternar capas de señal con planos de tierra/alimentación
- Mantener planos de referencia continuos

### 2.2 Planos de Tierra

#### Reglas Críticas:
1. **Plano continuo**: Evitar dividir el plano de tierra
2. **Conexión de múltiples puntos**: En alta frecuencia (>1MHz)
3. **Punto único de tierra**: Solo para audio analógico y DC
4. **Vías de tierra abundantes**: 
   - Mínimo cada 6mm en áreas críticas
   - Cada 3mm cerca de componentes de alta frecuencia
5. **Área de bucle mínima**: Mantener trazas de señal/retorno juntas

```
CORRECTO:                    INCORRECTO:
Component                    Component
    |                            |
  Signal ———→                  Signal ————————→
    ↓                                          ↓
  GND ←———————                              GND ←——
(bucle pequeño)              (bucle grande - genera EMI)
```

### 2.3 Ancho y Separación de Pistas

#### Anchos de Pista Recomendados:
| Corriente | Ancho Mínimo (1oz Cu) | Ancho Recomendado |
|-----------|----------------------|-------------------|
| < 0.5A    | 0.25mm (10mil)       | 0.3mm (12mil)     |
| 0.5-1A    | 0.4mm (16mil)        | 0.5mm (20mil)     |
| 1-2A      | 0.8mm (32mil)        | 1.0mm (40mil)     |
| 2-3A      | 1.5mm (60mil)        | 2.0mm (80mil)     |

#### Separaciones (Clearance):
- **Señales normales**: 0.2mm (8mil) mínimo
- **Señales de alta tensión (>50V)**: 0.5mm+ según voltaje
- **Impedancia controlada**: Calculada según stackup
- **Entre señales rápidas**: 3x el ancho de pista

### 2.4 Reglas de Enrutamiento

#### Señales de Alta Velocidad:
```python
# Criterio de señal de alta velocidad:
# Si tiempo_de_subida < 2 × tiempo_de_propagación_de_pista
# Entonces requiere técnicas de alta velocidad

# Ejemplo:
rise_time = 2e-9  # 2ns
trace_length = 0.05  # 5cm
propagation_speed = 1.5e8  # 15cm/ns en FR4
prop_time = trace_length / propagation_speed

if rise_time < 2 * prop_time:
    print("Requiere diseño de alta velocidad")
```

**Técnicas:**
1. **Impedancia controlada**: 50Ω para señales diferenciales
2. **Longitudes pareadas**: ±0.5mm para pares diferenciales
3. **Sin stubs**: Eliminar trazas muertas
4. **Terminación adecuada**: Serie, paralelo o Thevenin según aplicación

#### Ángulos de Pista:
- **Evitar ángulos de 90°**: Usar 45° o curvas suaves
- **Razón**: Los ángulos agudos causan reflexiones y aumentan EMI

```
CORRECTO:         INCORRECTO:
    /                 |
   /                  |___
  /                       |
```

---

## 3. Colocación de Componentes

### 3.1 Proximidad y Agrupación

**Regla General**: Minimizar longitudes de pista entre componentes relacionados

#### Circuitos de Alimentación:
```
Fuente → Filtro EMI → Regulador → Condensador Bulk → IC
         (10-100mm)   (5-10mm)    (< 5mm)
```

#### Desacoplamiento de IC:
- **Condensador 100nF**: ≤ 5mm del pin de alimentación del IC
- **Condensador 10µF**: ≤ 10mm del IC
- **Vías a tierra**: Directamente desde pads del condensador

### 3.2 Zonas Funcionales

Dividir el PCB en zonas:
1. **Zona de alimentación**: Reguladores, filtros
2. **Zona digital**: Microcontroladores, lógica
3. **Zona analógica**: Amplificadores, ADC/DAC
4. **Zona RF** (si aplica): Separada con guardia de tierra

**Separación entre zonas:**
- Digital ↔ Analógica: > 10mm
- RF ↔ Digital: > 15mm
- Alta potencia ↔ Señales sensibles: > 20mm

### 3.3 Orientación de Componentes

```
Flujo de señal direccional:
Entrada → Procesamiento → Salida
(izquierda a derecha, sin cruces de pistas)
```

---

## 4. Técnicas de Filtrado y Desacoplamiento

### 4.1 Condensadores de Desacoplamiento

**Estrategia Múltiple:**
```
Para cada IC:
- 1× 100nF (0805 o 0603 cerámico X7R) - HF
- 1× 10µF (electrolítico o cerámico) - MF
- 1× 100µF (bulk, por cada 4-5 ICs) - LF
```

**Colocación:**
```
     VCC pin
        |
     ------- (Condensador 100nF)
        |
       GND
     (vía directa al plano)
```

### 4.2 Filtros de Alimentación

#### Ferrite Beads:
- **Impedancia**: 30-120Ω @ 100MHz
- **Corriente nominal**: > 120% de corriente máxima
- **Uso**: Entre diferentes dominios de alimentación

#### Filtro π (Pi):
```
VCC_in ——[Ferrite]——+——[Inductor]——+—— VCC_out
                    |              |
                   [C1]           [C2]
                    |              |
                   GND            GND

C1 = 10-47µF (entrada)
L = 10-100µH (filtro)
C2 = 10-100µF (salida)
```

### 4.3 Circuitos de Protección

**Entrada de Alimentación:**
```
VCC_ext ——[Fusible]——[Varistor]——[Diodo TVS]——[Filtro EMI]—— VCC_int
                         |             |
                        GND           GND
```

---

## 5. Cableado y Conectores

### 5.1 Cables y Longitudes

**Reglas:**
1. **Cables cortos**: Minimizar longitud (< 1m si es posible)
2. **Cables trenzados**: Para señales diferenciales (ej: RS-485, CAN)
3. **Cables apantallados**: Para señales sensibles o ambientes ruidosos
4. **Apantallamiento conectado**:
   - Un extremo para DC/baja frecuencia
   - Ambos extremos para alta frecuencia

### 5.2 Conectores

**Tipos recomendados:**
- **Señales digitales**: IDC, pin headers con paso 2.54mm
- **Alimentación**: Conectores de bloque de terminales atornillados
- **Alta frecuencia**: SMA, MCX, U.FL (con impedancia controlada)

**Prácticas:**
- Pin de tierra cada 3-5 pines de señal en conectores multi-pin
- Conectores de montaje superficial con múltiples pines de tierra

---

## 6. Consideraciones de Señales Específicas

### 6.1 Relojes y Osciladores

**Crítico para EMI:**
```
Ubicación del Cristal:
- < 10mm del pin de entrada del IC
- Plano de tierra sólido debajo
- Guard ring de tierra alrededor
- Sin pistas cruzando debajo

Osciladores:
- Usar osciladores con spread spectrum si es posible
- Filtrar salida de reloj si va a otros bloques
```

### 6.2 Comunicación Digital de Alta Velocidad

#### I2C/SPI:
- Resistencias pull-up cerca del maestro
- 22-100Ω en serie en MOSI/MISO para señales rápidas

#### UART/RS-232:
- Condensadores de 10-100pF cerca de los pines TX/RX
- Ferrite beads si el cable sale del PCB

#### USB:
- Impedancia diferencial 90Ω (±10%)
- Longitudes pareadas (< 0.5mm diferencia)
- Plano de tierra sólido debajo de las pistas

### 6.3 Circuitos Analógicos

**Reglas de Oro:**
1. **Plano de tierra analógico separado**: Conectado en un solo punto
2. **Alimentación analógica limpia**: Filtrada desde digital
3. **Guarda de tierra**: Alrededor de trazas sensibles
4. **Evitar señales digitales**: Cerca de nodos de alta impedancia

```
Layout Amplificador:
         GND Guard Ring
    +----------------------+
    |   Vin+    Vout      |
    |     \      |         |
    |      [AMP]-+         |
    |     /               |
    |   Vin-              |
    +----------------------+
         (tierra sólida)
```

---

## 7. Técnicas Avanzadas

### 7.1 Apantallamiento (Shielding)

**Caja metálica completa:**
- Conectar a tierra del PCB en múltiples puntos
- Usar juntas de EMI en aberturas
- Material: Aluminio o acero inoxidable

**Shields locales en PCB:**
- Latas metálicas sobre circuitos críticos
- Soldadas al plano de tierra con múltiples puntos
- Ejemplo: Shields para módulos WiFi/Bluetooth

### 7.2 Guard Rings y Guard Traces

```
Guard Ring alrededor de señal sensible:
    
    GND GND GND GND GND
    GND ========== GND  ← Guard Traces
    GND |  Signal | GND
    GND ========== GND
    GND GND GND GND GND
    
(Conectar guard ring a GND con vías cada 3-5mm)
```

### 7.3 Stitching Vias

**Propósito**: Conectar planos de tierra en PCB multicapa

**Ubicación:**
- Perímetro del PCB: cada 10-15mm
- Áreas de alta velocidad: cada 3-5mm
- Cerca de conectores: cada 5mm
- A lo largo de cambios de capa de señal

---

## 8. Testing y Validación

### 8.1 Pruebas Pre-Certificación

**Equipo básico:**
1. **Near-field probe**: Detectar puntos calientes de EMI
2. **Osciloscopio**: Verificar integridad de señal y ringing
3. **Analizador de espectro**: Medir emisiones radiadas

**Procedimiento:**
```
1. Escaneo con near-field probe sobre el PCB
2. Identificar frecuencias problemáticas
3. Correlacionar con señales de reloj/switching
4. Aplicar correcciones: filtros, ferrite beads, condensadores
5. Re-test
```

### 8.2 Checklist de Diseño

Antes de fabricar:
- [ ] Todos los ICs tienen condensadores de desacoplamiento (100nF + 10µF)
- [ ] Plano de tierra continuo sin divisiones grandes
- [ ] Señales de reloj < 10mm, sin stubs
- [ ] Pares diferenciales con longitudes pareadas
- [ ] Filtros EMI en entradas de alimentación
- [ ] Circuitos analógicos separados de digitales
- [ ] Guard rings alrededor de señales sensibles
- [ ] Stitching vias cada 10mm en perímetro
- [ ] Ángulos de pista 45° o curvas suaves
- [ ] Ancho de pista adecuado para corriente

---

## 9. Estándares y Normativas

### 9.1 Emisiones Radiadas

**FCC Part 15 (USA):**
- Clase A (industrial): Límites menos estrictos
- Clase B (residencial): Límites más estrictos

**CISPR 22 / EN 55022 (Europa):**
- Equivalente a FCC Part 15

**Frecuencias críticas:**
- 30 MHz - 1 GHz: Más restrictivo
- Picos armónicos de relojes suelen causar problemas

### 9.2 Inmunidad

**IEC 61000-4:**
- 4-2: Descarga electrostática (ESD)
- 4-3: Campos electromagnéticos radiados
- 4-4: Transitorios rápidos (burst)
- 4-5: Sobretensiones (surge)

---

## 10. Ejemplos de Implementación

### Ejemplo 1: Microcontrolador con Comunicación SPI

```
[MCU]——(100nF)——GND
  |
  VCC——[Ferrite 47Ω]——VCC_ext
  
  SCK ——[22Ω]—— SCK_out
  MOSI——[22Ω]—— MOSI_out
  MISO<————————— MISO_in
  CS ——————————— CS_out
  
  (Condensadores de desacoplamiento: < 5mm del MCU)
  (Resistencias en serie: para reducir ringing)
```

### Ejemplo 2: Circuito de Switching (Buck Converter)

```
VIN ——[C_in]——[Switch]——[L]——+——[C_out]—— VOUT
              |              |      |
              |              |    [RC Snubber]
              |              |      |
             GND            GND    GND

Notas críticas:
- Loop de alta frecuencia: Switch-L-C_out-GND lo más pequeño posible
- C_in cerca del switch (< 5mm)
- C_out cerca de la carga
- Plano de tierra bajo todo el circuito
- Considerar guard ring si hay señales sensibles cercanas
```

### Ejemplo 3: Layout de ADC de Precisión

```
Plano de tierra analógico (AGND):
    +----[Sensor]----[Filter]----[ADC]----+
    |                                     |
   AGND ←—————————————————————————→ AGND
                     |
                  [Ferrite]
                     |
                   DGND (plano digital)

- Conexión de punto único: AGND y DGND unidos solo bajo el ADC
- Alimentación analógica filtrada con ferrite + condensadores
- Pistas analógicas rodeadas de guardia de tierra
```

---

## 11. Recursos Adicionales

### Libros Recomendados:
- "EMC for Product Designers" - Tim Williams
- "High Speed Digital Design" - Howard Johnson
- "Signal and Power Integrity Simplified" - Eric Bogatin

### Herramientas de Software:
- **Altium Designer**: DRC para EMI
- **KiCAD**: Plugin EMC checker
- **HyperLynx**: Simulación de integridad de señal
- **CST Studio**: Simulación electromagnética 3D

### Sitios Web:
- https://www.analog.com/en/design-center/design-tools-and-calculators.html
- https://www.ti.com/lit/an/slyt670/slyt670.pdf
- https://www.onsemi.com/support/design-tools

---

## Conclusión

El diseño de circuitos con baja EMI y ruido requiere atención a múltiples aspectos: layout del PCB, selección de componentes, filtrado adecuado y técnicas de conexión a tierra. Seguir estas guías desde el inicio del diseño evitará costosos rediseños y problemas de certificación.

**Regla de oro**: Es mucho más fácil y económico diseñar correctamente desde el principio que solucionar problemas de EMI después de fabricar el PCB.

---

*Documento creado para el proyecto "circuit"*
*Última actualización: 2025-11-24*
