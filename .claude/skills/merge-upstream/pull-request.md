# The pull request and merging it

Read this when the user asks for the merge's PR, or asks you to merge it. Steps 1 to 6 are those of [SKILL.md](SKILL.md).

## The pull request

When I ask for the PR (push only when I say so):

- **Title:** `Merge FROM upstream OxiGuitar PR N`, where `N` is the last upstream PR the merge brings in (the target's PR, or the last PR before it when the target is a release or other commit without one). For example: `Merge FROM upstream OxiGuitar PR 290`. The capital FROM keeps the direction plain: FuTab takes OxiGuitar's changes, nothing goes back to OxiGuitar. Never a title that could read as merging into upstream (the old `Merge upstream to oxiguitar #N` did), and **never a `#` before the number**: FuTab has no PR of that number, so GitHub links OxiGuitar's, and the merge commit (whose message carries the title) posts on upstream's PR (Referring to upstream in `.claude/rules/github/RULE.md`). Nothing else in the title: no repository prefix, no list of PRs, no release number.
- **Description:** first, the warning to merge with "Create a merge commit", never squash or rebase, and why. Then the upstream PRs merged (as `OxiGuitar PR N`, never `mateusrdp/oxiguitar#N`, with what each changes and its merge commit), the skipped ones with reasons, what upstream still has, every conflict and how it was settled, the names changed and kept, behaviour changes users will notice, the checks run, and test steps.
- Branch, base and sign-off as in step 1 and `.claude/rules/github/RULE.md`.

## Merging the pull request

A merge PR must land as a merge commit. The merge button's choice is easy to get wrong (PR #7 was squashed by mistake), so when I ask you to merge it, do it yourself:

1. Check every check on the PR's head has passed, and say which haven't if any:

   ```bash
   gh pr view <n> --json headRefOid,statusCheckRollup
   ```

   Nothing tells you when CI finishes, and you don't poll it: if checks are still running, say so and wait for me to tell you it's green.
2. Merge it with a merge commit:

   ```bash
   gh pr merge <n> --merge
   ```

   If the branch rules block it only for want of a review (I can't approve my own PRs), add `--admin` once I've said to merge: that's how I merge them. Never `--squash` or `--rebase`, whatever the repository's default. If the admin merge is refused (the session's permission check may block it), don't work around it: ask me to merge it on GitHub, saying plainly: **"Merge #N with Create a merge commit, not Squash and merge: it carries upstream's history."**
3. Check the result: the commit `develop` now points at has **two** parents (`git log -1 --format=%p origin/develop` after `git fetch origin develop`), and the catch-up report against `origin/develop` (`--ours origin/develop`) no longer lists the merged PRs. If either is wrong, follow [squashed-merge.md](squashed-merge.md).
