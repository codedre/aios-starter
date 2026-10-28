---
name: brain-map
description: Draw this folder as a 3D map of files and the links between them, so you can see your AI operating system. Use when asked to "show me my brain", "map my brain", "visualize my notes", or after adding a lot of new pages.
---

# Brain map

## Steps

1. From the folder root, run `python3 scripts/brain-map.py`. It reads every `.md` file, finds
   which files mention each other (markdown links, `[[wiki links]]`, and file paths in
   backticks), and writes `brain.html` in the root.
2. Open `brain.html` in a browser (`python3 scripts/brain-map.py --open` does both). If you're
   on a computer the person can't see, send them the file instead.
3. Tell them in one line: how many files and connections it found, and anything that stands
   out, like a file nothing links to.

## What they'll see

- Each file is a glowing dot, colored by what kind of file it is (who you are, rules, what's
  true now, decisions, people, projects, skills). Busier files are bigger.
- Lines are connections between files. Hover a dot to light up its connections. Click it to
  read the file in a side panel.
- The legend at the bottom left hides or shows each kind of file. "Find a file" jumps to one.

## Where it stops

- `brain.html` holds a copy of every file's text. It's in `.gitignore` so it never gets
  committed. Don't post it or send it to anyone but the person whose brain it is.
- The page loads its 3D drawing library from the web, so it needs an internet connection.

## How you know it worked

- The script prints a file count and a connection count, and `brain.html` exists.
- The count matches roughly how many `.md` files are in the folder (the root README, CLAUDE.md
  and LICENSE are left out on purpose).
