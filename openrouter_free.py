#!/usr/bin/env python3
"""
Lista os modelos GRATUITOS (sem cobrança de créditos) disponíveis no OpenRouter.

Consulta o endpoint público https://openrouter.ai/api/v1/models (não precisa
de chave de API) e filtra os modelos cujo preço de prompt e de completion é 0.

Uso:
    python3 openrouter_free.py            # tabela
    python3 openrouter_free.py --json     # JSON cru
    python3 openrouter_free.py --ids      # só os IDs (um por linha)
"""

import argparse
import json
import sys
import urllib.error
import urllib.request

URL = "https://openrouter.ai/api/v1/models"
TIMEOUT = 30


def fetch_models():
    req = urllib.request.Request(URL, headers={"User-Agent": "openrouter-free/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        sys.exit(f"Erro HTTP {e.code} ao acessar {URL}")
    except urllib.error.URLError as e:
        sys.exit(f"Erro de rede: {e.reason}")
    except json.JSONDecodeError:
        sys.exit("Resposta inválida (não é JSON).")
    return data.get("data", [])


def _as_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def is_free(model):
    """Gratuito = preço de prompt E completion iguais a 0."""
    pricing = model.get("pricing", {}) or {}
    prompt = _as_float(pricing.get("prompt"))
    completion = _as_float(pricing.get("completion"))
    if prompt is None or completion is None:
        return False
    return prompt == 0.0 and completion == 0.0


def context_len(model):
    return model.get("context_length") or model.get("top_provider", {}).get(
        "context_length"
    )


def main():
    ap = argparse.ArgumentParser(description="Modelos gratuitos no OpenRouter")
    ap.add_argument("--json", action="store_true", help="saída JSON crua")
    ap.add_argument("--ids", action="store_true", help="só os IDs")
    args = ap.parse_args()

    models = fetch_models()
    free = [m for m in models if is_free(m)]
    free.sort(key=lambda m: m.get("id", ""))

    if args.json:
        print(json.dumps(free, indent=2, ensure_ascii=False))
        return

    if args.ids:
        for m in free:
            print(m.get("id", ""))
        return

    print(f"Modelos gratuitos no OpenRouter: {len(free)} de {len(models)} totais\n")
    for m in free:
        ctx = context_len(m)
        ctx_str = f"{ctx:,} ctx" if isinstance(ctx, int) else "ctx ?"
        print(f"• {m.get('id', '?')}")
        print(f"    {m.get('name', '')}  [{ctx_str}]")


if __name__ == "__main__":
    main()
