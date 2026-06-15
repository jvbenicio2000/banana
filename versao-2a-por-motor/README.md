# 📁 Versão 2 A por motor

Esta pasta é a **variante de baixa corrente** do projeto: os mesmos 6 motores,
mas com **corrente de trabalho de 2 A por motor** (em vez de 5 A).

Contém **todos os arquivos equivalentes** à versão original (5 A), recalculados:

```
versao-2a-por-motor/
├── README.md                 # este arquivo
├── alvo.md                   # objetivo (2 A)
├── prompt-placa-motores.md   # prompt de engenharia (2 A)
├── flux-roteiro.md           # roteiro Flux Copilot (2 A)
├── bom-jlcpcb.md             # BOM detalhada (2 A, ponte H discreta IRF3205+IR2104)
├── bom-jlcpcb.csv            # BOM formato JLCPCB (2 A)
├── bom-jlcpcb-max-basic.md   # BOM "máximo Basic" (ponte H complementar SOT-23)
├── bom-jlcpcb-max-basic.csv  # BOM máximo-Basic formato JLCPCB
├── design-max-basic.md       # nota de projeto do drive complementar
└── dimensionamento/
    ├── 1-calor-mosfet.md
    ├── 2-largura-trilha.md
    ├── 3-fusivel.md
    └── 4-capacitor.md
```

## O que muda da versão 5 A → 2 A

| Parâmetro | Versão 5 A (raiz do repo) | **Versão 2 A (esta pasta)** |
|---|---|---|
| Corrente/motor contínua | 5 A | **2 A** |
| Pico stall (~3×) | ~15 A | **~6 A** |
| Canal A/B (1 motor) | 5 A / 15 A pico | **2 A / 6 A pico** |
| Canal C/D (2 em paralelo) | 10 A / 30 A pico | **4 A / 12 A pico** |
| Total do sistema | até 30 A (~360 W) | **até 12 A (~144 W)** |
| Cobre da PCB | 2 oz | **1 oz** |
| Camadas | 2–4 | **2** |
| Dissipadores | necessários | **dispensados** (perda ~0,24 W/MOSFET) |
| Conector de entrada | borne 7,62 mm | **borne 5,08 mm** |
| Fusível | externo ~40 A (off-board) | **5×20 na placa, ~15 A slow-blow** |
| Shunt de corrente | 5 mΩ | **10 mΩ** (melhor resolução em 12 A) |

## Convenções (iguais à versão 5 A)

- 6 motores físicos em **4 canais de ponte H** (A, B independentes; C, D com 2
  motores em paralelo cada).
- Ponte H **discreta** (IRF3205S + IR2104) — mantida para robustez; a 2 A está
  **super-dimensionada** (sobra enorme), o que é proposital e barato.
- Bidirecional + PWM em todos os canais; 2 GPIOs por canal.
- 12 jacks banana 4 mm (2 por motor); PGND/AGND em star ground.

> 💡 Alternativa não adotada aqui: a 2 A daria para trocar a ponte H discreta por
> **CIs integrados** (1 driver por motor, sem paralelismo), encolhendo muito a
> BOM. Esta versão preferiu **espelhar a arquitetura da versão 5 A**. Se quiser a
> variante com drivers integrados, peça que eu gero uma terceira pasta.
