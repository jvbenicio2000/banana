# Dimensionamento 3 — Fusível

Como escolher o valor do fusível de proteção. Diferente das outras contas, não
há uma fórmula "fechada" — é uma **escolha com margens** e algumas regras.

---

## O que o fusível faz

Ele é o **elo fraco proposital** do circuito. Se algo der errado (curto, motor
travado, falha), a corrente dispara e o fusível **queima primeiro**, cortando
tudo **antes** que o fio, a trilha ou os componentes se danifiquem ou peguem
fogo. Ele protege o resto.

---

## A conta (três regras simultâneas)

O valor escolhido precisa satisfazer **as três condições ao mesmo tempo**.

### Regra 1 — Maior que a corrente normal (com margem)

Se o fusível for igual à corrente de trabalho, ele queima à toa ("queima por
incômodo"). Os fabricantes recomendam usar o fusível em no máximo **75% da
capacidade**.

> **Valor do fusível = Corrente máxima normal ÷ 0,75**

Que na prática equivale a **multiplicar a corrente máxima por cerca de 1,25 a
1,5**.

### Regra 2 — Menor que o limite do elo mais fraco

O fusível só protege se queimar **antes** do fio/trilha. Então o valor tem que
ficar **abaixo** da corrente que danifica o fio, a trilha ou o conector. Ou
seja: **o fio e a trilha precisam aguentar mais corrente do que o fusível.**

### Regra 3 — Tensão e tipo corretos

- **Tensão nominal** do fusível ≥ tensão do circuito (12 V → use 32 V ou mais,
  que é o comum).
- **Tipo**: existe o **rápido** e o **retardado (slow-blow / time-delay)**.

---

## O detalhe que mais importa: motores

Motores puxam um **pico enorme na partida** (corrente de partida/inrush), que
pode ser **3 a 8 vezes** a corrente normal, por uma fração de segundo.

- Fusível **rápido** → queima toda vez que ligar os motores (falso alarme).
- Fusível **retardado (slow-blow)** → tolera o pico curto da partida, mas ainda
  queima se a sobrecorrente **persistir** (motor travado, curto real).

Portanto, em circuito com motor, use **fusível retardado**.

---

## Exemplo (o projeto de 6 motores)

1. Corrente máxima somando os 6 motores: **até 30 A**.
2. **Regra 1:** 30 ÷ 0,75 = **40 A** (ou 30 × 1,25 = 37,5 A → arredonda para cima).
3. **Regra 2:** fio e trilha de entrada precisam aguentar **mais que 40 A**
   (fio reforçado ~12 AWG, polígono de cobre largo).
4. **Regra 3:** fusível de **40 A**, **32 V** (ou mais), tipo **retardado**.

> Resultado: **um fusível retardado de ~40 A / 32 V na entrada de 12 V.**

---

## Dica extra — fusível por canal

Além do fusível geral da entrada, dá para colocar um fusível menor **em cada
canal de motor** (ex.: retardado de ~8–10 A por canal de 5 A). Assim, se **um**
motor der problema, só aquele canal corta e o resto continua funcionando. Não é
obrigatório, mas dá robustez.

---

## Resumo

1. Fusível = corrente máxima normal **× ~1,25–1,5** (não queimar à toa).
2. Tem que ficar **abaixo** do que o fio/trilha aguenta.
3. **Tensão** ≥ a do circuito.
4. Com motores, use **retardado (slow-blow)** pelo pico de partida.
5. No projeto: **~40 A, 32 V, slow-blow**.
