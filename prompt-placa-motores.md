# Prompt de Engenharia — Placa Controladora de 6 Motores DC

Especificação completa para uma IA de projeto de PCB gerar o esquemático,
layout e BOM da placa, pronta para fabricação/montagem na **JLCPCB**.

> Premissas confirmadas: motores de **1–5 A** em 12 V, controle **bidirecional
> (ponte H)**, **todos os canais com PWM**. São **4 canais de ponte H** (2
> motores independentes + 2 pares de motores em paralelo). Todos os canais
> dimensionados para o pior caso: **10 A contínuos / 30 A de pico**.

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
controle por PWM. A placa deve incluir todos os filtros, desacoplamentos,
proteções e dissipadores de calor corretos para operação confiável.

# REQUISITOS FUNCIONAIS
1. Alimentação única de 12 V DC que alimenta TANTO os motores QUANTO o ESP32.
2. Microcontrolador: módulo ESP32-WROOM-32E (LCSC C701341).
3. Controle de motores via 4 canais de PONTE H completa (bidirecional,
   frente/ré) com PWM de velocidade em TODOS os canais:
   - Canal A: 1 motor independente
   - Canal B: 1 motor independente
   - Canal C: 2 motores ligados em PARALELO (curto-circuitados 2 a 2) na placa
   - Canal D: 2 motores ligados em PARALELO na placa
   Total: 6 motores físicos, 4 canais de acionamento.
4. Corrente por motor: 1–5 A contínuos em 12 V (pico de partida/stall até ~3x).
   Portanto, dimensione:
   - Canais A e B: ~5 A contínuos, pico ~15 A
   - Canais C e D (par em paralelo): ~10 A contínuos, pico ~30 A
   Para uniformidade, projete TODOS os 4 canais idênticos para o pior caso
   (10 A contínuos / 30 A de pico).
5. Conexão dos motores: 12 conectores tipo BANANA fêmea de 4 mm (≈3,9 mm),
   PCB/painel, 2 por motor (6 motores × 2), com codificação de cor
   vermelho/preto por motor. O paralelismo 2-a-2 dos canais C e D é feito
   internamente nas trilhas da placa.
6. Entrada de 12 V: conector dedicado (borne parafuso 5,08 mm OU 2 jacks
   banana) com fusível e proteção contra inversão de polaridade.
7. Programação do ESP32: USB-C + conversor USB-serial CH340C com auto-reset
   (transistores para EN/BOOT) e botões BOOT e EN/RESET.

# ARQUITETURA / BLOCOS
[Entrada 12V] → Fusível → Proteção reversa (P-MOSFET) → TVS → Filtro EMI
(choke modo comum + LC) → Capacitores de bulk
   ├─→ Trilho 12V de potência → 4× Ponte H → Motores (banana)
   └─→ Buck 12V→5V → LDO 5V→3,3V → ESP32 + lógica

[ESP32] → 8 GPIOs PWM (2 por ponte H: IN1/IN2) → Gate drivers → MOSFETs

# COMPONENTES OBRIGATÓRIOS (usar peças da biblioteca JLCPCB)
- MCU: ESP32-WROOM-32E (C701341)
- Ponte H (por canal, ×4):
    - 4× MOSFET N IRF3205S TO-263/D2PAK SMD (C2874633)
    - 2× gate driver meia-ponte IR2104/IR2103 (C17701703) com bootstrap
    - Diodos de bootstrap, resistores de gate (10–47 Ω) e pull-downs (10 kΩ)
- Alimentação lógica: buck 12V→5V (MP1584/MP2315) + LDO AMS1117-3.3
- USB-serial: CH340C + USB-C
- Sinalização: LED de power, LED de status, 1 LED por canal
- Botão de teste/reset: tactile SMD (C318884)

# FILTROS, DESACOPLAMENTO E TÉRMICO (CRÍTICO)
1. Entrada: fusível, TVS (SMBJ série), capacitores de bulk eletrolíticos
   (ex.: 1000 µF/25V) + cerâmicos 100 nF; choke de modo comum para EMI.
2. Por ponte H: capacitor de bulk local (470–1000 µF/25V) próximo aos
   MOSFETs; cerâmicos 100 nF de desacoplamento; rede SNUBBER RC + capacitor
   cerâmico (100 nF) através de cada saída de motor para suprimir transientes
   indutivos; diodos de roda-livre Schottky se necessário (além do corpo do MOSFET).
3. ESP32: 100 nF + 10 µF próximos ao módulo; bulk de 10–22 µF;
   desacoplamento dedicado no trilho 3,3 V.
4. Gate drivers: capacitor de bootstrap correto, cerâmica de desacoplamento
   junto ao VCC de cada driver.
5. TÉRMICO / DISSIPADORES:
   - MOSFETs SMD (TO-263) sobre amplo POUR de cobre com muitas VIAS TÉRMICAS
     para a camada inferior/plano; áreas de dissipação dimensionadas para
     10 A contínuos por canal.
   - Trilhas de potência largas, cobre de 2 oz, ou polígonos de potência.
   - Prever espaço/furos para dissipadores parafusáveis caso a versão TO-220
     seja escolhida.
6. Sensoriamento de corrente (opcional, recomendado): shunt + INA180 por
   canal, lido pelo ADC do ESP32 para proteção de sobrecorrente.

# RESTRIÇÕES DE FABRICAÇÃO (JLCPCB)
- Priorizar componentes SMD; preferir peças "Basic" quando possível.
- PCB de no mínimo 2 camadas; usar 4 camadas se ajudar na integridade de
  energia/térmica. Cobre de 2 oz nas camadas de potência.
- Larguras de trilha calculadas para a corrente (use IPC-2221): trilhas de
  motor para 10 A; trilhas de pico de 30 A devem ser curtas e largas.
- Regras de espaçamento e folga adequadas para 12 V/30 A.
- Separar terra de potência (PGND) e terra de sinal (AGND) com ponto único
  de junção (star ground).
- Mapear os pinos PWM em GPIOs válidos do ESP32 (evitar GPIOs de boot/strapping).

# ENTREGÁVEIS
1. Esquemático completo, organizado por blocos (alimentação, MCU, 4 pontes H,
   proteção/filtro, conectores).
2. Layout da PCB com posicionamento, roteamento, planos de cobre, vias
   térmicas e zonas de dissipação.
3. BOM com referências LCSC (JLCPCB) e quantidades.
4. Arquivos de fabricação: Gerber, BOM (.csv) e Pick&Place (CPL) no formato
   aceito pela JLCPCB.
5. Tabela de pinagem ESP32 → função (qual GPIO controla cada IN de cada ponte).
6. Notas de montagem e de calibração/uso.

# SEGURANÇA E VALIDAÇÃO
- Inclua proteção contra curto, inversão de polaridade e sobrecorrente.
- Indique o dimensionamento térmico (estimar dissipação dos MOSFETs com Rds(on)
  do IRF3205 em 10 A) e se há necessidade de dissipador externo.
- Liste premissas feitas e quaisquer pontos que precisem de confirmação.
```

---

## Pontos de atenção

- **Curto-circuitar 2 motores em paralelo** só funciona bem se os motores forem
  **iguais** (mesmo modelo/carga). Motores diferentes dividem corrente de forma
  desigual e um pode sobrecarregar. Confirme que cada par usará motores idênticos.
- **Corrente total do sistema:** 6 × 5 A = **até 30 A** vindos da fonte de 12 V
  (≈ 360 W). Confirmar fonte, fusível (~40 A slow-blow), fiação (~12 AWG) e
  conector de entrada robusto.
- Detalhes dos cálculos de dimensionamento estão em `dimensionamento/`.
