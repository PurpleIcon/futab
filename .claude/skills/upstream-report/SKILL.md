---
name: upstream-report
description: Update the upstream catch-up report, `oxiguitar-catchup.md`, by running `scripts/upstream/catchup.py`, and summarise what upstream OxiGuitar (mateusrdp/oxiguitar) has that FuTab hasn't merged yet. Use whenever the task is to see, check, list or refresh what's new upstream, what FuTab is behind on, or which files a merge from upstream would conflict in, without merging anything.
argument-hint: "[--ours REF] [--theirs REF] [--no-fetch]"
---

# Update the upstream catch-up report

`scripts/upstream/catchup.py` compares FuTab with upstream OxiGuitar by git ancestry (`ours..theirs`) and writes `oxiguitar-catchup.md` at the repository's root: the upstream releases and commits FuTab hasn't merged, each with its pull request, and the files a merge would conflict in. It merges nothing and changes no file in the repository; the only things it touches are the `upstream` remote (added if missing, then fetched) and `refs/upstream-tags/` (upstream's tags, kept apart from FuTab's).

This skill only reports. To merge, use `merge-upstream` (`.claude/skills/merge-upstream/SKILL.md`), which runs this report before and after a merge.

## 1. Run it

Arguments: `$ARGUMENTS` (passed to the script as they are).

| Option | Meaning |
| --- | --- |
| (none) | fetch upstream, compare `upstream/develop` with the checked-out branch (`HEAD`) |
| `--ours REF` | FuTab's side, e.g. `origin/develop` to see what `develop` on GitHub lacks rather than the current branch |
| `--theirs REF` | upstream's side (default `upstream/develop`), e.g. an upstream commit or `refs/upstream-tags/v0.19.2` |
| `--no-fetch` | use what is fetched already (offline, or to repeat a run quickly) |
| `-o PATH` | write elsewhere; `-o -` prints to stdout. Don't use it for this skill: its job is to update `oxiguitar-catchup.md` |

From `futab/`:

```bash
python3 -I scripts/upstream/catchup.py
```

When I haven't said which side to compare, and the checked-out branch isn't `develop` or a merge branch (`feat/merge-oxiguitar-*`), say which branch the report is against: a feature branch made from an older `develop` shows more missing than `develop` does. Offer `--ours origin/develop` (after `git fetch origin develop`) if that's what I probably meant.

If the script stops with a git error (no network, no `upstream` access), show me the error and stop; don't work around it.

## 2. Read it and tell me

Read `oxiguitar-catchup.md` and tell me, short:

- what it was compared against (`ours` and its commit, `theirs` and its commit) and the last common commit;
- how many commits are missing, and the upstream releases among them;
- the missing PRs in merge order (`#N` and title, one line each), with release or non-PR commits named where they fall;
- the files a merge would conflict in, apart from `CHANGELOG.md` (always conflicts, always ours), and which PRs cause them;
- anything that looks wrong (see below).

Don't paste the whole file; it's gitignored and stays local, I can open it.

## 3. Checks

- **A PR already merged is listed as missing:** FuTab's ancestry broke: a merge PR was squashed or rebased, or an upstream commit was cherry-picked. Say which PR and stop; `merge-upstream`'s "If a merge PR was squashed" puts it right.
- **A PR skipped on purpose** (merged and reverted) must not be listed. If it is, same as above.
- **"Unknown" conflicts:** git is older than 2.38. Say so; the rest of the report still holds.

## When is the report up to date?

Never by itself. The file is only rewritten when the script runs, and each run compares `upstream/develop` with the branch checked out at that moment (`HEAD`), unless `--ours` says otherwise. So:

- **While a merge is in progress (not committed yet):** the file still lists the PRs being merged, because `HEAD` hasn't moved. That's expected, not a fault.
- **After the merge commit on the merge branch:** running the script drops the merged and skipped PRs; the rest is what FuTab hasn't taken yet.
- **On GitHub:** the Upstream workflow (`.github/workflows/upstream.yml`) runs the same script against `develop` every Monday, and by hand with "Run workflow" on the Actions tab. Its report is the run's summary and an artifact, not this file.
- **The one thing that makes it wrong:** squash-merging (or rebasing) a merge PR. That throws away upstream's ancestry, so every merged PR shows up as missing again. Hence "Create a merge commit" for merge PRs, always.

The file is gitignored (`/oxiguitar-catchup.md` in `.gitignore`), so it never shows up in commits or PRs; each person or run makes their own. Never commit it.

## Keeping this skill current

If the script gains options or its report changes shape, update this skill with it, and ask me before changing the script itself.
