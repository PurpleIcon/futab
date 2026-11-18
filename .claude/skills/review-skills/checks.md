# Checks for a skill

What the `review-skills` skill looks at in each skill, and how serious each problem is:

- **must fix**: the skill is broken, or won't be found or used;
- **should fix**: it works, but misleads, wastes context or will break;
- **consider**: worth improving.

Give the line number with every finding that has one, and the change that fixes it.

## 1. Name and place

`scripts/agents/check-layout.py skills` checks most of this; the rest is yours.

```text
.claude/skills/<skill-name>/SKILL.md
```

- `<skill-name>` is kebab-case: lower-case letters, digits and hyphens, 1 to 64 characters. The script checks this. Also **must fix**: a name that starts or ends with a hyphen, holds `--`, or holds `claude` or `anthropic` (reserved words).
- The file is named exactly `SKILL.md`. Nothing else sits directly in `.claude/skills/`. Both checked by the script.
- Supporting files (more instructions, reference tables, scripts) sit beside `SKILL.md` in the skill's folder.

## 2. Front matter

- It parses as YAML. A value holding `: ` (a colon and a space) needs double quotes, or YAML reads a new key and the front matter breaks: **must fix**.
- `name` is exactly the folder's name (checked by the script).
- `description` is non-empty (checked by the script), at most 1024 characters, with no `<...>` tags: **must fix** otherwise.
- `description` says what the skill does **and** when to use it, in words a user would type ("merge upstream", "build a test rpm"). No "when": **must fix**, as Claude can't tell when to pick it. Vague or no trigger words: **should fix**.
- `description` is in the third person ("Builds ...", not "Build ..." or "I build"): **consider**.
- Other keys Claude Code reads may follow: `argument-hint`, `allowed-tools`, `model`, `disable-model-invocation`, `user-invocable`. A key you don't recognise: **consider**, and ask whether it is a typo.
- The body uses `$ARGUMENTS` but there is no `argument-hint`: **consider**.

## 3. What it points at

Check every path: in links, in inline code, in commands.

- An absolute or home path (`/home/...`, `~/...`, `C:\...`): **must fix**. It only works on one machine.
- A file the skill needs that doesn't exist: **must fix**. Not a finding: a file the skill says to create, or one it says is gone on purpose.
- The skill's own supporting files are named from its folder (`checks.md`), not from the repository root (`.claude/skills/<name>/checks.md`): **should fix** otherwise.
- Project files (`scripts/...`, `docs/...`, `CHANGELOG.md`, `.claude/rules/<rule-name>/RULE.md`) are named from the repository root. That is right.
- Another skill is named by its name ("the `upstream-report` skill"), never by a path into its folder: **should fix** otherwise. A path breaks when that skill is reorganised.
- A path outside the repository (`../...`): **must fix**. FuTab's skills and rules name nothing outside the repository; whatever they need must be in it.

## 4. What it loads

The whole `SKILL.md` is read every time the skill runs; a supporting file only when `SKILL.md` says to read it.

- Report the line count. Over 500 lines: **consider**, naming what could move out. Length alone is never more than that: a long skill that needs all of it every time is fine.
- **should fix**, with what to move, when it should be read, and a file name for it:
  - a section needed only in some runs (one argument, one error, a follow-up the user may never ask for);
  - a large table or reference list needed only in some runs;
  - two jobs that share no steps: split into two skills, or one skill with a file per job.

## 5. How it reads

- The body gives steps to follow, or reference to look things up in, not a restatement of the description: **should fix** otherwise.
- It agrees with the rules in `.claude/rules/`. For example: tests only when asked; build and lint as the checks; never run the app; ask before committing; `git commit -s`; no `#N` for an upstream number in anything that reaches GitHub; no polling. A step that contradicts a rule, or another skill: **should fix**, quoting both.
- One idea, one word (not "front matter" here and "header" there for the same thing): **consider**.
- A command, flag or Claude Code feature that is deprecated or gone: **should fix**, with its replacement. Only when you are sure.
