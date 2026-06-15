# BOM — Placa Controladora de 6 Motores DC (JLCPCB / PCBA)

Lista de materiais levantada com a skill **`jlcpcb-catalog`**
(`python3 skills/jlcpcb-catalog/scripts/search.py …`), consultando a biblioteca
de montagem da JLCPCB/LCSC.

- **Estoque/preço:** consultados em 2026-06-15 (variam — reconfira antes do pedido).
- **Arquitetura:** 4 canais de ponte H idênticos (10 A cont. / 30 A pico),
  ESP32-WROOM-32E, alimentação única 12 V. Ver `alvo.md` e `prompt-placa-motores.md`.
- Preços = faixa unitária (menor qty → maior qty).

---

## 1. Núcleo / ICs

| # | Função | MPN | LCSC | Encaps. | Qtd | Estoque | Preço un. |
|---|---|---|---|---|---|---|---|
| 1 | MCU Wi-Fi/BT | ESP32-WROOM-32E-N4 | **C701341** | SMD 25,5×18 | 1 | 20.070 | $2,30–3,34 |
| 2 | MOSFET N de potência (ponte H) | IRF3205S-JSM | **C2874633** | TO-263 | 16 | 5.399 | $0,23–0,52 |
| 3 | Gate driver meia-ponte | IR2104STRPBF | **C2960** | SOIC-8 | 8 | 45.445 | $0,20–0,44 |
| 4 | Buck 12V→5V | MP1584EN-LF-Z | **C15051** | SOIC-8-EP | 1 | 3.341 | $2,18–3,05 |
| 5 | LDO 3,3V | AMS1117-3.3 | **C6186** | SOT-223 | 1 | 1,49 M | $0,07–0,15 |
| 6 | USB-Serial | CH340C | **C7464026** | SOP-16 | 1 | 40.915 | $0,31–0,56 |
| 7 | Sense de corrente (por canal) | INA180A1IDBVR | **C122228** | SOT-23-5 | 4 | 55.410 | $0,07–0,14 |

> Ponte H: 4 MOSFET + 2 drivers **por canal** × 4 canais = **16 IRF3205S + 8 IR2104**.

## 2. Proteção / entrada

| # | Função | MPN | LCSC | Encaps. | Qtd | Estoque | Preço un. |
|---|---|---|---|---|---|---|---|
| 8 | Proteção polaridade reversa (P-MOSFET) | IRF4905STRLPBF | **C2620** | D2PAK | 1 | 9.543 | $0,41–0,83 |
| 9 | TVS supressor surto | SMBJ16A | **C353386** | SMB | 1 | 36.998 | $0,015–0,034 |
| 10 | Choke de modo comum (EMI) | 744223 (Würth) | **C5289492** | SMD-4P | 1 | 940 | $0,79–1,42 |
| 11 | Borne parafuso 5,08 mm 2P (12V in) | WJ2EDGRC-5.08-2P | **C3697** | P=5,08 | 1 | 102.961 | $0,02–0,04 |
| 12 | Suporte de fusível 5×20 | XC-7 (BLX-A) | **C3131** | THT | 1 | 133.949 | $0,035–0,062 |

## 3. Diodos

| # | Função | MPN | LCSC | Encaps. | Qtd | Estoque | Preço un. |
|---|---|---|---|---|---|---|---|
| 13 | Diodo de bootstrap (rápido) | US1M | **C412437** | SMA | 8 | 503.541 | $0,0045–0,010 |
| 14 | Schottky roda-livre (opcional) | SS54 | **C22452** | SMA | 8 | 541.319 | $0,018–0,040 |

## 4. Capacitores

| # | Função | MPN | LCSC | Encaps. | Qtd | Estoque | Preço un. |
|---|---|---|---|---|---|---|---|
| 15 | Bulk entrada 1000µF/25V | 01EC4294 | **C503217** | THT D10×16 | 2–3 | 57.882 | $0,033–0,058 |
| 16 | Bulk por canal 470µF/25V | KF471M025F | **C59352** | THT D8×11,5 | 4 | 64.776 | $0,038–0,082 |
| 17 | Cerâmico 10µF 0805 (bulk lógica) | CL21A106KAYNNNE | **C15850** | 0805 | ~8 | 12,7 M | $0,0045–0,009 |
| 18 | Cerâmico 22µF 1206 (3,3V) | CL31A226KAHNNNE | **C12891** | 1206 | 1–2 | 3,2 M | $0,019–0,037 |
| 19 | Cerâmico 100nF 0805 (decoupling) | CC0805KRX7R9BB104 | **C49678** | 0805 | ~30 | 15,7 M | $0,002–0,004 |

## 5. Resistores

| # | Função | MPN | LCSC | Encaps. | Qtd | Estoque | Preço un. |
|---|---|---|---|---|---|---|---|
| 20 | Gate 22 Ω (por MOSFET) | RC0805FR-0722RL | **C107702** | 0805 | 16 | 146.763 | $0,001–0,002 |
| 21 | Pull-down/pull-up 10 kΩ | 0805W8F1002T5E | **C17414** | 0805 | ~20 | 15,4 M | $0,0007–0,0016 |
| 22 | Shunt de corrente 5 mΩ 3W 2512 | HoJLR2512-3W-5mR | **C2903482** | 2512 | 4 | 73.573 | $0,043–0,079 |

## 6. Interface / sinalização

| # | Função | MPN | LCSC | Encaps. | Qtd | Estoque | Preço un. |
|---|---|---|---|---|---|---|---|
| 23 | Conector USB-C (programação) | TYPE-C 16PIN 2MD(073) | **C2765186** | SMD | 1 | 735.053 | $0,032–0,058 |
| 24 | Botão tactile SMD (BOOT/EN) | TS-1187A | **C318884** | SMD 5,1×5,1 | 2 | 918.009 | $0,010–0,018 |
| 25 | LED 0805 (power/status/canal) | XL-2012SURC (vermelho) | **C965812** | 0805 | ~7 | 2,0 M | $0,003–0,005 |

---

## ⚠️ Itens que exigem decisão / não saem do catálogo PCBA

1. **Conectores banana 4 mm (12×).** A biblioteca de montagem da JLCPCB **não
   tem** jacks banana de painel adequados (são peças mecânicas de furo passante,
   normalmente soldadas à mão). Mais próximos no catálogo: *binding posts*
   `C106273 / C106272`. **Recomendação:** comprar os 12 jacks à parte e montá-los
   manualmente; deixar furos/footprint na placa.
2. **Fusível de alta corrente.** O sistema chega a ~30 A (6×5 A). O suporte 5×20
   (`C3131`) e fusíveis de vidro **não** aguentam isso — use um **fusível tipo
   lâmina (ATO/MIDI) ~40 A slow-blow** com suporte próprio (fora do PCBA).
3. **Choke de modo comum `744223`** tem corrente nominal baixa para 30 A —
   reavaliar/escolher um choke de potência adequado ou suprimir o filtro CM.
4. **IRF3205S é 55 V/Rds(on)≈8 mΩ.** Confira o cálculo térmico em
   `dimensionamento/1-calor-mosfet.md` para 10 A contínuos (pour de cobre + vias).
5. Peças **THT** (eletrolíticos, borne, suporte de fusível) têm custo de solda
   manual na JLCPCB — considere versões SMD se quiser PCBA 100% automático.

---

### Como reproduzir / atualizar esta lista

```bash
# exemplos (skill jlcpcb-catalog):
python3 skills/jlcpcb-catalog/scripts/search.py "IRF3205S"
python3 skills/jlcpcb-catalog/scripts/search.py "IR2104" --limit 5
python3 skills/jlcpcb-catalog/scripts/search.py "AMS1117-3.3" --json
```
