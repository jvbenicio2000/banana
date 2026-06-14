# Skill: jlcpcb-catalog

Skill autocontida para **consultar o catálogo de componentes da JLCPCB / LCSC**
(estoque, preço, encapsulamento e código LCSC), sem precisar de chave de API
nem aprovação.

Usa a API pública não-oficial **jlcsearch** (`jlcsearch.tscircuit.com`), que
indexa a biblioteca de montagem (PCBA) da JLCPCB.

## Conteúdo

```
jlcpcb-catalog/
├── SKILL.md              # definição da skill (frontmatter + instruções)
├── README.md             # este arquivo
└── scripts/
    └── search.py         # script de consulta (Python 3, sem dependências)
```

## Requisitos

- **Python 3** (qualquer versão recente; usa só a biblioteca padrão)
- **Acesso à internet** a `https://jlcsearch.tscircuit.com`

Não há `pip install` — o script usa apenas `urllib`/`json` do Python.

## Instalação (para outros agentes)

Esta skill segue o formato de **Agent Skills** (um diretório com `SKILL.md`).
Para usar em outro agente compatível (ex.: Claude Code), copie a pasta inteira
para o diretório de skills do agente. Exemplos:

```bash
# Claude Code — skills do projeto:
cp -r jlcpcb-catalog .claude/skills/

# ou skills do usuário (globais):
cp -r jlcpcb-catalog ~/.claude/skills/
```

Depois é só invocar a skill `jlcpcb-catalog` quando precisar consultar peças.

## Uso direto (sem agente)

O script também roda sozinho na linha de comando:

```bash
cd jlcpcb-catalog

python3 scripts/search.py "ESP32-WROOM-32E"
python3 scripts/search.py "DRV8833" --limit 5 --full
python3 scripts/search.py "0.1uF" --category capacitors
python3 scripts/search.py --list-categories
python3 scripts/search.py "IRF3205" --json
```

## Opções

| Opção | Descrição |
|---|---|
| `query` | palavra-chave ou MPN (part number do fabricante) |
| `--category NOME` | busca dentro de uma categoria (ex.: `resistors`, `capacitors`, `microcontrollers`, `voltage_regulators`) |
| `--limit N` | máximo de resultados (padrão 20) |
| `--full` | pede `full=true` à API (mais campos) |
| `--json` | imprime o JSON cru (para processar com `jq`/outro agente) |
| `--list-categories` | lista as categorias do catálogo |

## Observações

- O código LCSC é mostrado com o prefixo `C` (ex.: `C701341`), pronto para a
  BOM da JLCPCB.
- Busca por **MPN exato** funciona melhor que termos genéricos.
- Esta é uma API **não-oficial**; para *fazer pedidos* programaticamente use a
  API oficial `api.jlcpcb.com` (requer cadastro/aprovação).
