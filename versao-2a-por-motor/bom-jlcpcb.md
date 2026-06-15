# BOM — Placa Controladora de 6 Motores DC (versão 2 A/motor — JLCPCB/PCBA)

Variante de **2 A por motor**. Levantada com a skill **`jlcpcb-catalog`**.
Mesma arquitetura discreta da versão 5 A, recalculada para **4 A cont. / 12 A
pico** por canal.

- **Consulta:** 2026-06-15 (estoque/preço variam — reconferir antes do pedido).
- **B** = Basic (sem taxa de feeder), **E** = Extended (~US$ 3/part).
- 🔻 = item que **mudou** em relação à versão 5 A.

---

## ✅ Componentes

| # | Função | MPN | LCSC | Encaps. | Qtd | Tipo | Preço un. | Estoque |
|---|---|---|---|---|---|---|---|---|
| 1 | MCU Wi-Fi/BT | ESP32-WROOM-32E-N4 | **C701341** | SMD 25,5×18 | 1 | E | $3,34→2,30 | 20.070 |
| 2 | MOSFET N (ponte H)¹ | IRF3205S-JSM | **C2874633** | TO-263 | 16 | E | $0,52→0,23 | 5.399 |
| 3 | Gate driver meia-ponte | IR2104STRPBF | **C2960** | SOIC-8 | 8 | E | $0,44→0,20 | 45.445 |
| 4 | Buck 12V→5V | MP1584EN-LF-Z | **C15051** | SOIC-8-EP | 1 | E | $3,05→2,18 | 3.341 |
| 5 | LDO 3,3V | AMS1117-3.3 | **C6186** | SOT-223 | 1 | B | $0,15→0,07 | 1,49 M |
| 6 | USB-Serial | CH340C | **C7464026** | SOP-16 | 1 | E | $0,56→0,31 | 40.915 |
| 7 | Sense de corrente | INA180A1IDBVR | **C122228** | SOT-23-5 | 4 | E | $0,14→0,07 | 55.410 |
| 8 | Proteção polaridade (P-MOS) | IRF4905STRLPBF | **C2620** | D2PAK | 1 | E | $0,83→0,41 | 9.543 |
| 9 | TVS surto | SMBJ16A | **C353386** | SMB | 1 | E | $0,034→0,015 | 36.998 |
| 10 🔻 | **Borne entrada 12V (5,08mm)** | WJ2EDGRC-5.08-2P | **C3697** | THT | 1 | E·THT | $0,038→0,020 | 102.961 |
| 11 🔻 | **Suporte de fusível 5×20** | XC-7 (BLX-A) | **C3131** | THT | 1 | E·THT | $0,062→0,035 | 133.949 |
| 12 | Diodo bootstrap | US1M | **C412437** | SMA | 8 | B | $0,010→0,0045 | 503.541 |
| 13 | Schottky roda-livre | SS54 | **C22452** | SMA | 8 | B | $0,040→0,018 | 541.319 |
| 14 🔻 | Bulk entrada 1000µF/25V | 01EC4294 | **C503217** | THT D10×16 | 2 | E·THT | $0,058→0,033 | 57.882 |
| 15 | Bulk por canal 470µF/25V | CD2884771EM | **C2960233** | THT D8×12 | 4 | E·THT | $0,038→0,019 | 45.962 |
| 16 | Cerâmico 10µF | CL21A106KAYNNNE | **C15850** | 0805 | 8 | B | $0,009→0,0045 | 12,7 M |
| 17 | Cerâmico 22µF | CL31A226KAHNNNE | **C12891** | 1206 | 2 | B | $0,037→0,019 | 3,2 M |
| 18 | Cerâmico 100nF | CC0805KRX7R9BB104 | **C49678** | 0805 | 30 | B | $0,0041→0,0021 | 15,7 M |
| 19 | Gate 22Ω | RC0805FR-0722RL | **C107702** | 0805 | 16 | E | $0,0019→0,0010 | 146.763 |
| 20 | Pull-down/up 10kΩ | 0805W8F1002T5E | **C17414** | 0805 | 20 | B | $0,0016→0,0007 | 15,4 M |
| 21 🔻 | **Shunt 10mΩ 3W** | HoYLR2512-3W-10mR | **C5375464** | 2512 | 4 | E | $0,052→0,024 | 84.918 |
| 22 | Conector USB-C | TYPE-C 16PIN 2MD | **C2765186** | SMD | 1 | E | $0,058→0,032 | 735.053 |
| 23 | Botão tactile (BOOT/EN) | TS-1187A | **C318884** | SMD | 2 | B | $0,018→0,0095 | 918.009 |
| 24 | LED vermelho | NCD0805R1 | **C84256** | 0805 | 6 | B | $0,011→0,0053 | 7,2 M |

¹ A 4 A o IRF3205 está **super-dimensionado** (perda ~0,24 W). Mantido por ser
barato/robusto; poderia ser um MOSFET menor se quiser otimizar.

### Decisões / diferenças vs. versão 5 A
- **Fusível:** ✅ **volta para a placa** (suporte 5×20 `C3131` + fusível ~15 A
  slow-blow inserido) — possível porque a corrente caiu para ~12 A.
- **Borne de entrada:** 5,08 mm (`C3697`) no lugar do 7,62 mm.
- **Shunt:** 10 mΩ (melhor resolução: 12 A → ~2,4 V no ADC).
- **Bulk de entrada:** 2× 1000 µF (em vez de 3×).
- **Choke de modo comum:** continua **omitido**.
- **PCB:** 1 oz / 2 camadas / **sem dissipador** (ver `dimensionamento/`).

---

## 🔩 Itens off-board / consumíveis

| Item | Descrição | Qtd | Observação |
|---|---|---|---|
| Jacks banana 4 mm | Fêmea painel/PCB, vermelho/preto | 12 | Não há no catálogo PCBA; soldar à mão |
| Fusível 5×20 ~15 A slow-blow | Elemento de vidro/cerâmico | 1 | Consumível inserido no suporte `C3131` (não montado pela JLCPCB) |

---

## 💰 Estimativa de custo (componentes, por placa)

- **Componentes (qty baixa):** ≈ **US$ 22 / placa** (parecido com a versão 5 A,
  pois mantém os mesmos ICs). **A economia real vem da PCB**: 1 oz em vez de 2 oz,
  2 camadas, **sem dissipadores**, placa menor e fonte 12 V/15 A bem mais barata.
- Economia total estimada no conjunto **placa + montagem + fonte: ~30–50%**.

*(Não inclui PCB, banana jacks, fusível, frete e impostos.)*

---

## Pendências de engenharia (afinar no Flux, ver `dimensionamento/`)

1. **Passivos do buck MP1584** (indutor ~10–22 µH, diodo catch, feedback).
2. **Resistor do snubber RC** nas saídas (~10 Ω/1 W) + 100 nF.
3. **Pinagem ESP32** (evitar GPIO 0/2/12/15).
4. Conferir o térmico (a 4 A, dispensa dissipador — `dimensionamento/1`).
