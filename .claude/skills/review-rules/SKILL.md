---
name: review-rules
description: Review FuTab's agent rules (`.claude/rules/`) against the naming and layout rules (a kebab-case folder per rule, a file named exactly RULE.md, YAML front matter whose name matches the folder, and a description), report every problem, and fix them once the user says so. Use whenever the task is to review, check, lint or tidy the rules, or after adding or renaming one.
---

# Review the rules

FuTab's agent rules live in `.claude/rules/`. Claude Code loads every `.md` file there, subfolders included, in every session in this repository. This skill checks they all follow the layout below, reports what doesn't, and fixes it only when I say so.

## The layout

```text
.claude/rules/<rule-name>/RULE.md
```

- **Folder:** one per rule, named `<rule-name>` in kebab-case: lower-case letters, digits and hyphens only, at most 64 characters (`general`, `github`, `tags`). Nothing else sits directly in `.claude/rules/`: no loose `.md` files.
- **File:** named exactly `RULE.md` (case-sensitive: not `rule.md` or `Rule.md`). Each `.md` file in the folder is loaded as a rule, so keep anything else out of it.
- **Front matter:** the file opens with YAML front matter between two `---` lines, with:
  - `name`: exactly the folder's name;
  - `description`: what the rule covers, in one sentence.

  Put the description in double quotes when it holds a colon followed by a space (`: `), or YAML reads it as a new key and the front matter breaks.

  ```yaml
  ---
  name: tags
  description: How FuTab's release tags are made and pushed, how they are protected, and what is never done with tags.
  ---
  ```

## Steps

1. Run the check from the repository's root:

   ```bash
   python3 -I scripts/agents/check-layout.py rules
   ```

   It prints one line per problem, or `ok`.
2. Read each `RULE.md`'s `description` too: the script checks it exists, not that it matches what the rule covers. Note any that don't.
3. Check the workspace notes import every rule: `../CLAUDE.md` (the workspace's, outside the repository) has a line `@futab/.claude/rules/<rule-name>/RULE.md` for each, so sessions started in the workspace load them too. Note any rule missing there, or imported there but gone.
4. Report: each problem with its file, and the fix you propose (for example "move `.claude/rules/tags.md` to `.claude/rules/tags/RULE.md` and add front matter `name: tags`"). If there is none, say so in one line.
5. **Change nothing until I say so.** Then make the fixes:
   - move or rename with `git mv`, so git keeps the history;
   - fix or add the front matter in place;
   - when a rule's path changes, update everything that names it: skills and other rules (`grep -rn 'rules/<old>' .claude AGENTS.md CONTRIBUTING.md docs`), the workspace `../CLAUDE.md`'s imports, and the `[Unreleased]` entry in `CHANGELOG.md` if it names the path. Leave released `CHANGELOG.md` sections as they are.
6. Run the check again: it must print `ok`. Then add an entry to `CHANGELOG.md` under `[Unreleased]` if anything changed, and ask me before committing.
