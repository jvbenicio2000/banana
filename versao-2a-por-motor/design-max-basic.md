# Nota de projeto — Ponte H complementar (versão máximo-Basic)

Por que e como o estágio de potência muda na BOM `bom-jlcpcb-max-basic.md`.

## Por que mudar a topologia

A ponte H "padrão" do projeto usa **MOSFETs de potência N (IRF3205) + gate
driver IR2104** — peças **Extended** (com taxa de feeder) e **sem equivalente
Basic** na JLCPCB. Para zerar a taxa no estágio de potência, trocamos por uma
**ponte H complementar discreta**, que só usa peças **Basic SOT-23**.

## Como funciona (por canal/motor)

Cada motor tem uma ponte H com 4 MOSFETs (2 "pernas"):

```
        +12V
         │
    ┌────┴────┐
   [P]       [P]      ← AO3401A (high-side, P-MOS)
    │         │
    ├──MOTOR──┤        (saída A) ── (saída B)
    │         │
   [N]       [N]      ← AO3400A (low-side, N-MOS)
    └────┬────┘
        GND
```

- **Low-side (N-MOS AO3400A):** o gate é acionado **direto por um GPIO do ESP32**
  (3,3 V já liga o AO3400A; para 2 A a Rds fica baixa o suficiente). Resistor de
  **pull-down 10 k** mantém desligado no boot + **série 1 k** opcional.
- **High-side (P-MOS AO3401A):** a fonte está em 12 V; para ligar é preciso puxar
  o gate **abaixo** de 12 V. Um **NPN MMBT3904** faz esse "level-shift":
  - **Pull-up 10 k** do gate do P-MOS para +12 V → mantém **desligado** em repouso.
  - O GPIO liga o NPN (via **base 10 k**); o NPN puxa o gate através de um
    **divisor 10 k/10 k**, fixando **Vgs ≈ −6 V** — liga o P-MOS **sem passar do
    limite ±12 V** do AO3401A.

> ⚠️ **Anti-shoot-through:** nunca ligar P e N da **mesma perna** juntos. O
> firmware (e/ou um pequeno dead-time) garante isso. Para PWM + sentido, acionam-se
> os pares **diagonais** (P de um lado + N do outro).

## Controle / GPIOs

- **2 sinais por motor** (IN1/IN2) → **12 sinais** para 6 motores.
- O ESP32-WROOM-32E tem GPIOs suficientes, mas **valide a pinagem** (evitar
  strapping/boot 0/2/12/15 e pinos só-entrada 34–39).

## Proteção de polaridade reversa (também Basic)

Sem o IRF4905 (Extended), usamos **4× AO3401A em paralelo** no positivo de 12 V
(gate por divisor 10 k/10 k → Vgs ≈ −6 V). Em ~12 A do sistema, a perda total é
~2,4 W repartida nos 4 SOT-23 → **pour de cobre generoso** sob eles.

## Limitações aceitas

- **Sem sensor de corrente** (INA180 é Extended) → proteção fica no **fusível
  ~15 A** na placa. Dá para reativar o sensoriamento depois (aí volta 1 Extended).
- Peças SOT-23 são para **2 A/6 A por motor** — **não** suportam o paralelismo de
  4 A/12 A; por isso esta variante é **6 canais independentes**.
- P-MOS high-side tem Rds maior que N-MOS → leve perda extra (ok em 2 A).
