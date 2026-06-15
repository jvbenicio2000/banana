# BOM MÁXIMO-BASIC — Placa 6 Motores DC (2 A/motor, 6 A pico)

Variante com o **máximo de componentes Basic / Preferred** (sem taxa de feeder na
JLCPCB), mantendo **o ESP32** e o dimensionamento de **2 A contínuos / 6 A de
pico por motor**.

Para conseguir um **estágio de potência inteiramente Basic**, o projeto muda de
topologia:

- **Ponte H complementar discreta** (P-MOS high-side + N-MOS low-side) com peças
  **SOT-23 Basic** — não usa o gate driver IR2104 (que é Extended).
- **6 canais independentes** (1 ponte H por motor, **sem paralelismo**) — cada
  canal a 2 A / 6 A. (Na versão anterior, paralelizar criava canais de 4 A/12 A
  que exigiam MOSFETs de potência Extended.)

> ⚖️ **Trade-offs assumidos:** peças mais "leves" (SOT-23), maior contagem de
> componentes e P-MOS high-side um pouco menos eficiente. Veja `design-max-basic.md`
> para o esquema de drive, o sensoriamento de corrente e a câmera.

## ➕ Add-ons (a seu pedido): sensor de corrente + câmera

- **Sensor de corrente por canal:** 6× INA180 + 6× shunt 10 mΩ → ADC do ESP32
  (overcurrent por firmware, além do fusível). São peças **Extended**.
- **Câmera (sensor tipo câmera):** módulo **SPI ArduCAM OV2640** (externo, com
  FIFO/JPEG próprio — funciona sem PSRAM no WROOM-32E) plugado num **header 1×8**
  na placa (SPI + I²C/SCCB). O módulo em si é comprado à parte.
- **Expansor I²C PCA9555:** necessário para caber tudo nos pinos do ESP32 — leva
  os **sinais de direção dos motores** para o I²C, liberando GPIOs para a câmera.
  Ver `design-max-basic.md` (orçamento de pinos).

- **Consulta:** 2026-06-15. **B** = Basic, **P** = Preferred (ambos sem taxa).
- Quantidades de passivos são **aproximadas** (fecham no esquemático do Flux).

---

## ✅ Componentes SEM taxa de feeder (Basic / Preferred)

| Função | MPN | LCSC | Tipo | Encaps. | Qtd | Preço un. |
|---|---|---|---|---|---|---|
| MOSFET P high-side (ponte H) | AO3401A | **C15127** | B | SOT-23 | 12 | $0,053→0,028 |
| MOSFET N low-side (ponte H) | AO3400A | **C20917** | B | SOT-23 | 12 | $0,067→0,036 |
| NPN drive do high-side | MMBT3904 | **C20526** | B | SOT-23 | 12 | $0,008→0,004 |
| Proteção polaridade reversa (P-MOS ×4 paralelo) | AO3401A | **C15127** | B | SOT-23 | 4 | $0,053→0,028 |
| Buck 12V→5V (lógica) | TPS5430DDAR | **C9864** | B | SOIC-8-EP | 1 | $0,34→0,19 |
| Indutor do buck (~22µH)¹ | SDFL2012T220K | **C32375** | P | 0805 | 1 | $0,025→0,016 |
| Schottky catch do buck | SS54 | **C22452** | B | SMA | 1 | $0,040→0,018 |
| LDO 3,3V | AMS1117-3.3 | **C6186** | B | SOT-223 | 1 | $0,15→0,07 |
| TVS de surto | SMBJ16A | **C19077571** | P | SMB | 1 | $0,040→0,020 |
| Cerâmico bulk/decoupling 22µF | CL31A226KAHNNNE | **C12891** | B | 1206 | 4 | $0,037→0,019 |
| Cerâmico 10µF | CL21A106KAYNNNE | **C15850** | B | 0805 | 8 | $0,009→0,0045 |
| Cerâmico 100nF | CC0805KRX7R9BB104 | **C49678** | B | 0805 | ~32 | $0,0041→0,0021 |
| Resistor 10kΩ (gate/bias/pull) | 0805W8F1002T5E | **C17414** | B | 0805 | ~56 | $0,0016→0,0007 |
| Resistor 1kΩ (gate série/drive) | 0805W8F1001T5E | **C17513** | B | 0805 | ~14 | $0,0016→0,0008 |
| Botão tactile (BOOT/EN) | TS-1187A | **C318884** | B | SMD | 2 | $0,018→0,0095 |
| LED vermelho (power/status/6 canais) | NCD0805R1 | **C84256** | B | 0805 | 8 | $0,011→0,0053 |

¹ Confirmar a **corrente nominal** do indutor (o buck só alimenta a lógica,
~0,3–0,5 A); se o pico de Wi-Fi do ESP32 exigir, usar um indutor maior.

## ⚠️ Componentes que PERMANECEM Extended (sem equivalente Basic)

| Função | MPN | LCSC | Qtd | Motivo |
|---|---|---|---|---|
| MCU Wi-Fi/BT (você pediu p/ manter) | ESP32-WROOM-32E-N4 | **C701341** | 1 | Não há módulo Basic |
| USB-Serial | CH340C | **C7464026** | 1 | Sem opção Basic/Preferred |
| Conector USB-C | TYPE-C 16PIN 2MD | **C2765186** | 1 | Sem opção Basic/Preferred |
| Borne entrada 5,08 mm | WJ2EDGRC-5.08-2P | **C3697** | 1 | Sem opção Basic/Preferred |
| Suporte de fusível 5×20 | XC-7 | **C3131** | 1 | Sem opção Basic/Preferred |
| Bulk eletrolítico 470µF/25V² | CD2884771EM | **C2960233** | 10 | Eletrolíticos não têm Basic; valor **unificado** p/ usar só 1 feeder |
| Sense de corrente (1 por canal) | INA180A1IDBVR | **C122228** | 6 | Sem amplificador de corrente Basic |
| Shunt 10 mΩ 3W (1 por canal) | HoYLR2512-3W-10mR | **C5375464** | 6 | Sem shunt Basic |
| Expansor I²C (direção dos motores) | PCA9555PW | **C42420607** | 1 | Libera pinos do ESP32 p/ a câmera |
| Header 1×8 (câmera SPI ArduCAM) | 2.54-1×8P fêmea | **C27438** | 1 | Conector p/ módulo de câmera externo |

² Unifiquei o bulk em **um único valor (470 µF/25V)** — 4 na entrada + 6 nos
canais — para gastar **apenas uma** taxa de feeder de eletrolítico. (Trocar por
cerâmicos esbarra no *derating* por tensão DC a 12 V, que exigiria dezenas de
peças.)

---

## 🔩 Off-board / consumíveis

| Item | Qtd | Observação |
|---|---|---|
| Jacks banana 4 mm | 12 | Soldar à mão; não há no PCBA |
| Fusível 5×20 ~15 A slow-blow | 1 | Inserido no suporte `C3131` |
| Módulo de câmera SPI ArduCAM (OV2640) | 1 | Plugado no header 1×8; comprado à parte |

---

## 💰 Resultado em taxas de feeder

- **Estágio de potência:** 100% Basic (sem taxa). ✅
- **Tipos Extended (com taxa de feeder):** **10** — sendo 6 da base
  (ESP32, CH340C, USB-C, borne, suporte de fusível, eletrolítico) + 4 dos
  add-ons que você pediu (INA180, shunt, PCA9555, header da câmera).
- Mesmo assim, **bem menos** que a BOM discreta original (que tinha o estágio de
  potência todo Extended). Os 4 Extended dos add-ons são o custo das features
  (sensor de corrente + câmera).

---

## Pendências (afinar no Flux Copilot)

1. **Esquema de drive** da ponte H complementar (ver `design-max-basic.md`):
   pull-ups, divisores de gate (limitar Vgs do P-MOS a ~6 V) e anti-shoot-through.
2. **Feedback do TPS5430** (resistores p/ 5 V, Vref 1,221 V) — usar datasheet.
3. **Indutor do buck** — confirmar corrente/saturação.
4. **Pinagem ESP32**: agora são **12 sinais PWM** (2 por motor × 6) — checar
   GPIOs disponíveis e evitar strapping/boot (0/2/12/15).
5. **Térmico**: P-MOS de reverse (4× SOT-23) a 12 A dissipa ~2,4 W no total —
   usar pour de cobre generoso sob eles.
