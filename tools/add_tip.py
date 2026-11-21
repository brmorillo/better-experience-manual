#!/usr/bin/env python3
"""
Adiciona uma dica da comunidade em dicas/<idioma>/<id>.md.

Usado pelo robo do GitHub (.github/workflows/dica.yml) com o evento do pedido:
    python tools/add_tip.py --event evento.json

Ou na mao:
    python tools/add_tip.py --page pt-BR/gps --author seu-usuario --text "Sua dica"
"""
import argparse
import datetime
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_manual as bm  # noqa: E402


def parse_issue_body(body):
    """O formulario vira '### Rotulo\\n\\nvalor'. Devolve {rotulo: valor}."""
    fields, cur = {}, None
    for line in (body or "").replace("\r\n", "\n").split("\n"):
        m = re.match(r"^###\s+(.*)$", line)
        if m:
            cur = m.group(1).strip().lower()
            fields[cur] = []
        elif cur is not None:
            fields[cur].append(line)
    return {k: "\n".join(v).strip() for k, v in fields.items()}


def field(fields, prefix):
    for k, v in fields.items():
        if k.startswith(prefix):
            return "" if v == "_No response_" else v
    return ""


def resolve_page(page):
    _, langs = bm.load_all()
    page = page.strip().strip("/").replace("\\", "/")
    if page.startswith("docs/"):
        page = page[5:]
    lang, _, rest = page.partition("/")
    if lang not in langs:
        raise bm.ManualError(f"idioma '{lang}' nao existe (use {', '.join(langs)})")
    parts = [p for p in rest.split("/") if p]
    if parts and parts[-1].lower() == "readme.md":
        parts.pop()
    pid = bm.slug(parts[-1]) if parts else bm.ROOT_ID
    if pid not in langs[lang][2]:
        raise bm.ManualError(f"pagina '{pid}' nao existe em docs/{lang}")
    return lang, pid


def add(page, author, text, date=None, ref=""):
    lang, pid = resolve_page(page)
    author = re.sub(r"[^A-Za-z0-9_.-]", "", author.lstrip("@")) or "anonimo"
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"^\s*#+\s*", "", text, flags=re.M).strip()   # sem titulos
    if not text:
        raise bm.ManualError("a dica esta vazia")
    if len(text) > bm.MAX_TIP:
        raise bm.ManualError(f"a dica tem {len(text)} caracteres (maximo {bm.MAX_TIP})")
    date = date or datetime.date.today().isoformat()
    head = f"## @{author} | {date}" + (f" | {ref}" if ref else "")
    path = bm.TIPS / lang / f"{pid}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    old = path.read_text(encoding="utf-8").rstrip() + "\n\n" if path.exists() else ""
    if ref:
        # pedido editado: troca a dica antiga desse pedido pela nova
        old = re.sub(rf"^##[^\n]*\|\s*{re.escape(ref)}\s*\n.*?(?=^## |\Z)", "", old,
                     flags=re.M | re.S).rstrip()
        old = old + "\n\n" if old else ""
    new = old + head + "\n\n" + text + "\n"
    bm.parse_tips(new, str(path))          # mesma validacao do build
    path.write_text(new, encoding="utf-8", newline="\n")
    return path.relative_to(bm.ROOT).as_posix()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--event", type=pathlib.Path)
    ap.add_argument("--github-output", type=pathlib.Path)
    ap.add_argument("--page")
    ap.add_argument("--author")
    ap.add_argument("--text")
    args = ap.parse_args()
    try:
        if args.event:
            ev = json.loads(args.event.read_text(encoding="utf-8"))
            issue = ev["issue"]
            fields = parse_issue_body(issue.get("body"))
            rel = add(field(fields, "página") or field(fields, "pagina"),
                      issue["user"]["login"], field(fields, "dica"),
                      issue["created_at"][:10], f"#{issue['number']}")
        else:
            if not (args.page and args.author and args.text):
                ap.error("use --event, ou --page, --author e --text")
            rel = add(args.page, args.author, args.text)
    except bm.ManualError as e:
        print("erro:", e, file=sys.stderr)
        return 1
    print("dica adicionada em", rel)
    if args.github_output:
        with args.github_output.open("a", encoding="utf-8") as f:
            f.write(f"file={rel}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
