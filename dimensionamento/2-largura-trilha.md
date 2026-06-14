# Dimensionamento 2 — Largura da Trilha de Cobre

Como descobrir **quão larga** uma trilha precisa ser para carregar a corrente
sem esquentar demais. O padrão usado é o **IPC-2221**.

---

## A ideia

Uma trilha de cobre é como um **cano** por onde a corrente passa. Ela tem uma
pequena resistência e, por isso, **esquenta** quando a corrente passa. Se for
**estreita demais**, esquenta muito e pode derreter. Dimensionar a largura é
garantir que ela esquente só um pouco, dentro de um limite seguro.

---

## Do que a conta depende

A largura necessária depende de **três coisas**:

- **A corrente** que vai passar. Mais corrente → trilha mais larga.
- **O aquecimento que você aceita.** Você escolhe quanto a trilha pode esquentar
  acima do ambiente (normalmente até ~10 °C). Aceitar mais calor permite trilha
  mais fina; querer trilha bem fria exige mais largura.
- **A espessura do cobre** (a "onça" da placa: 1 oz, 2 oz...). Cobre mais grosso
  carrega mais corrente com a mesma largura. Dobrar a espessura permite usar
  cerca de **metade** da largura.

O que realmente carrega corrente é a **área da seção** da trilha, ou seja
**largura × espessura** do cobre.

---

## A conta (IPC-2221), em dois passos

### Passo 1 — Área de cobre necessária

> **Área = ( Corrente ÷ ( k × Aumento_de_temperatura^0,44 ) ) ^ (1 ÷ 0,725)**

Onde:
- **Corrente** em amperes.
- **Aumento_de_temperatura** em graus acima do ambiente (ex.: 10 °C).
- **k** = constante conforme a posição da trilha:
  - **0,048** na **superfície** da placa (camada externa).
  - **0,024** **dentro** da placa (camada interna) — esfria pior, aguenta menos.
- Resultado (**Área**) em **mils²** (mil = milésimo de polegada).

> Os expoentes "quebrados" (0,44 e 0,725) vêm de **medições experimentais**, não
> de uma teoria limpa — a fórmula apenas descreve o que acontece na prática.

### Passo 2 — Converter área em largura

> **Largura = Área ÷ Espessura_do_cobre**

Espessura conforme a onça do cobre:
- **1 oz** ≈ 1,4 mils
- **2 oz** ≈ 2,8 mils

---

## Exemplo (10 A, cobre 2 oz, 10 °C, superfície)

1. Aumento de temperatura elevado a 0,44 ≈ **2,75**
2. Multiplicado por k (0,048) ≈ **0,132**
3. Corrente dividida por isso: 10 ÷ 0,132 ≈ **75,7**
4. Elevado a (1 ÷ 0,725 ≈ 1,38): área ≈ **390 mils²**
5. Dividido pela espessura 2 oz (2,8 mils): **≈ 140 mils ≈ 3,5 mm**

Resultado: a trilha de 10 A precisa de **~3,5 mm** em cobre 2 oz. (Em cobre
1 oz daria o dobro, ~7 mm — por isso pedimos cobre grosso em placas de
potência.)

> Na prática, usa-se uma **calculadora de largura de trilha** (online, ou a do
> KiCad/Flux). É exatamente essa fórmula que roda por trás.

### Tabela rápida (aumento de ~10 °C)

| Corrente | Cobre 1 oz | Cobre 2 oz |
|---|---|---|
| 5 A | ~2,5 mm | ~1,3 mm |
| 10 A | ~7 mm | ~3,5 mm |
| 30 A (pico) | inviável | usar **polígono** |

---

## Polígonos (copper pour)

Quando a corrente fica muito alta (como os 30 A de pico), em vez de uma trilha
larguíssima usa-se um **polígono**: uma **área grande de cobre preenchida**,
como uma chapa, em vez de uma linha.

Vantagens em alta corrente:
- **Resistência baixíssima** (área enorme) → quase não esquenta.
- **Dissipa calor** → funciona como dissipador plano; por isso colocamos os
  MOSFETs sobre um polígono com **vias térmicas**.
- **Cabe na placa** → ocupa o espaço livre, sem trilhas absurdamente largas.

Cuidados:
- A corrente se espalha e escolhe o caminho mais fácil; evite **gargalos**
  (pontos estreitos) que anulam a vantagem.
- Use **vias de costura (stitching vias)** para o calor/corrente passarem para
  outras camadas/plano.
- Em pinos de potência, use **conexão sólida** ao polígono (não "alívio
  térmico"), que conduz mais calor e corrente.
- Normalmente um polígono para o **12 V** e outro para o **terra (GND)**.

---

## Resumo

1. **Área** = sai da corrente e do aquecimento aceito (fórmula IPC-2221).
2. **Largura** = área ÷ espessura do cobre.
3. Cobre mais grosso → trilha mais estreita para a mesma corrente.
4. Corrente alta → use **polígono** em vez de trilha.
