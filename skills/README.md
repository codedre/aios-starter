# Skills

A skill is a job written down once, so any agent can do it the same way every time.
If you've explained a job to an agent twice, make it a skill.

One folder per skill, with a `SKILL.md` inside. Every skill answers four things:

1. **When to use it:** the words or situation that should trigger it.
2. **The steps:** in order, short.
3. **Where it stops for approval:** anything that sends, spends or deletes.
4. **How you know it worked:** what you check before calling it done.

`morning-brief/` is an example. Copy it to start your own.

In Grok Bot you can also say "save this as a skill called [name]" after a job goes well,
then type `/` to call it. Copy the saved steps into a folder here too, so other agent apps
can use them.

## Skills in this folder

| Skill | What it does |
|---|---|
| `morning-brief` | A short morning summary of today's calendar, what needs a reply, and what's stuck |
