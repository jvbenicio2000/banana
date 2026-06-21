#!/usr/bin/env python3
"""
Cliente simples para chamar modelos do OpenRouter.

A chave de API é lida (nesta ordem) de:
  1. variável de ambiente  OPENROUTER_API_KEY
  2. arquivo  .env          (linha  OPENROUTER_API_KEY=...)
  3. arquivo  .openrouter_key  (chave em texto puro, 1 linha)

Esses arquivos estão no .gitignore e NUNCA sobem para o GitHub.

Uso:
  python3 ask_openrouter.py "sua pergunta"
  python3 ask_openrouter.py --model "meta-llama/llama-3.3-70b-instruct:free" "pergunta"
  echo "pergunta longa" | python3 ask_openrouter.py -        # lê do stdin
  python3 ask_openrouter.py --json "pergunta"                # resposta crua
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "meta-llama/llama-3.3-70b-instruct:free"
TIMEOUT = 120


def load_key():
    key = os.environ.get("OPENROUTER_API_KEY")
    if key:
        return key.strip()
    if os.path.exists(".env"):
        with open(".env", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("OPENROUTER_API_KEY"):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    if os.path.exists(".openrouter_key"):
        with open(".openrouter_key", encoding="utf-8") as f:
            k = f.read().strip()
            if k:
                return k
    sys.exit(
        "Chave não encontrada. Defina OPENROUTER_API_KEY, ou crie o arquivo "
        ".env (OPENROUTER_API_KEY=...) ou .openrouter_key (chave pura)."
    )


def ask(model, prompt, key, system=None):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    body = json.dumps({"model": model, "messages": messages}).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/jvbenicio2000/banana",
            "X-Title": "banana-cli",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        sys.exit(f"Erro HTTP {e.code}: {detail}")
    except urllib.error.URLError as e:
        sys.exit(f"Erro de rede: {e.reason}")


def main():
    ap = argparse.ArgumentParser(description="Chama um modelo do OpenRouter.")
    ap.add_argument("prompt", help="a pergunta (use - para ler do stdin)")
    ap.add_argument("--model", default=DEFAULT_MODEL, help="ID do modelo")
    ap.add_argument("--system", default=None, help="mensagem de sistema (opcional)")
    ap.add_argument("--json", action="store_true", help="imprime a resposta JSON crua")
    args = ap.parse_args()

    prompt = sys.stdin.read() if args.prompt == "-" else args.prompt
    key = load_key()
    data = ask(args.model, prompt, key, args.system)

    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return
    try:
        print(data["choices"][0]["message"]["content"])
    except (KeyError, IndexError):
        print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
