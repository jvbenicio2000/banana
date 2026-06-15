# BOM FINAL — Placa Controladora de 6 Motores DC (JLCPCB / PCBA)

Lista de materiais **aprovada componente a componente** usando a skill
**`jlcpcb-catalog`** (`python3 skills/jlcpcb-catalog/scripts/search.py …`).

- **Consulta:** 2026-06-15 (estoque/preço variam — reconferir antes do pedido).
- **Arquitetura:** 4 canais de ponte H discreta idênticos (10 A cont. / 30 A pico),
  ESP32-WROOM-32E, alimentação única 12 V. Ver `alvo.md` / `prompt-placa-motores.md`.
- **Preço un.** = faixa (menor qty → maior qty). **B** = Basic (sem taxa de feeder),
  **E** = Extended (taxa única ~US$ 3/part).

---

## ✅ Componentes aprovados

| # | Função | MPN | LCSC | Encaps. | Qtd | Tipo | Preço un. | Estoque |
|---|---|---|---|---|---|---|---|---|
| 1 | MCU Wi-Fi/BT | ESP32-WROOM-32E-N4 | **C701341** | SMD 25,5×18 | 1 | E | $3,34→2,30 | 20.070 |
| 2 | MOSFET N (ponte H) | IRF3205S-JSM | **C2874633** | TO-263 | 16 | E | $0,52→0,23 | 5.399 |
| 3 | Gate driver meia-ponte | IR2104STRPBF | **C2960** | SOIC-8 | 8 | E | $0,44→0,20 | 45.445 |
| 4 | Buck 12V→5V | MP1584EN-LF-Z | **C15051** | SOIC-8-EP | 1 | E | $3,05→2,18 | 3.341 |
| 5 | LDO 3,3V | AMS1117-3.3 | **C6186** | SOT-223 | 1 | B | $0,15→0,07 | 1,49 M |
| 6 | USB-Serial | CH340C | **C7464026** | SOP-16 | 1 | E | $0,56→0,31 | 40.915 |
| 7 | Sense de corrente | INA180A1IDBVR | **C122228** | SOT-23-5 | 4 | E | $0,14→0,07 | 55.410 |
| 8 | Proteção polaridade (P-MOS) | IRF4905STRLPBF | **C2620** | D2PAK | 1 | E | $0,83→0,41 | 9.543 |
| 9 | TVS surto | SMBJ16A | **C353386** | SMB | 1 | E | $0,034→0,015 | 36.998 |
| 11 | Borne entrada 12V (7,62mm) | KF7.62-2P | **C707824** | THT | 1 | E·THT | $0,095→0,057 | 51.552 |
| 13 | Diodo bootstrap | US1M | **C412437** | SMA | 8 | B | $0,010→0,0045 | 503.541 |
| 14 | Schottky roda-livre | SS54 | **C22452** | SMA | 8 | B | $0,040→0,018 | 541.319 |
| 15 | Bulk entrada 1000µF/25V | 01EC4294 | **C503217** | THT D10×16 | 3 | E·THT | $0,058→0,033 | 57.882 |
| 16 | Bulk por canal 470µF/25V | CD2884771EM | **C2960233** | THT D8×12 | 4 | E·THT | $0,038→0,019 | 45.962 |
| 17 | Cerâmico 10µF | CL21A106KAYNNNE | **C15850** | 0805 | 8 | B | $0,009→0,0045 | 12,7 M |
| 18 | Cerâmico 22µF | CL31A226KAHNNNE | **C12891** | 1206 | 2 | B | $0,037→0,019 | 3,2 M |
| 19 | Cerâmico 100nF | CC0805KRX7R9BB104 | **C49678** | 0805 | 30 | B | $0,0041→0,0021 | 15,7 M |
| 20 | Gate 22Ω | RC0805FR-0722RL | **C107702** | 0805 | 16 | E | $0,0019→0,0010 | 146.763 |
| 21 | Pull-down/up 10kΩ | 0805W8F1002T5E | **C17414** | 0805 | 20 | B | $0,0016→0,0007 | 15,4 M |
| 22 | Shunt 5mΩ 3W | HoYLR2512-3W-5mR | **C5375461** | 2512 | 4 | E | $0,049→0,023 | 21.286 |
| 23 | Conector USB-C | TYPE-C 16PIN 2MD | **C2765186** | SMD | 1 | E | $0,058→0,032 | 735.053 |
| 24 | Botão tactile (BOOT/EN) | TS-1187A | **C318884** | SMD | 2 | B | $0,018→0,0095 | 918.009 |
| 25 | LED vermelho | NCD0805R1 | **C84256** | 0805 | 6 | B | $0,011→0,0053 | 7,2 M |

### Decisões registradas
- **#10 Choke de modo comum:** ❌ **omitido** (EMI tratada por bulk caps + snubbers + layout).
- **#12 Fusível na placa:** ❌ **omitido** — proteção de sobrecorrente via **firmware** (INA180 + corte de PWM).

---

## 🔩 Itens off-board (comprar/montar à parte — não saem do PCBA)

| Item | Descrição | Qtd | Observação |
|---|---|---|---|
| Jacks banana 4 mm | Fêmea painel/PCB, vermelho/preto | 12 | Não há no catálogo de montagem; soldar à mão / footprint na placa |
| Suporte de fusível inline + fusível | Lâmina ATO/MIDI ~40 A slow-blow | 1 | **Rede de segurança física** na fonte (ver aviso abaixo) |
| Dissipadores (se usar TO-220) | Parafusáveis | — | Provisão de furos no layout |

> ⚠️ **Aviso de segurança:** com o fusível removido da placa (decisão #12), o
> firmware **não** protege contra curto franco (MOSFET em curto / falha de
> fiação). É **fortemente recomendado** um fusível físico (~40 A) na fonte de
> 12 V como rede de segurança contra fogo em 30 A.

---

## 💰 Estimativa de custo (componentes, por placa)

- **Componentes (qty baixa):** ≈ **US$ 22 / placa** (cai com volume).
- **Itens dominantes:** ESP32 (~$3,3), 16× IRF3205S (~$8,3), MP1584 (~$3,0),
  8× IR2104 (~$3,5).
- **Taxas de setup (uma vez):** ~14 peças **Extended** → taxa de feeder
  (~US$ 3 cada, parte pode ser grátis dependendo da promo JLCPCB).
- **Solda manual (THT):** borne 7,62 + 3× 1000µF + 4× 470µF têm custo de
  montagem manual adicional.

*(Não inclui PCB, banana jacks, fusível externo, frete e impostos.)*

---

## Pendências de engenharia (afinar no Flux Copilot, ver `dimensionamento/`)

1. **Passivos do buck MP1584** (indutor ~10–22 µH, diodo catch, resistores de
   feedback p/ 5 V) — dimensionar pelo datasheet.
2. **Resistor do snubber RC** nas saídas de motor (ex.: ~10 Ω / 1 W) + o 100 nF.
3. **Tabela de pinagem ESP32** (evitar GPIO 0/2/12/15 de strapping/boot).
4. **Cálculo térmico** dos IRF3205S a 10 A (pour de cobre + vias) — ver
   `dimensionamento/1-calor-mosfet.md`.

---

### Reproduzir / atualizar
```bash
python3 skills/jlcpcb-catalog/scripts/search.py "IRF3205S"
python3 skills/jlcpcb-catalog/scripts/search.py "IR2104" --json
```
