# Dimensionamento 4 — Capacitor de Bulk

Como escolher a capacitância que "segura" a tensão quando o motor puxa corrente
de repente.

---

## O que o capacitor de bulk faz

Pense nele como uma **caixa d'água local** ao lado do motor / ponte H.

Quando o motor liga ou o PWM chaveia, ele pede um **golpe de corrente
instantâneo**. A fonte de 12 V está longe, e o fio até ela tem uma "inércia"
(indutância) que **impede a corrente de chegar rápido o suficiente**. Resultado:
a tensão **afunda** naquele instante (cai de 12 V para, digamos, 10 V) e volta —
são as **quedas e oscilações** que bagunçam o circuito e podem até resetar o
ESP32.

O capacitor resolve: fica **cheio de energia** ali perto e, no instante do
golpe, **entrega a corrente na hora**, segurando a tensão estável. Depois a
fonte o reabastece com calma.

---

## A conta

A ideia central: **um capacitor entrega corrente por um tempo, e isso faz a
tensão dele cair um pouco.** A relação é:

> **Capacitância = ( Corrente entregue × Tempo que ela dura ) ÷ Queda de tensão aceitável**

Três fatores:
- **Corrente** que o motor puxa de repente (maior → cap maior).
- **Tempo** que o capacitor segura sozinho até a fonte assumir. No PWM, está
  ligado ao **período do chaveamento** — quanto mais **baixa** a frequência,
  mais tempo ele precisa segurar e maior o cap.
- **Queda de tensão aceitável (ripple):** quanto você deixa a tensão balançar.
  Aceitar mais balanço → cap menor; querer tensão firme → cap maior.

### Exemplo (canal de 10 A, PWM 20 kHz)

1. **Corrente:** 10 A.
2. **Tempo:** a 20 kHz cada ciclo dura 50 microssegundos; no pior caso o cap
   segura cerca de metade, ~**25 microssegundos**.
3. **Queda aceitável:** digamos **0,5 V**.

Conta: 10 A × 25 µs ÷ 0,5 V ≈ **500 microfarads**.

> Por isso a recomendação de **470 a 1000 µF por canal**. Quanto mais perto de
> 1000 µF, mais firme a tensão.

---

## Precisa de DOIS tipos juntos

Um capacitor só não resolve, porque cada tipo é bom numa coisa:

- **Eletrolítico grande (centenas de µF):** guarda **muita energia**, mas é
  **lento** — bom para os golpes "lentos" (liga/desliga e partida do motor).
- **Cerâmico pequeno (100 nanofarads):** guarda pouca energia, mas é
  **rapidíssimo** — pega os picos de altíssima frequência do chaveamento dos
  MOSFETs.

Regra: **um eletrolítico grande de bulk + um cerâmico de 100 nF colado bem perto
de cada MOSFET / ponte H.** Os dois trabalham em dupla, cada um cobrindo uma
"velocidade" de golpe.

---

## A tensão do capacitor (não esqueça)

O capacitor tem uma **tensão máxima**. Regra: escolha tensão nominal de pelo
menos **1,5 vez** a do circuito. Em 12 V: 12 × 1,5 = 18 V → use capacitores de
**25 V** (valor comercial logo acima). Nunca use um de 16 V "no limite", porque
picos do motor podem passar de 12 V e estourar o capacitor.

---

## Resumo

1. **Capacitância** = corrente do golpe × tempo que dura ÷ queda de tensão aceita.
2. No projeto: **470 a 1000 µF por canal** (eletrolítico).
3. **+ 100 nF cerâmico** colado em cada MOSFET (golpes rápidos).
4. Tensão do capacitor: **25 V** (≥ 1,5× os 12 V).
