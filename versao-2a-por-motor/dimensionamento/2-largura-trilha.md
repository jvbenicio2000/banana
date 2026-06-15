# Dimensionamento 2 — Largura da Trilha de Cobre (versão 2 A/motor)

Como descobrir **quão larga** uma trilha precisa ser para carregar a corrente
sem esquentar demais. O padrão usado é o **IPC-2221**.

---

## A ideia

Uma trilha de cobre é como um **cano** por onde a corrente passa. Ela tem uma
pequena resistência e **esquenta** quando a corrente passa. Se for **estreita
demais**, esquenta muito. Dimensionar a largura garante aquecimento dentro de um
limite seguro.

---

## Do que a conta depende

- **A corrente** que vai passar (mais corrente → trilha mais larga).
- **O aquecimento aceito** (normalmente ~10 °C acima do ambiente).
- **A espessura do cobre** (1 oz, 2 oz...). Cobre mais grosso carrega mais com a
  mesma largura.

O que carrega corrente é a **área da seção** = largura × espessura.

---

## A conta (IPC-2221), em dois passos

### Passo 1 — Área de cobre necessária

> **Área = ( Corrente ÷ ( k × Aumento_de_temperatura^0,44 ) ) ^ (1 ÷ 0,725)**

- **k** = 0,048 na **superfície** (camada externa); 0,024 **interna**.
- Resultado em **mils²**.

### Passo 2 — Converter área em largura

> **Largura = Área ÷ Espessura_do_cobre**

- **1 oz** ≈ 1,4 mils
- **2 oz** ≈ 2,8 mils

---

## Exemplo (4 A — pior canal, cobre 1 oz, 10 °C, superfície)

1. Aumento de temperatura ^0,44 ≈ **2,75**
2. × k (0,048) ≈ **0,132**
3. 4 ÷ 0,132 ≈ **30,3**
4. ^(1 ÷ 0,725 ≈ 1,38): área ≈ **96 mils²**
5. ÷ espessura 1 oz (1,4 mils): **≈ 69 mils ≈ 1,75 mm**

Resultado: a trilha de 4 A precisa de **~1,75 mm em cobre 1 oz**. Na prática
use **~2,5 mm** para folga. Os canais de 1 motor (2 A) pedem só **~0,9 mm**.

> Diferente da versão 5 A (que exigia ~3,5 mm em 2 oz ou polígonos para 10 A),
> aqui trilhas normais em **1 oz** resolvem.

### Tabela rápida (aumento de ~10 °C)

| Corrente | Cobre 1 oz | Cobre 2 oz |
|---|---|---|
| 2 A (canal A/B) | ~0,9 mm | ~0,5 mm |
| 4 A (canal C/D) | ~1,75 mm (use 2,5) | ~0,9 mm |
| 12 A (pico) | curto/largo ou pour pequeno | tranquilo |

---

## Polígonos (copper pour)

A 12 A de pico, um pour pequeno sob os MOSFETs já resolve (também ajuda no
térmico). Não há mais a necessidade dos grandes polígonos de 30 A da versão 5 A.

Cuidados gerais: evite **gargalos**, use **vias de costura** entre camadas e
**conexão sólida** (não alívio térmico) nos pinos de potência. Polígono de 12 V
e polígono de GND.

---

## Resumo

1. **Área** = corrente e aquecimento aceito (IPC-2221).
2. **Largura** = área ÷ espessura do cobre.
3. A 4 A em **1 oz**: ~1,75 mm (use 2,5 mm). A 2 A: ~0,9 mm.
4. Pico de 12 A → pour modesto; sem necessidade de 2 oz.
