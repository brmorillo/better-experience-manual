#!/usr/bin/env python3
"""
Adds a community tip to tips/<language>/<id>.md.

Used by the GitHub bot (.github/workflows/tip.yml) with the issue event:
    python tools/add_tip.py --event event.json

Or by hand:
    python tools/add_tip.py --page en/gps --author your-username --text "Your tip"
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
    """The issue form becomes '### Label\\n\\nvalue'. Returns {label: value}."""
    fields, cur = {}, None
    for line in (body or "").replace("\r\n", "\n").split("\n"):
        m = re.match(r"^###\s+(.*)$", line)
        if m:
            cur = m.group(1).strip().lower()
            fields[cur] = []
        elif cur is not None:
            fields[cur].append(line)
    return {k: "\n".join(v).strip() for k, v in fields.items()}


def field(fields, *prefixes):
    """Value of the first label that starts with any of the prefixes.
    Accepts both the English-first labels ("Page / Pagina") and the old
    Portuguese-first ones ("Pagina / Page")."""
    for k, v in fields.items():
        if k.startswith(prefixes):
            return "" if v == "_No response_" else v
    return ""


def resolve_page(page):
    _, langs = bm.load_all()
    page = page.strip().strip("/").replace("\\", "/")
    if page.startswith("docs/"):
        page = page[5:]
    lang, _, rest = page.partition("/")
    if lang not in langs:
        raise bm.ManualError(f"language '{lang}' does not exist (use {', '.join(langs)})")
    parts = [p for p in rest.split("/") if p]
    if parts and parts[-1].lower() == "readme.md":
        parts.pop()
    pid = bm.slug(parts[-1]) if parts else bm.ROOT_ID
    if pid not in langs[lang][2]:
        raise bm.ManualError(f"page '{pid}' does not exist in docs/{lang}")
    return lang, pid


def add(page, author, text, date=None, ref=""):
    lang, pid = resolve_page(page)
    author = re.sub(r"[^A-Za-z0-9_.-]", "", author.lstrip("@")) or "anonymous"
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"^\s*#+\s*", "", text, flags=re.M).strip()   # no headings
    if not text:
        raise bm.ManualError("the tip is empty")
    if len(text) > bm.MAX_TIP:
        raise bm.ManualError(f"the tip has {len(text)} characters (max {bm.MAX_TIP})")
    date = date or datetime.date.today().isoformat()
    head = f"## @{author} | {date}" + (f" | {ref}" if ref else "")
    path = bm.TIPS / lang / f"{pid}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    old = path.read_text(encoding="utf-8").rstrip() + "\n\n" if path.exists() else ""
    if ref:
        # edited issue: replace this issue's old tip with the new one
        old = re.sub(rf"^##[^\n]*\|\s*{re.escape(ref)}\s*\n.*?(?=^## |\Z)", "", old,
                     flags=re.M | re.S).rstrip()
        old = old + "\n\n" if old else ""
    new = old + head + "\n\n" + text + "\n"
    bm.parse_tips(new, str(path))          # same validation as the build
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
            rel = add(field(fields, "page", "página", "pagina"),
                      issue["user"]["login"], field(fields, "tip", "dica"),
                      issue["created_at"][:10], f"#{issue['number']}")
        else:
            if not (args.page and args.author and args.text):
                ap.error("use --event, or --page, --author and --text")
            rel = add(args.page, args.author, args.text)
    except bm.ManualError as e:
        print("error:", e, file=sys.stderr)
        return 1
    print("tip added to", rel)
    if args.github_output:
        with args.github_output.open("a", encoding="utf-8") as f:
            f.write(f"file={rel}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
