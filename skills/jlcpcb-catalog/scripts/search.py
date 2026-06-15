#!/usr/bin/env python3
"""
jlcpcb-catalog — consulta o catálogo de componentes da JLCPCB / LCSC.

Usa a API pública NÃO-OFICIAL jlcsearch (tscircuit), que indexa a biblioteca
de montagem (PCBA) da JLCPCB. Não requer chave de API nem aprovação.

Requisitos: apenas Python 3 (biblioteca padrão). Sem dependências externas.

Exemplos:
    python3 search.py "ESP32-WROOM-32E"
    python3 search.py "DRV8833" --limit 5 --full
    python3 search.py "0.1uF" --category capacitors
    python3 search.py --list-categories
    python3 search.py "IRF3205" --json
"""

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://jlcsearch.tscircuit.com"
TIMEOUT = 30


def _fetch(url):
    """Faz GET e retorna o JSON decodificado (ou levanta erro amigável)."""
    req = urllib.request.Request(
        url, headers={"User-Agent": "jlcpcb-catalog-skill/1.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        sys.exit(f"Erro HTTP {e.code} ao acessar: {url}")
    except urllib.error.URLError as e:
        sys.exit(f"Erro de rede: {e.reason} (sem acesso a {BASE}?)")
    except json.JSONDecodeError:
        sys.exit("Resposta inválida (não é JSON). A API pode estar indisponível.")


def list_categories():
    data = _fetch(f"{BASE}/categories/list.json")
    cats = data.get("categories", data if isinstance(data, list) else [])
    seen = set()
    for c in cats:
        if isinstance(c, dict):
            name = c.get("category", "")
            sub = c.get("subcategory", "")
        else:
            name, sub = str(c), ""
        key = (name, sub)
        if key in seen:
            continue
        seen.add(key)
        print(f"{name}" + (f"  ›  {sub}" if sub else ""))


def search(query, category=None, limit=20, full=False):
    params = {}
    if category:
        path = f"/{category}/list.json"
        if query:
            params["search"] = query
    else:
        path = "/components/list.json"
        params["search"] = query or ""
    if full:
        params["full"] = "true"

    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)

    data = _fetch(url)
    comps = data.get("components", data if isinstance(data, list) else [])
    return comps[: limit if limit and limit > 0 else None]


def _lcsc(rec):
    val = rec.get("lcsc") or rec.get("lcsc_id") or rec.get("lcscId")
    if val is None:
        return "-"
    s = str(val)
    return s if s.upper().startswith("C") else f"C{s}"


def _price(rec):
    p = rec.get("price")
    if p is None:
        # alguns registros trazem faixas em 'prices' / 'price_tiers'
        p = rec.get("prices") or rec.get("price_tiers")
    if p is None:
        return "-"
    if isinstance(p, (int, float)):
        return f"${p}"
    # a API costuma devolver as faixas de preço como JSON em texto
    if isinstance(p, str):
        s = p.strip()
        if s.startswith("[") or s.startswith("{"):
            try:
                p = json.loads(s)
            except json.JSONDecodeError:
                return s
        else:
            return s
    if isinstance(p, list) and p:
        vals = []
        for tier in p:
            if isinstance(tier, dict):
                v = tier.get("price") or tier.get("unit_price")
                if v is not None:
                    vals.append(float(v))
            elif isinstance(tier, (int, float)):
                vals.append(float(tier))
        if vals:
            return f"${min(vals):.4f}-${max(vals):.4f}"
    return str(p)


def _field(rec, *names, default="-"):
    for n in names:
        if rec.get(n) not in (None, ""):
            return rec[n]
    return default


def print_table(comps):
    if not comps:
        print("Nenhum componente encontrado. Tente outra palavra-chave ou o MPN exato.")
        return
    for i, rec in enumerate(comps, 1):
        lcsc = _lcsc(rec)
        mfr = _field(rec, "mfr", "manufacturer_part", "mpn", "part")
        pkg = _field(rec, "package", "package_name")
        stock = _field(rec, "stock", "in_stock", "quantity")
        price = _price(rec)
        desc = _field(rec, "description", "desc", default="")
        print(f"[{i}] {lcsc}  {mfr}")
        print(f"     package: {pkg} | stock: {stock} | price: {price}")
        if desc:
            print(f"     {desc}")
        print()


def main():
    ap = argparse.ArgumentParser(
        description="Consulta o catálogo de componentes da JLCPCB / LCSC."
    )
    ap.add_argument("query", nargs="?", default="", help="palavra-chave ou MPN")
    ap.add_argument("--category", help="busca dentro de uma categoria (ex.: capacitors)")
    ap.add_argument("--limit", type=int, default=20, help="máx. de resultados (padrão 20)")
    ap.add_argument("--full", action="store_true", help="pede full=true à API")
    ap.add_argument("--json", action="store_true", help="saída JSON crua")
    ap.add_argument("--list-categories", action="store_true", help="lista categorias")
    args = ap.parse_args()

    if args.list_categories:
        list_categories()
        return

    if not args.query and not args.category:
        ap.error("informe uma palavra-chave de busca, --category ou --list-categories")

    comps = search(args.query, args.category, args.limit, args.full)

    if args.json:
        print(json.dumps(comps, indent=2, ensure_ascii=False))
    else:
        print_table(comps)


if __name__ == "__main__":
    main()
