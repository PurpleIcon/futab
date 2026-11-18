# Checks for a rule

What the `review-rules` skill looks at in each rule, and how serious each problem is:

- **must fix**: the rule is broken, or isn't loaded as meant;
- **should fix**: it works, but misleads, contradicts or wastes context;
- **consider**: worth improving.

Give the line number with every finding that has one, and the change that fixes it.

## 1. Name and place

`scripts/agents/check-layout.py rules` checks most of this; the rest is yours.

```text
.claude/rules/<rule-name>/RULE.md
```

- `<rule-name>` is kebab-case: lower-case letters, digits and hyphens, 1 to 64 characters (checked by the script). Also **must fix**: a name that starts or ends with a hyphen, or holds `--`.
- The file is named exactly `RULE.md`. Nothing else sits directly in `.claude/rules/`: no loose `.md` files. Both checked by the script.
- Any other `.md` file in a rule's folder is loaded as a rule too: **should fix**. Keep notes and examples out of `.claude/rules/`, in `docs/futab-design/` for example.

## 2. Front matter

- It parses as YAML. A value holding `: ` (a colon and a space) needs double quotes, or YAML reads a new key and the front matter breaks: **must fix**.
- `name` is exactly the folder's name, and `description` is non-empty (checked by the script). These two are FuTab's convention, for people and for the review; Claude Code doesn't read them.
- `description` says what the rule covers, in one sentence, and matches what the rule says now: **consider** otherwise.
- `paths:` (glob patterns) is the one key Claude Code reads: the rule then loads only when Claude works on matching files. A rule with `paths:` that a `CLAUDE.md` also imports with `@` loads every time anyway, as imports always load: **should fix**.
- Keys from other tools (Cursor's `globs`, `alwaysApply`) do nothing here: **should fix**.
- Any other key you don't recognise: **consider**, and ask whether it is a typo.

## 3. What it points at

Check every path: in links, in inline code, in commands.

- An absolute or home path (`/home/...`, `~/...`, `C:\...`): **must fix**. It only works on one machine.
- A file the rule needs that doesn't exist: **must fix**. Not a finding: a file the rule says to create, or one it says is gone on purpose.
- Files are named from the repository root (`scripts/check-dco.sh`, `CHANGELOG.md`). A rule may name a skill's `SKILL.md` by its path: a rule has no supporting files, so that is how it points at a procedure.
- A path outside the repository (`../...`): **must fix**. FuTab's skills and rules name nothing outside the repository; whatever they need must be in it.

## 4. What it costs

Every rule is read in full at the start of every session.

- Report the line count. Over 100 lines: **consider**, naming what could go.
- A step-by-step procedure for one task (a release, a merge, a fix): **should fix**. It belongs in a skill, read only for that task; the rule keeps the one-line directive and names the skill.
- A long list or table needed only now and then (repositories, plugins, ids): **consider** moving it to `docs/` and pointing at it.
- The same directive in two rules: **consider** keeping it in one.

## 5. Does it agree

- Two rules that contradict each other, or a rule and a skill (one says `git checkout --ours`, the other says that does nothing), or a rule and `AGENTS.md`: **should fix**, quoting both and saying which looks right.
- A directive that can't be followed as written (it asks for polling where the project forbids it, or names a tool or step that doesn't exist): **should fix**.

## 6. How it reads

- Each directive is one clear instruction that can be followed or checked: **consider** rewording one that can't.
- One idea, one word: **consider**.
- A command, flag or Claude Code feature that is deprecated or gone: **should fix**, with its replacement. Only when you are sure.
