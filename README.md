# Your AI operating system: starter folder

Made by Andre Shonubi ([codedre](https://codedre.com)). Free to copy and make your own.
Click **Use this template** at the top of this page to get your own private copy.

This folder is a brain for your agents. It's plain text files that every agent reads before
it starts working. Agents forget between conversations. This folder doesn't. And because it's
just files, you can switch agent apps later (Grok Bot today, something else tomorrow) without
starting over.

## What's in here

| File | What it holds | How often it changes |
|---|---|---|
| `AGENTS.md` | The front door. What to read first, where everything is, which agent owns what | When you add an agent or a folder |
| `context/me.md` | Who you are, what you run, how you talk | Rarely |
| `context/rules.md` | The rules that never change, like "nothing goes out without my yes" | Rarely |
| `STATE.md` | What's true right now: what's live, what's stuck, what's next | Every week or so |
| `DECISIONS.md` | Calls you've made and why, so agents stop asking again | When you decide something |
| `inbox.md` | Ideas and to-dos you dump to look at later | All the time |
| `notes/` | One page per person, company or project | As you learn things |
| `skills/` | One folder per job you've explained more than once | When a job repeats |
| `scripts/` | Small tools, like the brain map | Rarely |

## Your first 30 minutes

1. **Fill in `context/me.md`.** Ten minutes, rough is fine. Talk it out loud to an agent and
   let it type if that's easier.
2. **Fill in `context/rules.md`.** Keep the approval rule. Add anything an agent should never do.
3. **Write three lines in `STATE.md`.** What you're working on, what's stuck, what's next.
4. **Fill in the agents table in `AGENTS.md`** with the team you built in the workshop:
   the orchestrator, the inbox and calendar agent, the research agent.
5. **Put the folder where your agents can read it.** See below.
6. **Test it.** Ask any agent: "Read AGENTS.md and tell me who I am and what's stuck." If the
   answer is right, it works.

## See your brain

Ask any agent to "show me my brain", or run this yourself from the folder:

```bash
python3 scripts/brain-map.py --open
```

It draws every file as a glowing dot and every link between files as a line, in 3D. Click a
dot to read the file. The map grows as you fill the folder in: every person, project and
decision you add shows up as a new dot. It needs Python 3 and an internet connection, and the
page it makes (`brain.html`) stays on your computer.

## Where to keep it

Pick one. You can move later.

- **Grok Bot:** keep the folder on the Bots' shared computer, or in a private GitHub repo the
  Bots can read. In each Bot's instructions, add: "Before any task, read AGENTS.md in
  [where the folder is] and follow it."
- **Claude Code:** open Claude Code in this folder. It reads `CLAUDE.md`, which points to `AGENTS.md`.
- **Codex and most other coding agents:** open them in this folder. They read `AGENTS.md` on their own.
- **Several apps at once:** a private GitHub repo. Every app clones it, and each one pulls
  before it reads and pushes after it writes.

## Keep it small

- One fact lives in one place. If two files disagree, fix one of them.
- `STATE.md` is rewritten, not added to. Keep it under a page.
- `DECISIONS.md` is added to, never edited. Newest on top.
- No passwords, API keys or card numbers in here, ever. Use a password manager.
- When an agent couldn't find something it needed, add a line to the table in `AGENTS.md`
  so the next one can.

## Want help?

If you want this set up for your business, book a call: codedre.com/call.
