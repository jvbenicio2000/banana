# Prompt de Engenharia — Placa Controladora de 6 Motores DC (versão 2 A/motor)

Especificação para uma IA de projeto de PCB gerar o esquemático, layout e BOM,
pronta para fabricação/montagem na **JLCPCB**. Variante de **2 A por motor**.

> Premissas: motores de **2 A** contínuos em 12 V, controle **bidirecional
> (ponte H)**, **todos os canais com PWM**. São **4 canais de ponte H** (2
> motores independentes + 2 pares em paralelo). Pior caso por canal:
> **4 A contínuos / 12 A de pico**.

---

## PROMPT (copiar e colar)

```markdown
# PAPEL
Você é um engenheiro eletrônico sênior especialista em projeto de PCB para
fabricação na JLCPCB (PCBA / montagem SMT). Projete o esquemático completo,
o layout da PCB e a BOM de uma placa controladora de 6 motores DC.

# OBJETIVO
Uma placa pronta para fabricação (PCBA na JLCPCB) que controla 6 motores DC
escovados a partir de uma ÚNICA fonte de 12 V, com um ESP32 fazendo o
controle por PWM. Inclua filtros, desacoplamentos, proteções e térmico
corretos para operação confiável.

# REQUISITOS FUNCIONAIS
1. Alimentação única de 12 V DC que alimenta TANTO os motores QUANTO o ESP32.
2. Microcontrolador: módulo ESP32-WROOM-32E (LCSC C701341).
3. Controle de motores via 4 canais de PONTE H completa (bidirecional) com PWM
   de velocidade em TODOS os canais:
   - Canal A: 1 motor independente
   - Canal B: 1 motor independente
   - Canal C: 2 motores ligados em PARALELO na placa
   - Canal D: 2 motores ligados em PARALELO na placa
   Total: 6 motores físicos, 4 canais de acionamento.
4. Corrente por motor: 2 A contínuos @12V (pico de partida/stall até ~3x = 6A).
   Portanto, dimensione:
   - Canais A e B: ~2 A contínuos, pico ~6 A
   - Canais C e D (par em paralelo): ~4 A contínuos, pico ~12 A
   Para uniformidade, projete TODOS os 4 canais idênticos para o pior caso
   (4 A contínuos / 12 A de pico).
5. Conexão dos motores: 12 conectores tipo BANANA fêmea de 4 mm, 2 por motor,
   com codificação vermelho/preto. O paralelismo 2-a-2 (C e D) é feito nas trilhas.
6. Entrada de 12 V: borne parafuso 5,08 mm com FUSÍVEL na placa (~15 A slow-blow)
   e proteção contra inversão de polaridade (P-MOSFET).
7. Programação do ESP32: USB-C + CH340C com auto-reset (transistores para
   EN/BOOT) e botões BOOT e EN/RESET.

# ARQUITETURA / BLOCOS
[Entrada 12V] → Fusível (~15A) → Proteção reversa (P-MOSFET) → TVS → filtro de
entrada → Capacitores de bulk
   ├─→ Trilho 12V de potência → 4× Ponte H → Motores (banana)
   └─→ Buck 12V→5V (MP1584EN) → LDO AMS1117-3.3 para o ESP32

[ESP32] → 8 GPIOs PWM (2 por ponte H: IN1/IN2) → Gate drivers → MOSFETs

# COMPONENTES OBRIGATÓRIOS (usar peças da biblioteca JLCPCB)
- MCU: ESP32-WROOM-32E (C701341)
- Ponte H (por canal, ×4):
    - 4× MOSFET N IRF3205S TO-263 SMD (C2874633) — super-dimensionado p/ 4A, ok
    - 2× gate driver meia-ponte IR2104 (C2960) com bootstrap
    - diodos de bootstrap, resistores de gate (22 Ω) e pull-downs (10 kΩ)
- Alimentação lógica: buck 12V→5V (MP1584EN) + LDO AMS1117-3.3
- USB-serial: CH340C + USB-C
- Sinalização: LED de power, LED de status, 1 LED por canal
- Botão de reset: tactile SMD (C318884)

# FILTROS, DESACOPLAMENTO E TÉRMICO
1. Entrada: fusível ~15A 5×20 na placa, TVS (SMBJ16A), bulk eletrolítico
   (1000 µF/25V) + cerâmicos 100 nF.
2. Por ponte H: bulk local (220–470 µF/25V) próximo aos MOSFETs; cerâmicos
   100 nF; rede SNUBBER RC + 100 nF cerâmico em cada saída de motor.
3. ESP32: 100 nF + 10 µF próximos ao módulo; bulk de 22 µF no 3,3 V.
4. Gate drivers: capacitor de bootstrap correto + cerâmica de desacoplamento.
5. TÉRMICO:
   - A 4 A contínuos a perda por MOSFET é ~0,24 W → SEM dissipador, apenas pour
     de cobre modesto + algumas vias térmicas.
   - Cobre de 1 oz é suficiente; trilhas de potência ~2,5 mm (4 A) e curtas/largas
     nos picos (12 A).
6. Sensoriamento de corrente (opcional): shunt 10 mΩ + INA180 por canal, lido
   pelo ADC do ESP32 (12 A → ~2,4 V, boa resolução).

# RESTRIÇÕES DE FABRICAÇÃO (JLCPCB)
- Priorizar SMD; preferir peças "Basic".
- PCB de 2 camadas, cobre 1 oz é suficiente.
- Larguras de trilha por IPC-2221: ~2,5 mm para 4 A; picos de 12 A curtos/largos.
- Espaçamento/folga adequados para 12 V/12 A.
- Separar PGND e AGND com ponto único (star ground).
- Mapear PWM em GPIOs válidos (evitar boot/strapping 0/2/12/15).

# ENTREGÁVEIS
1. Esquemático por blocos. 2. Layout com pours e vias. 3. BOM com LCSC e qtds.
4. Gerber + BOM (.csv) + Pick&Place (CPL) no formato JLCPCB.
5. Tabela de pinagem ESP32 → função. 6. Notas de montagem/uso.

# SEGURANÇA E VALIDAÇÃO
- Proteção contra curto (fusível na placa), inversão de polaridade e
  sobrecorrente (INA180 + firmware).
- Estime a dissipação dos MOSFETs a 4 A (confirme que dispensa dissipador).
- Liste premissas e pontos a confirmar.
```

---

## Pontos de atenção

- **Paralelizar 2 motores** só é seguro com motores **idênticos**.
- **Corrente total:** 6 × 2 A = **até 12 A** (≈ 144 W). Fonte 12 V/15 A, fio
  ~16 AWG e fusível ~15 A slow-blow já cobrem.
- A 2 A o IRF3205 está super-dimensionado — alternativamente caberia um MOSFET
  menor/mais barato, ou CIs de ponte H integrados (ver `README.md`).
- Cálculos em `dimensionamento/`.
