# Dimensionamento 3 — Fusível (versão 2 A/motor)

Como escolher o valor do fusível de proteção. Não há fórmula "fechada" — é uma
**escolha com margens** e algumas regras.

---

## O que o fusível faz

Ele é o **elo fraco proposital** do circuito. Se algo der errado (curto, motor
travado, falha), a corrente dispara e o fusível **queima primeiro**, cortando
tudo **antes** que o fio, a trilha ou os componentes peguem fogo.

> 💡 Vantagem da versão 2 A: como a corrente total é só ~12 A, o fusível e o
> suporte **cabem na própria placa** (suporte 5×20 SMD/THT), em vez de ficar
> externo como na versão 5 A (~40 A, off-board).

---

## A conta (três regras simultâneas)

### Regra 1 — Maior que a corrente normal (com margem)

> **Valor do fusível = Corrente máxima normal ÷ 0,75** (≈ × 1,25 a 1,5)

### Regra 2 — Menor que o limite do elo mais fraco

O fusível tem que queimar **antes** do fio/trilha. O fio e a trilha precisam
aguentar **mais** corrente que o fusível.

### Regra 3 — Tensão e tipo corretos

- **Tensão nominal** ≥ a do circuito (12 V → use 32 V).
- **Tipo**: rápido ou **retardado (slow-blow)**.

---

## O detalhe que mais importa: motores

Motores puxam um **pico de partida** de **3 a 8×** a corrente normal por uma
fração de segundo.

- Fusível **rápido** → queima toda vez que ligar (falso alarme).
- Fusível **retardado (slow-blow)** → tolera o pico curto, mas queima se a
  sobrecorrente **persistir** (motor travado, curto real).

Em circuito com motor, use **retardado**.

---

## Exemplo (este projeto de 6 motores a 2 A)

1. Corrente máxima somando os 6 motores: **até 12 A**.
2. **Regra 1:** 12 ÷ 0,75 = **16 A** (ou 12 × 1,25 = 15 A).
3. **Regra 2:** fio e trilha de entrada precisam aguentar **mais que 16 A**
   (fio ~16 AWG, trilha/pour de entrada largo).
4. **Regra 3:** fusível de **~15 A**, **32 V**, tipo **retardado**.

> Resultado: **um fusível retardado de ~15 A / 32 V na entrada de 12 V — e ele
> cabe na própria placa** (suporte 5×20).

---

## Dica extra — fusível por canal

Dá para colocar um fusível menor **por canal** (ex.: retardado ~6 A por canal de
4 A). Se **um** motor der problema, só aquele canal corta. Não é obrigatório.

---

## Resumo

1. Fusível = corrente máxima normal **× ~1,25–1,5**.
2. Tem que ficar **abaixo** do que o fio/trilha aguenta.
3. **Tensão** ≥ a do circuito (32 V).
4. Com motores, use **retardado (slow-blow)**.
5. No projeto 2 A: **~15 A, 32 V, slow-blow — na própria placa.**
