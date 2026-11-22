#!/usr/bin/env python3
"""
Converts the manual into the Lua file (and images) that the mod loads in game.

    docs/<language>/...      official guide. The folder tree IS the in-game tree:
                             each folder becomes a section, each .md a page.
    tips/<language>/<id>.md  community tips for each page (unofficial).
    ```mermaid               flowcharts: GitHub draws them by itself; for the
                             game they become PNGs (tools/mermaid_png.py)
                             shipped with the mod.

Usage:
    python tools/build_manual.py --check        # validate only (GitHub Actions)
    python tools/build_manual.py                # write everything into the mod folder
    python tools/build_manual.py --out x.lua --images folder/
                                                # write somewhere else (to look
                                                # at the diagram images)

Without --out/--images, it writes into the sibling mod folder (../PersonalAssistant/...):
    42/media/lua/client/PersonalAssistant/PA_ManualData.lua
    42/media/textures/PA_Manual/d_*.png
Requires Pillow:  pip install pillow

Tree rules (see CONTRIBUTING.md):
  - The number at the start of a name ("01-", "02-") only sets the order; it
    is hidden in game.
  - A page id is the file name without the number and without ".md"
    ("03-map-and-gps/02-gps.md" -> "gps"). A folder id is its name without
    the number. The root (docs/<language>/README.md) has the id "inicio".
  - Ids must be unique within a language: tips find their page by id, so
    moving a file to another folder does not lose its tips.
  - A folder's README.md is the text of the section itself (title and intro).
  - Files and folders starting with "_" or "." are ignored.
"""
import argparse
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import mermaid_png  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
TIPS = ROOT / "tips"
CONFIG = ROOT / "manual.config.json"
MOD_MEDIA = ROOT.parent / "PersonalAssistant" / "Contents" / "mods" / "PersonalAssistant" / "42" / "media"
DEFAULT_OUT = MOD_MEDIA / "lua" / "client" / "PersonalAssistant" / "PA_ManualData.lua"
DEFAULT_IMAGES = MOD_MEDIA / "textures" / "PA_Manual"
GAME_IMAGE_DIR = "media/textures/PA_Manual"   # path the game uses in getTexture

ROOT_ID = "inicio"
MAX_TIP = 600              # characters per tip
HIGHLIGHT = "1,0.82,0.35"  # bold
CODE = "0.55,0.8,1"        # `code`
TIP = "0.6,0.9,0.6"        # > tip
H3 = "0.95,0.95,0.75"      # ### smaller subheading
ORDER_RE = re.compile(r"^(\d+)[-_ .]+")


class ManualError(Exception):
    pass


# ---------------------------------------------------------------------------
# Diagrams
# ---------------------------------------------------------------------------

class Diagrams:
    """Collects the manual's diagrams: validates, measures and renders the PNGs."""

    def __init__(self):
        self.images = {}    # file name -> image (PIL)

    def add(self, source, where):
        try:
            g = mermaid_png.parse(source, where)
            name = mermaid_png.image_name(source)
            if name not in self.images:
                self.images[name] = mermaid_png.render(g)
        except mermaid_png.DiagramError as e:
            raise ManualError(str(e))
        except ImportError:
            raise ManualError("diagrams require Pillow: pip install pillow")
        img = self.images[name]
        return f"<IMAGECENTRE:{GAME_IMAGE_DIR}/{name},{img.width},{img.height}>", g.labels()

    def write(self, folder):
        folder.mkdir(parents=True, exist_ok=True)
        for old in folder.glob("d_*.png"):
            if old.name not in self.images:
                old.unlink()
        for name, img in self.images.items():
            target = folder / name
            if not target.exists():
                img.save(target, optimize=True)


# ---------------------------------------------------------------------------
# Markdown -> in-game rich text (ISRichTextPanel)
# ---------------------------------------------------------------------------

def clean(text):
    """The game panel treats "<" as the start of a command: replace it with "(".
    A lone ">" is safe (menu paths: Options > Mods)."""
    return text.replace("<", "(")


def inline(text):
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)       # images
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)    # links -> text
    parts, pos = [], 0
    pattern = re.compile(r"\*\*(.+?)\*\*([.,:;!?)]*)|`([^`]+)`([.,:;!?)]*)")
    for m in pattern.finditer(text):
        parts.append(clean(text[pos:m.start()]))
        if m.group(1) is not None:
            parts.append(f" <PUSHRGB:{HIGHLIGHT}> {clean(m.group(1) + m.group(2))} <POPRGB> ")
        else:
            parts.append(f" <PUSHRGB:{CODE}> {clean(m.group(3) + m.group(4))} <POPRGB> ")
        pos = m.end()
    parts.append(clean(text[pos:]))
    out = "".join(parts).replace("**", "")
    return re.sub(r"[ \t]+", " ", out).strip()


def plain_of(rich):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]*>", " ", rich)).strip()


def convert(md, source, diagrams=None):
    """Returns (title, rich text, extra text for search). The title comes from the '# ' line."""
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    title, blocks, para, extra = None, [], [], []
    fence, fence_lines = None, []
    diagrams = diagrams if diagrams is not None else Diagrams()

    def flush():
        if para:
            blocks.append(("p", inline(" ".join(para))))
            para.clear()

    for raw in md.replace("\r\n", "\n").split("\n"):
        s = raw.strip()
        if fence is not None:
            if s.startswith("```"):
                if fence == "mermaid":
                    tag, labels = diagrams.add("\n".join(fence_lines), source)
                    blocks.append(("img", tag))
                    extra.append(labels)
                else:
                    blocks.append(("code", list(fence_lines)))
                fence, fence_lines = None, []
            else:
                fence_lines.append(raw.rstrip())
            continue
        if s.startswith("```"):
            flush()
            fence = s[3:].strip().lower()
            continue
        if not s:
            flush(); blocks.append(("gap", "")); continue
        if s.startswith("|"):
            raise ManualError(f"{source}: tables do not show in game; use a list")
        if s.startswith("# "):
            flush()
            if title is not None:
                raise ManualError(f"{source}: only one '# ' title is allowed per file")
            title = s[2:].strip(); continue
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
            blocks[-1] = (kind, txt + " " + inline(s)); continue
        para.append(s)
    flush()
    if fence is not None:
        raise ManualError(f"{source}: unclosed ``` block")
    if not title:
        raise ManualError(f"{source}: missing the '# ...' title at the start of the file")

    out, prev = [f"<H1> {clean(title)} <LINE> <TEXT> "], "head"
    for kind, txt in blocks:
        if kind == "gap":
            if prev not in ("head", "img"):
                prev = "gap"
            continue
        if prev == "head" and kind not in ("h2", "h3"):
            sep = " "                      # the title already ends with <LINE>
        elif prev == "img":
            sep = " <LINE> "               # the image already ends with <LINE>
        elif prev in ("li", "ol", "p") and kind in ("li", "ol"):
            sep = " <LINE> "               # list right after the previous paragraph/item
        else:
            sep = " <LINE> <LINE> "
        if kind == "h2":
            out.append(f"{sep}<H2> {txt} <LINE> <TEXT> "); prev = "head"; continue
        if kind == "h3":
            out.append(f"{sep}<RGB:{H3}> {txt} <TEXT> "); prev = "head"; continue
        if kind == "li":
            out.append(f"{sep} - {txt}")
        elif kind == "ol":
            out.append(f"{sep} {txt}")
        elif kind == "tip":
            out.append(f"{sep}<RGB:{TIP}> {txt} <TEXT> ")
        elif kind == "img":
            out.append(f"{sep}{txt} <LINE> ")
        elif kind == "code":
            out.append(sep + " <LINE> ".join(f"<PUSHRGB:{CODE}> {clean(l.strip()) or '.'} <POPRGB>" for l in txt))
        else:
            out.append(f"{sep}{txt}")
        prev = kind
    text = re.sub(r"(<LINE> ){3,}", "<LINE> <LINE> ", "".join(out))
    return clean(title), re.sub(r"[ \t]+", " ", text).strip(), " ".join(extra)


# ---------------------------------------------------------------------------
# Tree
# ---------------------------------------------------------------------------

def order_key(path):
    m = ORDER_RE.match(path.name)
    return (0, int(m.group(1)), path.name.lower()) if m else (1, 0, path.name.lower())


def slug(name):
    name = re.sub(r"\.md$", "", name, flags=re.I)
    return ORDER_RE.sub("", name).strip().lower()


def pretty(name):
    s = ORDER_RE.sub("", name).replace("-", " ").replace("_", " ").strip()
    return s[:1].upper() + s[1:]


def build_tree(lang_dir, rel_root, diagrams=None):
    ids = {}

    def key_of(path):
        """Position by numbering ('3/2'), used to compare languages."""
        parts = []
        for part in path.relative_to(lang_dir).parts:
            m = ORDER_RE.match(part)
            parts.append((m.group(1).lstrip("0") or "0") if m else "?" + slug(part))
        return "/".join(parts)

    def rel_of(path):
        return (rel_root / path.relative_to(lang_dir).as_posix()).as_posix()

    def register(node_id, rel):
        if not re.match(r"^[a-z0-9][a-z0-9-]*$", node_id):
            raise ManualError(f"{rel}: use only lowercase unaccented letters, digits and '-' in the name "
                              f"(id '{node_id}')")
        if node_id in ids:
            raise ManualError(f"{rel}: the id '{node_id}' already exists in {ids[node_id]}; "
                              "rename one of them")
        ids[node_id] = rel

    def folder(path, node_id):
        register(node_id, rel_of(path) + "/")
        node = {"kind": "folder", "id": node_id, "title": pretty(path.name), "file": "", "text": "",
                "extra": "", "key": key_of(path) if path != lang_dir else ""}
        readme = next((p for p in path.iterdir() if p.name.lower() == "readme.md"), None)
        if readme:
            node["file"] = rel_of(readme)
            node["title"], node["text"], node["extra"] = convert(readme.read_text(encoding="utf-8"),
                                                                 node["file"], diagrams)
        children = []
        for child in sorted(path.iterdir(), key=order_key):
            if child.name.startswith(("_", ".")) or child.name.lower() == "readme.md":
                continue
            if child.is_dir():
                children.append(folder(child, slug(child.name)))
            elif child.suffix.lower() == ".md":
                crel = rel_of(child)
                cid = slug(child.name)
                register(cid, crel)
                title, text, extra = convert(child.read_text(encoding="utf-8"), crel, diagrams)
                children.append({"kind": "page", "id": cid, "title": title, "file": crel, "text": text,
                                 "extra": extra, "key": key_of(child)})
        node["children"] = children
        return node

    return folder(lang_dir, ROOT_ID), ids


# ---------------------------------------------------------------------------
# Community tips
# ---------------------------------------------------------------------------

TIP_HEAD = re.compile(r"^##\s+(.+?)\s*$")


def parse_tips(md, source):
    """Each tip starts with '## @author | YYYY-MM-DD | #issue' and runs until the next one."""
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    tips, cur = [], None
    for line in md.replace("\r\n", "\n").split("\n"):
        m = TIP_HEAD.match(line)
        if m:
            if cur:
                tips.append(cur)
            fields = [f.strip() for f in m.group(1).split("|")]
            cur = {"author": fields[0], "date": fields[1] if len(fields) > 1 else "",
                   "ref": fields[2] if len(fields) > 2 else "", "lines": []}
        elif line.startswith("# "):
            continue
        elif cur is not None:
            cur["lines"].append(line.strip())
        elif line.strip():
            raise ManualError(f"{source}: text before the first tip; each tip starts with '## @author | date'")
    if cur:
        tips.append(cur)
    out = []
    for t in tips:
        body = " ".join(l for l in t.pop("lines") if l).strip()
        if not body:
            raise ManualError(f"{source}: tip by {t['author']} is empty")
        if len(body) > MAX_TIP:
            raise ManualError(f"{source}: tip by {t['author']} has {len(body)} characters (max {MAX_TIP})")
        t["author"], t["date"], t["ref"] = clean(t["author"]), clean(t["date"]), clean(t["ref"])
        t["text"] = inline(body)
        out.append(t)
    return out


def attach_tips(tree, ids, folder_name):
    tip_dir = TIPS / folder_name
    by_id = {}
    if tip_dir.is_dir():
        for f in sorted(tip_dir.glob("*.md")):
            if f.name.lower() == "readme.md" or f.name.startswith(("_", ".")):
                continue
            rel = f.relative_to(ROOT).as_posix()
            if f.stem not in ids:
                raise ManualError(f"{rel}: there is no page with the id '{f.stem}' in docs/{folder_name}. "
                                  "If the page was renamed, rename this file too.")
            by_id[f.stem] = parse_tips(f.read_text(encoding="utf-8"), rel)
    total = 0

    def walk(node):
        nonlocal total
        node["tips"] = by_id.get(node["id"], [])
        total += len(node["tips"])
        node["plain"] = plain_of(node["title"] + " " + node["text"] + " " + node.get("extra", "") + " "
                                 + " ".join(t["text"] for t in node["tips"]))
        for c in node.get("children", []):
            walk(c)
    walk(tree)
    return total


def load_all(diagrams=None):
    """Tree + ids for each language (also used by tools/add_tip.py)."""
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    diagrams = diagrams if diagrams is not None else Diagrams()
    out = {}
    for folder_name, code in cfg["languages"].items():
        lang_dir = DOCS / folder_name
        if not (lang_dir / "README.md").exists():
            raise ManualError(f"docs/{folder_name}/README.md: the language home page is missing")
        tree, ids = build_tree(lang_dir, pathlib.PurePosixPath("docs") / folder_name, diagrams)
        out[folder_name] = (code, tree, ids)
    return cfg, out


def compare_languages(langs):
    """Warns (without failing) when one language has a page the other does not."""
    keys = {}
    for folder_name, (_, tree, _) in langs.items():
        found = {}

        def walk(n):
            if n.get("key"):
                found[n["key"]] = n["file"] or n["id"]
            for c in n.get("children", []):
                walk(c)
        walk(tree)
        keys[folder_name] = found
    warnings = []
    for a in keys:
        for b in keys:
            if a != b:
                for k, f in sorted(keys[a].items()):
                    if k not in keys[b]:
                        warnings.append(f"warning: {f} has no counterpart in docs/{b}/ (same numbering {k})")
    return warnings


def build():
    diagrams = Diagrams()
    cfg, langs = load_all(diagrams)
    data, report = {}, []
    for folder_name, (code, tree, ids) in langs.items():
        tips = attach_tips(tree, ids, folder_name)
        data[code] = {"folder": folder_name, "root": tree}
        report.append(f"{code}: {len(ids)} pages/sections, {tips} tips")
    templates = 0
    for f in sorted((ROOT / "templates").glob("*/*.md")):
        convert(f.read_text(encoding="utf-8"), f.relative_to(ROOT).as_posix(), Diagrams())
        templates += 1
    report.append(f"diagrams: {len(diagrams.images)}, templates ok: {templates}")
    report.extend(compare_languages(langs))
    return cfg, data, report, diagrams


# ---------------------------------------------------------------------------
# Lua output
# ---------------------------------------------------------------------------

def lua_long(s):
    level = 1
    while ("]" + "=" * level + "]") in s:
        level += 1
    eq = "=" * level
    return f"[{eq}[{s}]{eq}]"


def lua_str(s):
    return json.dumps(s, ensure_ascii=False)


def lua_node(node, ind):
    p = "    " * ind
    out = [p + "{",
           f"{p}    kind = {lua_str(node['kind'])}, id = {lua_str(node['id'])},",
           f"{p}    title = {lua_str(node['title'])}, file = {lua_str(node['file'])},",
           f"{p}    text = {lua_long(node['text'])},",
           f"{p}    plain = {lua_long(node['plain'])},"]
    if node["tips"]:
        out.append(f"{p}    tips = {{")
        for t in node["tips"]:
            out.append(f"{p}        {{ author = {lua_str(t['author'])}, date = {lua_str(t['date'])}, "
                       f"ref = {lua_str(t['ref'])}, text = {lua_long(t['text'])} }},")
        out.append(f"{p}    }},")
    if node["kind"] == "folder":
        out.append(f"{p}    children = {{")
        for c in node["children"]:
            out.extend(lua_node(c, ind + 2))
        out.append(f"{p}    }},")
    out.append(p + "},")
    return out


def render_lua(cfg, data):
    lines = [
        "-- GENERATED AUTOMATICALLY by tools/build_manual.py from the manual",
        "-- repository. Do not edit here: edit the .md files and run the script again.",
        "PersonalAssistant = PersonalAssistant or {}",
        "PersonalAssistant.ManualData = {",
        f"    repo = {lua_str(cfg.get('repo', ''))},",
        f"    branch = {lua_str(cfg.get('branch', 'main'))},",
        "    langs = {",
    ]
    for code, d in data.items():
        lines.append(f"        {code} = {{")
        lines.append(f"            folder = {lua_str(d['folder'])},")
        lines.append("            root =")
        lines.extend(lua_node(d["root"], 3))
        lines.append("        },")
    lines += ["    },", "}", ""]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="only validate the files")
    ap.add_argument("--out", type=pathlib.Path, default=DEFAULT_OUT)
    ap.add_argument("--images", type=pathlib.Path, default=DEFAULT_IMAGES, help="folder for the diagram PNGs")
    args = ap.parse_args()
    try:
        cfg, data, report, diagrams = build()
    except ManualError as e:
        print("error:", e, file=sys.stderr)
        return 1
    print("\n".join(report))
    if args.check:
        print("ok")
        return 0
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render_lua(cfg, data), encoding="utf-8", newline="\n")
    diagrams.write(args.images)
    print("written:", args.out)
    print("images:", args.images)
    return 0


if __name__ == "__main__":
    sys.exit(main())
