# 🎯 Alvo do Projeto — Placa Controladora de 6 Motores DC (versão 2 A/motor)

Variante de **baixa corrente** (2 A por motor) do projeto. Mesmo objetivo da
versão 5 A — projetar a placa do zero, levá-la aos arquivos de fabricação e
encomendar a produção/montagem (PCBA) na **JLCPCB** — porém dimensionada para
motores de **2 A contínuos**, o que deixa a placa **mais simples e barata**.

---

## 1. Objetivo geral

Projetar uma **PCB controladora de 6 motores DC** (2 A/motor), do conceito até
os arquivos de fabricação, usando o fluxo assistido por IA:

1. **Claude Code** — pesquisa de componentes (skill `jlcpcb-catalog`),
   dimensionamento e organização do repositório.
2. **App Claude** — discussão de requisitos e revisão.
3. **Flux.ai (Flux Copilot)** — esquemático e layout, guiado pelos prompts daqui.
4. **JLCPCB** — fabricação + montagem (SMT/PCBA).

> ⚠️ O roteamento de potência e a verificação de footprints/pinos ainda exigem
> revisão humana — mas a 2 A a complexidade térmica/de potência é bem menor.

---

## 2. O que a placa deve fazer (especificação funcional)

- **Alimentação única de 12 V DC**, que alimenta tanto os motores quanto o ESP32.
- **Microcontrolador:** módulo **ESP32-WROOM-32E** (Wi-Fi + Bluetooth).
- **6 motores DC** em **4 canais de ponte H completa** (bidirecional), todos com
  **PWM de velocidade**:
  - **Canal A:** 1 motor independente
  - **Canal B:** 1 motor independente
  - **Canal C:** 2 motores em **paralelo** (curto-circuitados 2 a 2) na placa
  - **Canal D:** 2 motores em **paralelo** na placa
- **Corrente:** **2 A por motor** em 12 V (pico de partida/stall até ~3× ≈ 6 A).
  - Canais A e B: ~2 A contínuos (pico ~6 A)
  - Canais C e D (par em paralelo): ~4 A contínuos (pico ~12 A)
  - **Todos os canais projetados para o pior caso: 4 A contínuos / 12 A de pico.**
- **Conexão dos motores:** conectores **banana de 4 mm**, 2 por motor (12 jacks),
  com codificação de cor.
- **Filtros, desacoplamento e proteções:** filtro de entrada, proteção contra
  inversão de polaridade, TVS, **fusível na placa (~15 A)**, bulk + cerâmicos,
  snubbers nas saídas.
- **Dissipação:** polígonos de cobre — **sem dissipadores** (perda por MOSFET
  ~0,24 W; ver `dimensionamento/1`).
- **(Opcional, recomendado):** sensoriamento de corrente por canal (shunt 10 mΩ +
  INA180) para proteção via firmware.

---

## 3. Arquitetura de blocos (visão geral)

```
[12V IN] → Fusível (~15A) → Proteção reversa → TVS → Filtro entrada → Bulk caps
   ├─→ Trilho 12V → 4× Ponte H (IRF3205 + IR2104) → Motores (banana)
   └─→ Buck 12V→5V → LDO 5V→3,3V → ESP32 + lógica

[ESP32] → 8 GPIOs PWM (2 por ponte H) → Gate drivers → MOSFETs
        → (opcional) ADC ← sensores de corrente por canal
```

---

## 4. Componentes-chave (catálogo JLCPCB)

| Função | Sugestão | Código LCSC |
|---|---|---|
| MCU + Wi-Fi | ESP32-WROOM-32E | C701341 |
| MOSFET de potência | IRF3205S (TO-263 SMD) | C2874633 |
| Gate driver meia-ponte | IR2104 | C2960 |
| Buck 12V→5V | MP1584EN | C15051 |
| LDO 3,3V | AMS1117-3.3 | C6186 |
| USB-Serial | CH340C | C7464026 |
| Sense de corrente | INA180A1 | C122228 |
| Shunt | 10 mΩ 3W 2512 | C5375464 |
| Borne entrada 5,08 mm | WJ2EDGRC-5.08-2P | C3697 |
| Suporte de fusível 5×20 | XC-7 | C3131 |
| Botão | Tactile SMD | C318884 |

> A 2 A o IRF3205 fica **super-dimensionado** (sobra enorme) — mantido por ser
> barato e robusto. Lista completa em `bom-jlcpcb.md` / `bom-jlcpcb.csv`.

---

## 5. Estado atual e próximos passos

**Já temos (nesta pasta):** alvo, prompt, roteiro Flux, dimensionamentos e BOM,
todos recalculados para 2 A.

**Próximos passos:**
1. Validar a **pinagem do ESP32** (evitar GPIOs de strapping/boot).
2. Confirmar estoque/códigos LCSC na hora do pedido.
3. Conduzir o **Flux Copilot** bloco a bloco (esquemático → revisão → layout → DRC).
4. Gerar **Gerbers + BOM + CPL** e enviar para a **JLCPCB**.

> ⚠️ Atenção de sistema: 6 motores × 2 A = **até 12 A** vindos da fonte de 12 V
> (≈ 144 W). Fonte 12 V/15 A, fio ~16 AWG e o fusível de ~15 A já dão conta.
