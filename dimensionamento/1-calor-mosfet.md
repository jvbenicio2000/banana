# Dimensionamento 1 — Calor no MOSFET

Como descobrir **quanto calor** um MOSFET gera e **quão quente** ele fica, para
decidir se precisa de dissipador.

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

O calor depende de **duas coisas**: da **corrente** que passa pela peça e da
**resistência interna** dela (no MOSFET ligado, chamada *Rds(on)*).

A regra (perda por condução): você multiplica a **corrente por ela mesma**
(corrente vezes corrente) e depois multiplica pela **resistência interna**. O
resultado é o calor gerado, em watts.

> Em fórmula: **Perda = Corrente × Corrente × Resistência**

O ponto mais importante: a corrente entra **duas vezes** na conta. Por isso o
calor **não cresce na mesma proporção** que a corrente — cresce muito mais
rápido. Se você **dobra** a corrente, o calor **quadruplica**; se **triplica**,
fica **nove vezes maior**. É por isso que o pico de partida (motor travado) é
tão perigoso.

A resistência entra de forma direta: quanto **menor** a *Rds(on)*, **menos**
calor a peça gera com a mesma corrente. Por isso escolher um MOSFET de
resistência baixa ajuda tanto.

Existe ainda uma perda menor, **por chaveamento** (a transição liga/desliga do
PWM), que cresce com a **frequência** do PWM. Em frequências baixas (ex.: 20 kHz)
ela é pequena; em frequências altas, passa a importar.

### Exemplo (IRF3205 a 10 A)

- *Rds(on)* a quente ≈ 0,012 ohm.
- Perda por condução = 10 × 10 × 0,012 = **1,2 W**.
- Perda por chaveamento a 20 kHz ≈ 0,12 W.
- **Total ≈ 1,3 W por MOSFET.**

---

## Etapa 2 — Quanto a peça vai esquentar

Saber o calor ainda não dá a temperatura. Para chegar nela, parte-se da
**temperatura do ambiente** e **soma-se** o aquecimento causado pelo calor.

O aquecimento é o **calor gerado** multiplicado por um número chamado
**resistência térmica**, que representa a **dificuldade que o calor tem de
escapar** da peça para o ar.

> Em fórmula: **Temperatura = Ambiente + ( Calor × Resistência térmica )**

Quanto **maior** essa dificuldade (resistência térmica alta), **mais** a peça
esquenta. Quanto **mais fácil** o calor escapa (resistência térmica baixa),
**menos** ela esquenta. É exatamente aí que entram o **cobre da placa** e o
**dissipador**: eles reduzem essa dificuldade e deixam a peça mais fria.

### Exemplo (1,3 W, ambiente 25 °C)

| Montagem | Resistência térmica | Temperatura final |
|---|---|---|
| SMD com pouco cobre | ~60 °C/W | ~103 °C ⚠️ |
| SMD com pour grande + vias térmicas | ~40 °C/W | ~77 °C ✅ |
| TO-220 com dissipador parafusado | ~10 °C/W | ~38 °C ✅✅ |

Projete para a junção ficar **abaixo de ~100–110 °C** (o limite do IRF3205 é
175 °C, mas trabalhe com margem).

**Conclusão do exemplo:** a 10 A contínuos, cobre generoso + vias térmicas já
resolve. Em ambiente quente (caixa fechada) ou corrente sustentada perto de
10 A, **acrescente dissipador** para ter margem.

> No pico de 30 A (partida/stall), a perda instantânea é enorme
> (30 × 30 × 0,012 ≈ 10,8 W), mas dura milissegundos — a massa térmica absorve.
> O perigo é o motor **travado por segundos**; por isso vale o sensoriamento de
> corrente para desligar antes de superaquecer.

---

## Resumo

1. **Calor gerado** = corrente × corrente × resistência interna (+ chaveamento).
2. **Temperatura** = ambiente + (calor × resistência térmica).
3. A corrente pesa ao quadrado → picos são críticos.
4. Mais cobre / dissipador = menor resistência térmica = peça mais fria.
