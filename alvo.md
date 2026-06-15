# 🎯 Alvo do Projeto — Placa Controladora de 6 Motores DC

Este documento descreve **aonde queremos chegar**: a placa a ser produzida, o
objetivo de usar **Claude Code + app Claude + Flux.ai** para projetá-la, e o
envio final para fabricação/montagem na **JLCPCB**.

---

## 1. Objetivo geral

Projetar, do zero, uma **placa de circuito impresso (PCB) controladora de 6
motores DC**, levá-la do conceito até os **arquivos de fabricação** e
**encomendar a produção + montagem (PCBA) na JLCPCB**.

O fluxo de trabalho pretendido é assistido por IA:

1. **Claude Code** (este agente) — pesquisa de componentes no catálogo da
   JLCPCB, dimensionamento (cálculos de calor, trilha, fusível, capacitor),
   geração de prompts/especificações e organização do repositório.
2. **App Claude (claude.ai) / trabalho colaborativo** — discussão de
   requisitos, revisão e decisões de projeto.
3. **Flux.ai (Flux Copilot)** — captura do esquemático e layout da PCB,
   guiado pelos prompts e pela especificação criados aqui.
4. **JLCPCB** — fabricação da placa e montagem dos componentes (SMT/PCBA) a
   partir dos Gerbers, BOM e arquivo Pick-and-Place.

> ⚠️ Observação importante: o roteamento de potência (alta corrente) e a
> verificação de footprints/pinos **exigem revisão humana** — o Flux Copilot
> acelera, mas não acerta tudo sozinho em uma placa de potência.

---

## 2. O que a placa deve fazer (especificação funcional)

- **Alimentação única de 12 V DC**, que alimenta **tanto os motores quanto o
  ESP32** (a partir de conversores na própria placa).
- **Microcontrolador:** módulo **ESP32-WROOM-32E** (Wi-Fi + Bluetooth).
- **6 motores DC** organizados em **4 canais de ponte H completa**
  (bidirecional — frente e ré), todos com **controle de velocidade por PWM**:
  - **Canal A:** 1 motor independente
  - **Canal B:** 1 motor independente
  - **Canal C:** 2 motores ligados em **paralelo** (curto-circuitados 2 a 2) na placa
  - **Canal D:** 2 motores ligados em **paralelo** na placa
- **Corrente:** 1–5 A por motor em 12 V (pico de partida/stall até ~3×).
  - Canais A e B: ~5 A contínuos
  - Canais C e D: ~10 A contínuos (par em paralelo)
  - **Todos os canais projetados para o pior caso: 10 A contínuos / 30 A de pico.**
- **Conexão dos motores:** conectores tipo **banana de 4 mm (≈3,9 mm)**, padrão
  doméstico, **2 por motor** (12 jacks no total), com codificação de cor.
- **Filtros, desacoplamento e proteções:** filtro de entrada/EMI, proteção
  contra inversão de polaridade, TVS, fusível, capacitores de bulk + cerâmicos,
  snubbers nas saídas dos motores.
- **Dissipação de calor:** polígonos de cobre + vias térmicas sob os MOSFETs
  (e provisão para dissipadores parafusáveis se necessário).
- **(Opcional, recomendado):** sensoriamento de corrente por canal para
  proteção de sobrecorrente via firmware.

---

## 3. Arquitetura de blocos (visão geral)

```
[12V IN] → Fusível → Proteção reversa → TVS → Filtro EMI → Bulk caps
   ├─→ Trilho 12V de potência → 4× Ponte H (IRF3205 + IR2104) → Motores (banana)
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
| Gate driver meia-ponte | IR2104 / IR2103 | C17701703 |
| Buck 12V→5V | MP1584EN | (a confirmar) |
| LDO 3,3V | AMS1117-3.3 | (a confirmar) |
| USB-Serial | CH340C | (a confirmar) |
| Botão | Tactile SMD | C318884 |

> A lista completa e os demais componentes pesquisados estão documentados ao
> longo do projeto; use a **skill `jlcpcb-catalog`** (ver `skills/`) para
> consultar estoque/preço/código atualizados.

---

## 5. Estado atual e próximos passos

**Já temos (neste repositório):**
- Este alvo (`alvo.md`)
- A skill de consulta ao catálogo da JLCPCB (`skills/jlcpcb-catalog/`)
- Os quatro dimensionamentos explicados (`dimensionamento/`)

**Próximos passos sugeridos:**
1. Fechar a **tabela final de dimensionamento** (valores por canal: 5 A e 10 A).
2. Validar a **pinagem do ESP32** (evitar pinos de strapping/boot).
3. Confirmar estoque/códigos LCSC das peças "a confirmar".
4. Conduzir o **Flux Copilot** bloco a bloco (esquemático → revisão →
   layout de potência manual → DRC).
5. Gerar **Gerbers + BOM + CPL** e enviar para a **JLCPCB**.

> ⚠️ Atenção de sistema: 6 motores × 5 A = **até 30 A** vindos da fonte de 12 V
> (≈ 360 W). Confirmar fonte, fusível (~40 A slow-blow), fiação (~12 AWG) e
> conector de entrada robusto.
