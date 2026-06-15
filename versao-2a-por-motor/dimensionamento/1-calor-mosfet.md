# Dimensionamento 1 — Calor no MOSFET (versão 2 A/motor)

Como descobrir **quanto calor** um MOSFET gera e **quão quente** ele fica, para
decidir se precisa de dissipador. (Spoiler: a 2 A, **não precisa**.)

---

## A ideia

Todo MOSFET de potência "perde" um pouco de energia em forma de **calor** quando
conduz a corrente do motor. Calculamos essa perda, vemos quanto a peça esquenta
e decidimos: ela aguenta sozinha, precisa de mais cobre, ou precisa de
dissipador?

O cálculo tem **duas etapas**: (1) quanto calor é gerado e (2) quão quente a
peça fica.

---

## Etapa 1 — Quanto calor a peça gera

O calor depende da **corrente** que passa e da **resistência interna** do MOSFET
ligado (*Rds(on)*).

> Em fórmula: **Perda = Corrente × Corrente × Resistência**

O ponto-chave: a corrente entra **ao quadrado**. Dobrar a corrente **quadruplica**
o calor. Por isso reduzir de 5 A → 2 A faz uma diferença enorme.

### Exemplo (IRF3205 a 4 A — pior canal, par em paralelo)

- *Rds(on)* a quente ≈ 0,012 ohm.
- Perda por condução = 4 × 4 × 0,012 = **0,19 W**.
- Perda por chaveamento a 20 kHz ≈ 0,05 W.
- **Total ≈ 0,24 W por MOSFET.**

> Compare: na versão 5 A (10 A por canal) eram ~1,3 W por MOSFET. Aqui é
> **~5× menos calor** — praticamente nada.

### Nos canais de 1 motor (2 A)

- Perda por condução = 2 × 2 × 0,012 = **0,05 W** (desprezível).

---

## Etapa 2 — Quanto a peça vai esquentar

> Em fórmula: **Temperatura = Ambiente + ( Calor × Resistência térmica )**

### Exemplo (0,24 W, ambiente 25 °C)

| Montagem | Resistência térmica | Temperatura final |
|---|---|---|
| SMD com pouco cobre | ~60 °C/W | ~39 °C ✅ |
| SMD com pour modesto + vias | ~40 °C/W | ~35 °C ✅✅ |

Mesmo no caso "pouco cobre" a junção fica **~39 °C** — muito abaixo dos 100–110 °C
de projeto. **Conclusão: dispensa dissipador e dispensa cobre 2 oz**; basta um
pour modesto em 1 oz com algumas vias.

> No pico de 12 A (partida/stall), a perda instantânea é 12 × 12 × 0,012 ≈
> **1,7 W**, mas dura milissegundos — a massa térmica absorve. O perigo continua
> sendo o motor **travado por segundos**; por isso vale o sensoriamento de
> corrente para desligar antes de superaquecer.

---

## Resumo

1. **Calor gerado** = corrente × corrente × resistência interna (+ chaveamento).
2. A 4 A: **~0,24 W/MOSFET**; a 2 A: **~0,05 W**.
3. A corrente pesa ao quadrado → cair de 5→2 A reduz muito o calor.
4. **Sem dissipador, cobre 1 oz e pour modesto bastam.**
