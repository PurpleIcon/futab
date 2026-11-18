---
name: review-skills
description: "Reviews FuTab's agent skills (`.claude/skills/`): their layout and names, front matter, the files they point at, how much they load and how clearly they read, and whether they agree with the rules. Reports what is wrong, most serious first, and fixes it once the user says so. Use whenever the task is to review, check, lint or tidy the skills, or after adding, renaming or editing one."
argument-hint: "[skill-name ...]"
---

# Review the skills

A skill is a task guide that Claude Code reads on demand. Only its `description` is in every session, so the description decides whether the skill is used at all; the body is read when it is, and should hold what the task needs every time, no more. This skill checks FuTab's skills against that, and against the layout FuTab keeps.

It reads and reports. **Change nothing until I say so.**

## Which skills

`$ARGUMENTS` holds skill names, separated by spaces; none means every skill. A name with no `.claude/skills/<name>/SKILL.md` is a finding of its own ("no such skill"): report it and carry on with the rest.

## Steps

Run everything from the repository root.

1. Run the layout check:

   ```bash
   python3 -I scripts/agents/check-layout.py skills
   ```

   It prints `ok`, or one line per problem with a folder name, the `SKILL.md` file name or the front matter's `name` and `description`. Each line is a **must fix**.
2. Read [checks.md](checks.md). Then read each skill in full, with its supporting files, and go through every check there. The script sees only the layout; the rest is judgement.
3. Read the rules in `.claude/rules/` and the other skills in `.claude/skills/` too, for check 5 in [checks.md](checks.md): a skill must not tell Claude to do what a rule or another skill forbids.
4. Report, in the form below.
5. When I say which findings to fix, fix those:
   - rename a folder with `git mv`, so git keeps its history;
   - fix front matter and text in place;
   - move a section into a file beside `SKILL.md` and leave a line in `SKILL.md` saying when to read it;
   - when a skill's name changes, update everything that names it (`grep -rn '<old-name>' .claude AGENTS.md CONTRIBUTING.md docs`) and the `[Unreleased]` entry in `CHANGELOG.md` if it names the skill. Leave released `CHANGELOG.md` sections alone.
6. Run step 1 again: it must print `ok`. If anything changed, add an entry to `CHANGELOG.md` under `[Unreleased]`, then ask me before committing.

## Report

No preamble: the report only.

```text
Skills reviewed: <count> (<names>)
Layout check: ok | <count> problems

### <skill-name> (.claude/skills/<skill-name>/SKILL.md, <lines> lines)

Must fix
1. Line <n>: <what is wrong>. Fix: <the change>.

Should fix
1. ...

Consider
1. ...

Nothing to fix: <names of skills with no findings>
Totals: <n> must fix, <n> should fix, <n> to consider
```

Leave out a heading with nothing under it, and give a skill a block only if it has a finding. A name with no skill gets a block of its own, with one must fix: `no such skill: .claude/skills/<name>/SKILL.md`.
