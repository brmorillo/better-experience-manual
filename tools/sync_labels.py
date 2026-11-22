#!/usr/bin/env python3
"""
Creates, renames or updates the GitHub labels from .github/labels.yml (never deletes any).
A label with `previous: <old name>` renames that old label instead of creating a new one.
Runs in GitHub Actions (.github/workflows/labels.yml), with GITHUB_TOKEN and
GITHUB_REPOSITORY. To only see what would change: python tools/sync_labels.py --dry-run
"""
import argparse
import json
import os
import pathlib
import sys
import urllib.parse
import urllib.request

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
API = "https://api.github.com"


def call(method, path, token, body=None):
    req = urllib.request.Request(API + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read() or b"null")


def load():
    labels = yaml.safe_load((ROOT / ".github" / "labels.yml").read_text(encoding="utf-8"))
    seen = set()
    for lab in labels:
        name = lab["name"]
        if name.lower() in seen:
            raise SystemExit(f"duplicate label: {name}")
        seen.add(name.lower())
        lab["color"] = str(lab["color"]).lstrip("#").lower()
        if len(lab["color"]) != 6:
            raise SystemExit(f"{name}: the color must have 6 hex digits")
        if len(lab.get("description", "")) > 100:
            raise SystemExit(f"{name}: the description is longer than 100 characters")
    return labels


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="only show what would change")
    args = ap.parse_args()
    wanted = load()
    repo = os.environ.get("GITHUB_REPOSITORY", "brmorillo/better-experience-manual")
    token = os.environ.get("GITHUB_TOKEN", "")
    have, page = {}, 1
    while True:
        batch = call("GET", f"/repos/{repo}/labels?per_page=100&page={page}", token)
        for lab in batch:
            have[lab["name"].lower()] = lab
        if len(batch) < 100:
            break
        page += 1
    for lab in wanted:
        body = {"name": lab["name"], "color": lab["color"], "description": lab.get("description", "")}
        cur = have.get(lab["name"].lower())
        if cur is None:
            # Renamed label: `previous` holds old names, so existing Issues keep it.
            prev = lab.get("previous") or []
            for old in ([prev] if isinstance(prev, str) else prev):
                cur = have.get(str(old).lower())
                if cur is not None:
                    print(f"rename: {cur['name']} -> {lab['name']}")
                    if not args.dry_run:
                        call("PATCH", f"/repos/{repo}/labels/{urllib.parse.quote(cur['name'], safe='')}", token,
                             {"new_name": body["name"], "color": body["color"], "description": body["description"]})
                    break
            if cur is not None:
                continue
        if cur is None:
            print("create:", lab["name"])
            if not args.dry_run:
                call("POST", f"/repos/{repo}/labels", token, body)
        elif (cur["name"], cur["color"].lower(), cur.get("description") or "") != (body["name"], body["color"], body["description"]):
            print("update:", lab["name"])
            if not args.dry_run:
                call("PATCH", f"/repos/{repo}/labels/{urllib.parse.quote(cur['name'], safe='')}", token,
                     {"new_name": body["name"], "color": body["color"], "description": body["description"]})
        else:
            print("ok:", lab["name"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
