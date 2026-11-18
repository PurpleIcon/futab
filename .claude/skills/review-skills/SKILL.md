---
name: review-skills
description: Review FuTab's agent skills (`.claude/skills/`) against the naming and layout rules (a kebab-case folder per skill, a file named exactly SKILL.md, YAML front matter whose name matches the folder, and a description), report every problem, and fix them once the user says so. Use whenever the task is to review, check, lint or tidy the skills, or after adding or renaming one.
---

# Review the skills

FuTab's skills live in `.claude/skills/`. This skill checks they all follow the layout below, reports what doesn't, and fixes it only when I say so.

## The layout

```text
.claude/skills/<skill-name>/SKILL.md
```

- **Folder:** one per skill, named `<skill-name>` in kebab-case: lower-case letters, digits and hyphens only, at most 64 characters (`build-test-rpm`, `merge-upstream`). Nothing else sits directly in `.claude/skills/`.
- **File:** named exactly `SKILL.md` (case-sensitive: not `skill.md` or `Skill.md`). Supporting files may sit beside it in the folder.
- **Front matter:** the file opens with YAML front matter between two `---` lines, with:
  - `name`: exactly the folder's name;
  - `description`: what the skill does and when to use it, in one paragraph (Claude Code reads it to decide when the skill applies).

  Other keys Claude Code knows (such as `argument-hint`) may follow.

  Put the description in double quotes when it holds a colon followed by a space (`: `), or YAML reads it as a new key and the front matter breaks.

  ```yaml
  ---
  name: build-test-rpm
  description: Build a test .rpm of FuTab from the working copy ... Use whenever the task is to ...
  ---
  ```

## Steps

1. Run the check from the repository's root:

   ```bash
   python3 -I scripts/agents/check-layout.py skills
   ```

   It prints one line per problem, or `ok`.
2. Read each `SKILL.md`'s `description` too: the script checks it exists, not that it says what the skill does and when to use it. Note any that don't.
3. Check the workspace notes list every skill: `../CLAUDE.md` (the workspace's, outside the repository) names each one under "Skills" with its path and a line on what it does. Note any skill missing there, or listed there but gone.
4. Report: each problem with its file, and the fix you propose (for example "rename `.claude/skills/Build_RPM/` to `build-rpm`, and set `name: build-rpm`"). If there is none, say so in one line.
5. **Change nothing until I say so.** Then make the fixes:
   - rename a folder with `git mv`, so git keeps its history;
   - fix the front matter in place;
   - when a skill's name changes, update everything that names it: other skills and rules (`grep -rn '<old-name>' .claude AGENTS.md CONTRIBUTING.md docs`), the workspace `../CLAUDE.md`, and the `[Unreleased]` entry in `CHANGELOG.md` if it names the skill. Leave released `CHANGELOG.md` sections as they are.
6. Run the check again: it must print `ok`. Then add an entry to `CHANGELOG.md` under `[Unreleased]` if anything changed, and ask me before committing.
