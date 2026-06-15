# Roteiro Flux.ai (Flux Copilot) — Placa de 6 Motores (versão 2 A/motor)

O **Flux Copilot não monta tudo de uma vez**: trabalha passo a passo e fica
melhor quando você dá o contexto primeiro e constrói **bloco por bloco**.
O Flux busca por **MPN (código do fabricante)**, não pelo código LCSC.

Cole os blocos abaixo no Flux Copilot, **na ordem**, conferindo cada etapa.
Esta é a variante de **2 A por motor** (placa mais simples: 1 oz, 2 camadas,
sem dissipador, fusível na placa).

---

## ETAPA 0 — Contexto do projeto (cole PRIMEIRO)

```
I'm designing a 6-DC-motor controller board for manufacturing at JLCPCB (SMT assembly).
Please remember these project goals and constraints throughout our conversation:

GOAL: A single-board controller powered by ONE 12V DC supply that feeds both the
motors and an ESP32. The ESP32 drives 4 full H-bridge channels with PWM:
- Channel A: 1 independent motor
- Channel B: 1 independent motor
- Channel C: 2 motors wired in PARALLEL on the board
- Channel D: 2 motors wired in PARALLEL on the board
(6 physical motors, 4 drive channels.)

ELECTRICAL: Each motor 2A continuous @12V (stall up to ~3x = 6A). Design all 4
channels identically for the worst case: 4A continuous / 12A peak per channel.
System total ~12A from the 12V supply (~144W).

PREFERENCES:
- Prefer SMD parts available on JLCPCB; give manufacturer part numbers (MPN).
- 2-layer board, 1oz copper is sufficient at this current.
- Robust filtering, decoupling, reverse-polarity & overcurrent protection. An
  on-board ~15A slow-blow fuse fits at this current. No heatsinks needed.
Acknowledge and propose a system-level block architecture before we build anything.
```

## ETAPA 1 — Arquitetura

```
Propose the full block diagram and a bill of materials skeleton for this board.
Use a discrete MOSFET H-bridge (IRF3205S + IR2104 gate driver) per channel,
sized for 4A continuous / 12A peak (over-spec but cheap/robust). Power chain:
12V input → on-board fuse (~15A) → reverse-polarity P-MOSFET → TVS → bulk caps →
(a) 12V power rail to H-bridges, (b) buck 12V→5V (MP1584EN) → LDO AMS1117-3.3 for
the ESP32. List the GPIO budget.
```

## ETAPA 2 — Alimentação e proteção

```
Build the power input and protection block: a 5.08mm screw terminal for 12V in,
an on-board 5x20 fuse holder (~15A slow-blow), a P-channel MOSFET reverse-polarity
protection, an SMBJ16A TVS, and bulk electrolytic (1000uF/25V) + 100nF ceramics.
Then add an MP1584EN buck to 5V and an AMS1117-3.3 LDO to 3.3V, each with proper
input/output caps. Give MPNs.
```

## ETAPA 3 — ESP32 + programação

```
Add an ESP32-WROOM-32E module with full decoupling (100nF + 10uF at the module,
22uF bulk on 3.3V), EN pull-up + RC, BOOT and EN/RESET tactile buttons, and a
USB-C + CH340C USB-UART with the standard two-transistor auto-reset circuit for
EN/IO0. Map 8 PWM-capable GPIOs (avoid strapping/boot pins) to drive 4 H-bridges
(IN1/IN2 each). Show me the pin-mapping table.
```

## ETAPA 4 — Uma ponte H (modelo) → replicar 4×

```
Design ONE full H-bridge channel rated for 4A continuous / 12A peak from 12V:
- 4x IRF3205S N-MOSFETs (TO-263)
- 2x IR2104 half-bridge gate drivers with bootstrap diode + bootstrap cap
- gate resistors (22 ohm) and gate pull-downs (10k)
- local bulk cap (220-470uF/25V) + 100nF decoupling
- an RC snubber + 100nF ceramic across the motor output
Driven by 2 PWM inputs from the ESP32. Make it a reusable block, then replicate
it 4 times as channels A, B, C, D.
```

## ETAPA 5 — Conectores banana + paralelismo

```
Add motor connectors: 12x 4mm banana jacks (PCB/panel mount), two per motor,
red/black coded. Channels A and B each go to one motor. For channels C and D,
wire the two banana-jack pairs in PARALLEL on the board. Keep these power traces
short and wide (~2.5mm for 4A in 1oz copper).
```

## ETAPA 6 — Proteção/sensoriamento (opcional, recomendado)

```
Add per-channel current sensing: a low-side 10mohm shunt + INA180 amplifier
feeding the ESP32 ADC (12A peak -> ~2.4V), for overcurrent protection in firmware.
Add a power LED, a status LED, and one LED per channel.
```

## ETAPA 7 — Layout e térmico

```
Now help with PCB layout: place the H-bridge MOSFETs over modest copper pours with
a few thermal vias; at 4A continuous the MOSFET loss is only ~0.24W so NO heatsink
is needed. Use 1oz copper, 2 layers, traces ~2.5mm for 4A (IPC-2221), separate
power ground (PGND) and signal ground (AGND) joined at a star point. Run DRC.
```

## ETAPA 8 — Exportar para a JLCPCB

```
Generate JLCPCB-ready manufacturing outputs: Gerbers, BOM (.csv with LCSC part
numbers), and the Pick-and-Place / CPL file. Flag any parts without a JLCPCB
match so I can substitute them.
```

---

## Dicas do Flux Copilot

- **Uma etapa por vez** e confira cada bloco antes de seguir.
- Se ele escolher uma peça ruim: *"replace with a JLCPCB Basic part, give the LCSC code"*.
- Para valores (bootstrap, snubber): *"reference the datasheet"*.
- Ao fim de cada etapa: *"review this block for errors before continuing"*.

## Onde o Flux costuma errar (revisar à mão)

| Tarefa | Confiança | Ação |
|---|---|---|
| Esquemático / topologia | Boa | Aproveitar |
| Escolha de peças | Média | Conferir rating e estoque na JLCPCB |
| Footprints | Média | **Validar pinagem contra o datasheet** |
| Pinos do ESP32 | Média | Evitar GPIO de boot/strapping (0/2/12/15) |
| Roteamento de potência | Média | A 12 A é bem mais tranquilo que na versão 30 A |
| Térmico | Boa | A 2 A dispensa dissipador (ver `dimensionamento/`) |

> Estratégia: Copilot faz o **esquemático** → você revisa
> **peças/footprints/pinos** → layout → DRC. Prototipe **1 canal** antes dos 4.
