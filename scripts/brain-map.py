#!/usr/bin/env python3
"""Draw your AI operating system as a 3D map.

Reads every .md file in this folder, finds which files mention each other, and
writes brain.html: one page that opens in any browser. Needs Python 3 and nothing
else to run; the page loads its 3D drawing library from the web.

    python3 scripts/brain-map.py          # writes brain.html in the folder root
    python3 scripts/brain-map.py --open   # and opens it
    python3 scripts/brain-map.py PATH     # map a different folder
"""

import argparse
import json
import re
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".obsidian", ".trash"}
# Files for people browsing the repo, not part of the brain itself.
SKIP_ROOT_FILES = {"readme.md", "claude.md", "license.md", "contributing.md", "changelog.md"}
MAX_CHARS = 20000

GROUPS = {
    "core": ("Front door", "#D9D2C3"),
    "you": ("Who you are", "#FFB01F"),
    "rules": ("Rules", "#FF5F57"),
    "state": ("What's true now", "#3DDC97"),
    "decisions": ("Decisions", "#5AA9FF"),
    "inbox": ("Inbox", "#E6F35B"),
    "people": ("People", "#FF7AC6"),
    "projects": ("Projects", "#A98BFF"),
    "notes": ("Notes", "#9AA7B8"),
    "skills": ("Skills", "#4FE0E8"),
    "other": ("Other", "#6B717B"),
}

MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
WIKI_LINK = re.compile(r"\[\[([^\]|#]+)")
TICK_REF = re.compile(r"`([^`\s]+)`")


def group_for(rel: Path) -> str:
    parts = rel.parts
    name = rel.name.lower()
    if len(parts) == 1:
        return {
            "state.md": "state",
            "decisions.md": "decisions",
            "inbox.md": "inbox",
        }.get(name, "core")
    top = parts[0].lower()
    if top == "context":
        return {"me.md": "you", "rules.md": "rules"}.get(name, "you")
    if top == "notes":
        if len(parts) > 2 and parts[1].lower() in ("people", "projects"):
            return parts[1].lower()
        return "notes"
    if top == "skills":
        return "skills"
    return "other"


def label_for(rel: Path, text: str) -> str:
    if rel.stem.startswith("_template"):
        return f"{rel.parent.name} template"
    if rel.name == "SKILL.md":
        return rel.parent.name
    if rel.name.lower() in ("readme.md", "index.md") and len(rel.parts) > 1:
        return f"{rel.parent.name} index"
    match = re.search(r"^#\s+(.+)$", text, re.M)
    if match:
        title = re.sub(r"[:\s]*\[.*$", "", match.group(1)).strip()
        if title:
            return title if len(title) <= 32 else title[:31] + "…"
    return rel.stem


def collect(root: Path):
    files = {}
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if len(rel.parts) == 1 and rel.name.lower() in SKIP_ROOT_FILES:
            continue
        try:
            files[rel.as_posix()] = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
    return files


def normalize(path: str) -> str:
    parts = []
    for part in path.split("/"):
        if part == "..":
            if parts:
                parts.pop()
        elif part not in ("", "."):
            parts.append(part)
    return "/".join(parts)


def resolve(ref: str, source: str, files: dict, by_stem: dict):
    ref = ref.split("#")[0].strip()
    if not ref or "://" in ref or ref.startswith("mailto:") or any(c in ref for c in "<>[]{}*"):
        return None
    here = Path(source).parent.as_posix()
    bases = ["", here + "/"] if here != "." else [""]
    if ref.endswith("/"):
        for base in bases:
            for index in ("README.md", "index.md"):
                candidate = normalize(base + ref + index)
                if candidate in files:
                    return candidate
        return None
    if not ref.lower().endswith(".md"):
        return None
    for base in bases:
        candidate = normalize(base + ref)
        if candidate in files:
            return candidate
    matches = by_stem.get(Path(ref).stem.lower(), [])
    return matches[0] if len(matches) == 1 else None


def build_graph(root: Path):
    files = collect(root)
    by_stem = {}
    for rel in files:
        by_stem.setdefault(Path(rel).stem.lower(), []).append(rel)

    links = set()
    for source, text in files.items():
        refs = MD_LINK.findall(text) + TICK_REF.findall(text)
        for ref in refs:
            target = resolve(ref, source, files, by_stem)
            if target and target != source:
                links.add(tuple(sorted((source, target))))
        for name in WIKI_LINK.findall(text):
            matches = by_stem.get(name.strip().lower(), [])
            if len(matches) == 1 and matches[0] != source:
                links.add(tuple(sorted((source, matches[0]))))

    degree = {rel: 0 for rel in files}
    for a, b in links:
        degree[a] += 1
        degree[b] += 1

    nodes = []
    for rel, text in files.items():
        path = Path(rel)
        nodes.append({
            "id": rel,
            "label": label_for(path, text),
            "group": group_for(path),
            "template": path.stem.startswith("_template"),
            "degree": degree[rel],
            "text": text[:MAX_CHARS],
        })
    return {
        "name": root.resolve().name,
        "built": datetime.now().strftime("%b %d, %Y %I:%M %p"),
        "groups": {key: {"name": n, "color": c} for key, (n, c) in GROUPS.items()},
        "nodes": nodes,
        "links": [{"source": a, "target": b} for a, b in sorted(links)],
    }


def main():
    parser = argparse.ArgumentParser(description="Draw your AI operating system as a 3D map.")
    parser.add_argument("root", nargs="?", default=Path(__file__).resolve().parent.parent, type=Path)
    parser.add_argument("--out", type=Path, help="where to write the page (default: brain.html in the root)")
    parser.add_argument("--open", action="store_true", help="open the page in your browser")
    args = parser.parse_args()

    root = args.root.resolve()
    if not root.is_dir():
        sys.exit(f"Not a folder: {root}")
    graph = build_graph(root)
    if not graph["nodes"]:
        sys.exit(f"No .md files found in {root}")

    template = (Path(__file__).resolve().parent / "brain-map.html").read_text(encoding="utf-8")
    data = json.dumps(graph, ensure_ascii=False).replace("</", "<\\/")
    out = (args.out or root / "brain.html").resolve()
    out.write_text(template.replace("__BRAIN_DATA__", data), encoding="utf-8")

    print(f"{len(graph['nodes'])} files, {len(graph['links'])} connections")
    print(f"Wrote {out}")
    if args.open:
        webbrowser.open(out.as_uri())


if __name__ == "__main__":
    main()
