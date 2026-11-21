#!/usr/bin/env python3
"""
Converte o manual (docs/<idioma>/*.md) no arquivo Lua que o mod carrega no jogo.

Uso:
    python tools/build_manual.py --check          # so valida (usado no GitHub Actions)
    python tools/build_manual.py --out <arquivo>  # gera o PA_ManualData.lua

Sem --out, grava em ../PersonalAssistant/Contents/mods/PersonalAssistant/42/
media/lua/client/PersonalAssistant/PA_ManualData.lua (pasta vizinha do mod).

Markdown aceito (subconjunto, ver CONTRIBUTING.md): # titulo, ## subtitulo,
### subtitulo menor, paragrafos, listas com "-" ou "1.", > dica, **negrito**,
`codigo`, [link](url) e <!-- comentarios -->. Tabelas e imagens nao aparecem
no jogo.
"""
import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CONFIG = ROOT / "manual.config.json"
DEFAULT_OUT = (ROOT.parent / "PersonalAssistant" / "Contents" / "mods" / "PersonalAssistant"
               / "42" / "media" / "lua" / "client" / "PersonalAssistant" / "PA_ManualData.lua")

HIGHLIGHT = "1,0.82,0.35"   # negrito
CODE = "0.55,0.8,1"         # `codigo`
TIP = "0.6,0.9,0.6"         # > dica
H3 = "0.95,0.95,0.75"       # ### subtitulo menor


class ManualError(Exception):
    pass


def clean(text):
    """O painel de texto do jogo trata "<" como inicio de comando: troca por "(".
    O ">" sozinho e seguro (usado nos caminhos de menu: Opcoes > Mods)."""
    return text.replace("<", "(")


def inline(text):
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)                 # imagens
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)              # links -> texto
    parts = []
    pos = 0
    pattern = re.compile(r"\*\*(.+?)\*\*([.,:;!?)]*)|`([^`]+)`([.,:;!?)]*)")
    for m in pattern.finditer(text):
        parts.append(clean(text[pos:m.start()]))
        if m.group(1) is not None:
            parts.append(f" <PUSHRGB:{HIGHLIGHT}> {clean(m.group(1) + m.group(2))} <POPRGB> ")
        else:
            parts.append(f" <PUSHRGB:{CODE}> {clean(m.group(3) + m.group(4))} <POPRGB> ")
        pos = m.end()
    parts.append(clean(text[pos:]))
    out = "".join(parts)
    out = out.replace("**", "")
    return re.sub(r"[ \t]+", " ", out).strip()


def convert(md, source):
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    lines = md.replace("\r\n", "\n").split("\n")
    title = None
    blocks = []          # cada bloco vira uma "linha" do painel
    para = []

    def flush():
        if para:
            blocks.append(("p", inline(" ".join(para))))
            para.clear()

    for raw in lines:
        line = raw.rstrip()
        s = line.strip()
        if not s:
            flush()
            blocks.append(("gap", ""))
            continue
        if s.startswith("|"):
            raise ManualError(f"{source}: tabelas nao aparecem no jogo; use uma lista")
        if s.startswith("# "):
            flush()
            if title is not None:
                raise ManualError(f"{source}: so pode haver um titulo '# ' por arquivo")
            title = s[2:].strip()
            continue
        if s.startswith("### "):
            flush(); blocks.append(("h3", inline(s[4:]))); continue
        if s.startswith("## "):
            flush(); blocks.append(("h2", inline(s[3:]))); continue
        m = re.match(r"^([-*+])\s+(.*)$", s)
        if m:
            flush(); blocks.append(("li", inline(m.group(2)))); continue
        m = re.match(r"^(\d+)[.)]\s+(.*)$", s)
        if m:
            flush(); blocks.append(("ol", m.group(1) + ". " + inline(m.group(2)))); continue
        if s.startswith(">"):
            flush(); blocks.append(("tip", inline(s.lstrip("> ")))); continue
        if raw.startswith("  ") and blocks and blocks[-1][0] in ("li", "ol") and not para:
            kind, txt = blocks[-1]
            blocks[-1] = (kind, txt + " " + inline(s))
            continue
        para.append(s)
    flush()

    if not title:
        raise ManualError(f"{source}: falta o titulo '# ...' no comeco do arquivo")

    out = [f"<H1> {clean(title)} <LINE> <TEXT> "]
    prev = "head"
    for kind, txt in blocks:
        if kind == "gap":
            if prev != "head":
                prev = "gap"
            continue
        if prev == "head" and kind not in ("h2", "h3"):
            sep = " "                              # o titulo ja termina com <LINE>
        elif prev in ("li", "ol", "p") and kind in ("li", "ol") and prev != "gap":
            sep = " <LINE> "                       # lista colada no item/paragrafo anterior
        else:
            sep = " <LINE> <LINE> "
        if kind == "h2":
            out.append(f"{sep}<H2> {txt} <LINE> <TEXT> ")
            prev = "head"
            continue
        elif kind == "h3":
            out.append(f"{sep}<RGB:{H3}> {txt} <TEXT> ")
            prev = "head"
            continue
        elif kind == "li":
            out.append(f"{sep} - {txt}")
        elif kind == "ol":
            out.append(f"{sep} {txt}")
        elif kind == "tip":
            out.append(f"{sep}<RGB:{TIP}> {txt} <TEXT> ")
        else:
            out.append(f"{sep}{txt}")
        prev = kind
    text = "".join(out)
    text = re.sub(r"(<LINE> ){3,}", "<LINE> <LINE> ", text)
    return clean(title), re.sub(r"[ \t]+", " ", text).strip()


def lua_long(s):
    level = 1
    while ("]" + "=" * level + "]") in s:
        level += 1
    eq = "=" * level
    return f"[{eq}[{s}]{eq}]"


def lua_str(s):
    return json.dumps(s, ensure_ascii=False)


def build():
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    langs = cfg["languages"]                    # {"pt-BR": "PTBR", "en": "EN"}
    data = {}
    for folder, code in langs.items():
        files = sorted((DOCS / folder).glob("*.md"))
        if not files:
            raise ManualError(f"docs/{folder}: nenhum capitulo")
        chapters = []
        for f in files:
            rel = f.relative_to(ROOT).as_posix()
            title, text = convert(f.read_text(encoding="utf-8"), rel)
            plain = re.sub(r"<[^>]*>", " ", text)
            chapters.append({"id": f.stem, "title": title, "file": rel, "text": text,
                             "plain": re.sub(r"\s+", " ", plain).strip()})
        data[code] = chapters
    counts = {k: len(v) for k, v in data.items()}
    if len(set(counts.values())) > 1:
        print(f"aviso: idiomas com numero diferente de capitulos: {counts}", file=sys.stderr)
    return cfg, data


def render_lua(cfg, data):
    lines = [
        "-- GERADO AUTOMATICAMENTE por tools/build_manual.py a partir do repositorio",
        "-- do manual. Nao edite aqui: edite os arquivos .md e rode o script de novo.",
        "PersonalAssistant = PersonalAssistant or {}",
        "PersonalAssistant.ManualData = {",
        f"    repo = {lua_str(cfg.get('repo', ''))},",
        f"    branch = {lua_str(cfg.get('branch', 'main'))},",
        "    langs = {",
    ]
    for code, chapters in data.items():
        lines.append(f"        {code} = {{")
        for c in chapters:
            lines.append("            {")
            lines.append(f"                id = {lua_str(c['id'])},")
            lines.append(f"                title = {lua_str(c['title'])},")
            lines.append(f"                file = {lua_str(c['file'])},")
            lines.append(f"                plain = {lua_long(c['plain'])},")
            lines.append(f"                text = {lua_long(c['text'])},")
            lines.append("            },")
        lines.append("        },")
    lines += ["    },", "}", ""]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="so valida os arquivos")
    ap.add_argument("--out", type=pathlib.Path, default=DEFAULT_OUT)
    args = ap.parse_args()
    try:
        cfg, data = build()
    except ManualError as e:
        print("erro:", e, file=sys.stderr)
        return 1
    for code, chapters in data.items():
        print(f"{code}: {len(chapters)} capitulos - " + ", ".join(c["id"] for c in chapters))
    if args.check:
        print("ok")
        return 0
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render_lua(cfg, data), encoding="utf-8", newline="\n")
    print("gravado:", args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
