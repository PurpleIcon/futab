---
name: review-rules
description: "Reviews FuTab's agent rules (`.claude/rules/`): their layout and names, front matter, the files they point at, how much they cost every session, whether they agree with each other and with the skills, and whether AGENTS.md lists them all. Reports what is wrong, most serious first, and fixes it once the user says so. Use whenever the task is to review, check, lint or tidy the rules, or after adding, renaming or editing one."
argument-hint: "[rule-name ...]"
---

# Review the rules

A rule is a standing directive. Claude Code loads every `.md` file under `.claude/rules/`, subfolders included, in full, in every session in this repository. So every line of a rule costs every session, and a rule that contradicts another leaves Claude to guess. This skill checks FuTab's rules against that, and against the layout FuTab keeps.

It reads and reports. **Change nothing until I say so.**

## Which rules

`$ARGUMENTS` holds rule names, separated by spaces; none means every rule. A name with no `.claude/rules/<name>/RULE.md` is a finding of its own ("no such rule"): report it and carry on with the rest.

Steps 3 and 4 cover every rule, whatever was named.

## Steps

Run everything from the repository root.

1. Run the layout check:

   ```bash
   python3 -I scripts/agents/check-layout.py rules
   ```

   It prints `ok`, or one line per problem with a folder name, the `RULE.md` file name or the front matter's `name` and `description`. Each line is a **must fix**.
2. Read [checks.md](checks.md). Then read each rule in full and go through every check there. The script sees only the layout; the rest is judgement.
3. Read all the rules together, and the skills in `.claude/skills/`, for check 5 in [checks.md](checks.md): rules that contradict each other or a skill.
4. Check `AGENTS.md` lists every rule's path with a line on what it covers, for agents other than Claude Code. A rule missing there, or listed there but gone: **should fix**. A line that no longer matches what the rule covers: **consider**.
5. Report, in the form below.
6. When I say which findings to fix, fix those:
   - move or rename with `git mv`, so git keeps the history;
   - fix front matter and text in place;
   - when a rule's path changes, update everything that names it (`grep -rn 'rules/<old>' .claude AGENTS.md CONTRIBUTING.md docs`) and the `[Unreleased]` entry in `CHANGELOG.md` if it names the path. Leave released `CHANGELOG.md` sections alone.
7. Run step 1 again: it must print `ok`. If anything changed, add an entry to `CHANGELOG.md` under `[Unreleased]`, then ask me before committing.

## Report

No preamble: the report only.

```text
Rules reviewed: <count> (<names>)
Layout check: ok | <count> problems

### <rule-name> (.claude/rules/<rule-name>/RULE.md, <lines> lines)

Must fix
1. Line <n>: <what is wrong>. Fix: <the change>.

Should fix
1. ...

Consider
1. ...

### AGENTS.md

<findings, or "all listed">

Nothing to fix: <names of rules with no findings>
Totals: <n> must fix, <n> should fix, <n> to consider
```

Leave out a heading with nothing under it, and give a rule a block only if it has a finding. A contradiction between two rules goes under the first of them, naming the other. A name with no rule gets a block of its own, with one must fix: `no such rule: .claude/rules/<name>/RULE.md`.
