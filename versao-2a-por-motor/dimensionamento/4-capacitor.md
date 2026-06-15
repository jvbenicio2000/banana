# Dimensionamento 4 — Capacitor de Bulk (versão 2 A/motor)

Como escolher a capacitância que "segura" a tensão quando o motor puxa corrente
de repente.

---

## O que o capacitor de bulk faz

Pense nele como uma **caixa d'água local** ao lado do motor / ponte H.

Quando o motor liga ou o PWM chaveia, ele pede um **golpe de corrente
instantâneo**. A fonte de 12 V está longe e o fio tem "inércia" (indutância) que
impede a corrente de chegar rápido. A tensão **afunda** e volta — oscilações que
bagunçam o circuito e podem resetar o ESP32.

O capacitor fica **cheio de energia** ali perto e **entrega a corrente na hora**,
segurando a tensão. Depois a fonte o reabastece.

---

## A conta

> **Capacitância = ( Corrente entregue × Tempo que ela dura ) ÷ Queda de tensão aceitável**

Três fatores: **corrente** do golpe, **tempo** que o cap segura (ligado ao
período do PWM) e **queda de tensão aceitável** (ripple).

### Exemplo (canal de 4 A, PWM 20 kHz)

1. **Corrente:** 4 A.
2. **Tempo:** a 20 kHz cada ciclo dura 50 µs; no pior caso o cap segura ~**25 µs**.
3. **Queda aceitável:** **0,5 V**.

Conta: 4 A × 25 µs ÷ 0,5 V ≈ **200 microfarads**.

> Por isso, na versão 2 A, **220 a 470 µF por canal** já bastam (a versão 5 A
> pedia 470–1000 µF). Mantivemos **470 µF** por folga.

---

## Precisa de DOIS tipos juntos

- **Eletrolítico grande (centenas de µF):** guarda **muita energia**, mas é
  **lento** — bom para os golpes de liga/desliga e partida.
- **Cerâmico pequeno (100 nF):** guarda pouco, mas é **rapidíssimo** — pega os
  picos de altíssima frequência do chaveamento.

Regra: **um eletrolítico de bulk + um cerâmico de 100 nF colado em cada MOSFET /
ponte H.**

---

## A tensão do capacitor (não esqueça)

Escolha tensão nominal de pelo menos **1,5×** a do circuito. Em 12 V: 12 × 1,5 =
18 V → use **25 V**. Nunca use 16 V "no limite".

---

## Resumo

1. **Capacitância** = corrente do golpe × tempo ÷ queda aceita.
2. No projeto 2 A: **220 a 470 µF por canal** (usamos 470 µF) + **1000 µF** na entrada.
3. **+ 100 nF cerâmico** colado em cada MOSFET.
4. Tensão do capacitor: **25 V** (≥ 1,5× os 12 V).
