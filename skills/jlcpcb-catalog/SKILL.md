---
name: jlcpcb-catalog
description: Search the JLCPCB / LCSC assembly parts catalog (stock, price, package, LCSC part number) for any electronic component — resistors, capacitors, ICs, microcontrollers, connectors, switches, sensors, motor drivers, modules, etc. Use whenever selecting or verifying parts for a PCB that will be fabricated/assembled at JLCPCB, or when the user asks what components are available, their price, stock, or LCSC code.
---

# JLCPCB Catalog Search

Consulta a biblioteca de componentes de montagem (PCBA) da **JLCPCB / LCSC**.

Usa a API pública **não-oficial** `jlcsearch` (tscircuit), que indexa a
biblioteca da JLCPCB. **Não requer chave nem aprovação** — ótimo para
*selecionar componentes* (estoque, preço, encapsulamento, código LCSC).

> A API **oficial** da JLCPCB (`api.jlcpcb.com`) exige cadastro e aprovação
> manual e é voltada a *fazer pedidos*. Para apenas **consultar peças**, esta
> skill é o caminho mais simples.

## Quando usar

- Escolher um componente para um projeto que será fabricado na JLCPCB.
- Descobrir o **código LCSC** (`Cxxxxxx`), **estoque**, **preço** ou
  **encapsulamento** de uma peça.
- Comparar opções (ex.: vários MOSFETs, drivers de motor, sensores).
- Listar as categorias/subcategorias do catálogo.

## Como usar

O script principal usa **somente a biblioteca padrão do Python 3** (sem
dependências). Execute:

```bash
# Busca geral por palavra-chave
python3 scripts/search.py "ESP32-WROOM-32E"

# Limitar resultados e mostrar todos os campos
python3 scripts/search.py "DRV8833" --limit 5 --full

# Buscar dentro de uma categoria específica
python3 scripts/search.py "0.1uF" --category capacitors
python3 scripts/search.py "STM32" --category microcontrollers

# Listar as categorias disponíveis
python3 scripts/search.py --list-categories

# Saída JSON crua (para processar com jq ou outro agente)
python3 scripts/search.py "IRF3205" --json
```

## Saída

Por padrão imprime uma tabela com: **LCSC**, **MFR** (part number do
fabricante), **Package**, **Stock**, **Price** e **Description**.

- O código LCSC é exibido com o prefixo `C` (ex.: `C701341`), que é o formato
  usado na BOM da JLCPCB.
- Use `--json` para obter o registro completo de cada peça.

## Dicas de busca

- Buscar por **part number conhecido** funciona melhor que termos genéricos
  (ex.: `TP4056` em vez de `lithium charger`; `ATGM336H` em vez de `GPS`).
- Se uma busca multi-palavra vier vazia, tente **uma palavra-chave** ou o
  **MPN exato**.
- Prefira peças com **estoque alto**; ao montar uma BOM, confirme se a peça é
  **Basic/Preferred** (montadas sem taxa de feeder pela JLCPCB) — peças
  "Extended" têm taxa de carregamento, e through-hole tem custo de solda
  manual/wave.

## Endpoints usados (referência)

- Base: `https://jlcsearch.tscircuit.com`
- `GET /components/list.json?search=<termo>&full=true` — busca geral
- `GET /<categoria>/list.json?search=<termo>` — busca por categoria
  (ex.: `resistors`, `capacitors`, `microcontrollers`, `voltage_regulators`)
- `GET /categories/list.json` — lista de categorias
- Resposta: JSON com a chave `components` (lista de peças).

## Para outros agentes

Esta skill é autocontida: copie a pasta `jlcpcb-catalog/` inteira para o
diretório de skills do seu agente. O único requisito é **Python 3** e
**acesso à internet** (a `jlcsearch.tscircuit.com`). Veja `README.md` para
instalação.
