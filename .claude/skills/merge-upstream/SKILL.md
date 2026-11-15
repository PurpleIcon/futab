---
name: merge-upstream
description: Merge upstream OxiGuitar (mateusrdp/oxiguitar, the `upstream` remote) into FuTab while keeping FuTab's names, all of it or up to a given upstream PR, optionally skipping PRs. Use whenever the task is to catch up with, sync from, pull in or merge OxiGuitar or upstream changes or PRs, or to resolve conflicts from such a merge.
argument-hint: "[#N | #A-#B] [skip #X[,#Y]]"
---

# Merge upstream OxiGuitar into FuTab

FuTab is OxiGuitar renamed, plus FuTab's own changes. Upstream keeps moving, and every change it makes lands on files FuTab renamed. This skill takes upstream's **changes** and keeps FuTab's **names**.

**Main rule:** in a clash that is only about the name, FuTab wins. In a clash about behaviour, upstream's behaviour wins, written with FuTab's names. If you can't tell which kind of clash it is, ask; don't guess.

## 0. What to merge

Arguments: `$ARGUMENTS`

| Arguments | Merges |
| --- | --- |
| (none) | all of `upstream/develop` |
| `#N` | upstream up to and including PR #N |
| `#A-#B` | the PRs from #A to #B, **in the order upstream merged them** (not by number: #270 was merged after #286) |
| `... skip #X` or `skip #X,#Y` | the same, then reverts #X (and #Y) in commits of their own after the merge: see "Skipping a PR" |

Git merges a commit together with everything before it, so a merge can only stop at a point in upstream's history; it can't pick PRs out of the middle. So:

1. Fetch, then list what's missing, in merge order: the catch-up report's "Missing changes" table, or

   ```bash
   git log --reverse --no-merges --format='%h %s' HEAD..upstream/develop
   ```

   (Not `--first-parent`: upstream's `develop` tip sits on a merge from `main`, so first-parent skips most of its PRs.)
2. Find each PR's squash commit: the missing commit whose subject **ends** in `(#N)` (earlier numbers in the subject are issues). If a PR isn't there, say whether it's already in FuTab (`git log --format='%h %s' upstream/develop | grep -E '\(#N\)$'` finds it, and `git merge-base --is-ancestor <sha> HEAD` succeeds) or not in upstream's `develop` at all, and stop.
3. The **target** is the commit of `#N`, or of `#B` for a range. Everything missing up to the target comes in.
4. `#N` alone, or a range's `#A`, should be the **first** missing PR. If it isn't, the missing PRs before it come in too, so list them and ask me: take them as well, skip them, or stop. If `#B` comes before `#A` in merge order, say so and stop.
5. Show me the resolved list (PR, title, commit, and any release or non-PR commits such as "Release 0.19.2" in between) and wait for my go-ahead before merging.

## 1. Before merging

1. Check the work tree is clean (`git status`) and that you're on a branch made from up-to-date `origin/develop`, named `feat/merge-oxiguitar-<version>` when the target is an upstream release, else `feat/merge-oxiguitar-pr<N>` for one PR or `feat/merge-oxiguitar-pr<A>-<B>` for a range.
2. Run `python3 -I scripts/upstream/catchup.py` and read `oxiguitar-catchup.md`: the upstream PRs coming in, the releases, and the files that will conflict. Tell me what's coming, in a few lines, before you start.
3. Merge without committing, so the checks in step 3 below also cover lines that merged cleanly:

   ```bash
   git merge --no-ff --no-commit <target>
   ```

   `<target>` is `upstream/develop` when merging everything, else the commit from step 0.

   Never cherry-pick or rebase upstream commits. FuTab tracks upstream by git ancestry: a copy of a commit keeps it on the catch-up list forever, and the next merge conflicts again.

## 2. Resolving conflicts

Go conflict by conflict (`git diff --name-only --diff-filter=U`). For each hunk, decide which kind it is:

- **Name only:** ours and theirs differ only in a name from the table below. Keep ours.
- **Behaviour, with names in it:** upstream changed code, text or config, and the text it touched has FuTab's names on our side. Take upstream's version, then put every name back to FuTab's using the table. Check the result line by line against both sides: nothing of upstream's change dropped, no OxiGuitar name brought back.
- **Both changed behaviour:** FuTab changed the same lines for a reason of its own (for example the hidden MIDI advice in `crates/oxiguitar-host/src/advice.rs`). Keep both if they combine; if they don't, stop and ask me, quoting both sides.

Files:

- `CHANGELOG.md`: always keep ours (`git checkout --ours CHANGELOG.md`). FuTab's changelog lists FuTab's changes only; the merge gets its own entry (step 4).
- A file FuTab renamed (desktop entry, metainfo, mime XML, man pages, `debian/*.manpages`, `scripts/package/oxiguitar-start`, icons): upstream's changes go into **FuTab's** file. If git reports modify/delete or leaves upstream's old-named file behind, apply upstream's change to FuTab's file and `git rm` the old name.
- A file FuTab deleted on purpose (`scripts/new-repo.sh`, `scripts/split-history.sh`, the PayPal button and QR code, the placeholder icon): keep it deleted. If upstream changed it, tell me in one line.
- A file upstream added: keep it. If its name or contents carry OxiGuitar names that the table renames, rename them. For example, upstream's new `FUNDING.yml` points at OxiGuitar's donations: ask me whether FuTab keeps it.
- Version numbers (`Cargo.toml`, `Cargo.lock`, `debian/changelog`, metainfo `<release>`): FuTab has its own version. Keep FuTab's version and FuTab's `debian/changelog` entries, and take only upstream's dependency changes in `Cargo.lock`. If `Cargo.lock` doesn't settle cleanly, take theirs and then run `cargo build` so Cargo writes FuTab's own entries back. If upstream's release is a good point for a FuTab release too, say so; don't bump anything yourself.

## The name table

What FuTab renamed: always FuTab's side in a merge.

| OxiGuitar (upstream) | FuTab |
| --- | --- |
| `OxiGuitar` (the app's name, in text users read: UI strings, messages, the user manual `docs/manual/`, the plugin guide `docs/plugins/`, man pages, metainfo, README) | `FuTab` |
| package and binary `oxiguitar`, `oxiguitar-x11`, `oxiguitar-cli` (`cargo run -p ...`, `target/.../oxiguitar*`, `/usr/bin/...`, `/app/bin/...`, `oxiguitar.exe`) | `futab`, `futab-x11`, `futab-cli`, `futab.exe` |
| app ID `io.github.mateusrdp.OxiGuitar` (and file names that use it) | `io.github.purpleicon.FuTab` |
| repository `mateusrdp/oxiguitar` as **this** project's home: `repository`/`homepage`, bug reports, issues, discussions, screenshots | `PurpleIcon/futab` |
| settings, data and cache folders `oxiguitar` / `OxiGuitar` | `futab` / `FuTab` |
| FuTab's own plugin folders: `lib/oxiguitar/plugins`, `~/.local/share/oxiguitar/plugins`, `Application Support/OxiGuitar/plugins` (searched first) | `lib/futab/plugins`, `~/.local/share/futab/plugins`, `Application Support/FuTab/plugins` |
| release files `OxiGuitar-…AppImage`, `…flatpak`, `…windows-….zip`, `…macos-universal.dmg`; `dist/OxiGuitar-…` | `FuTab-…` |
| launcher `oxiguitar-start`, man pages `oxiguitar.1`, `oxiguitar-cli.1` | `futab-start`, `futab.1`, `futab-cli.1` |
| icon `oxiguitar-*.png`, `oxiguitar-placeholder.svg` | `futab-*.png`, `futab.svg` |
| the core's advice dialog title / plugin name "OxiGuitar" (`Asked::core`) | "FuTab" |
| debian package `oxiguitar`, maintainer `OxiGuitar <maintainer@oxiguitar.invalid>` | `futab`, `FuTab <maintainer@futab.invalid>` |

What stays OxiGuitar's: never rename these, in a merge or anywhere else.

- **Credit and copyright:** SPDX headers (`Copyright (C) 2026 Mateus Rocha de Paula and the OxiGuitar contributors`), `authors` in manifests, CREDITS.md, the About box's credit to OxiGuitar, "a fork of OxiGuitar".
- **Code names:** crate folders (`crates/oxiguitar-*`), the library crates and their Rust names (`oxiguitar_plugin`, `oxiguitar_host`, ...), the `OXIGUITAR_*` environment variables (`OXIGUITAR_HOME`, ...).
- **Plugins** (OxiGuitar's, used as they are): plugin repo and package names (`oxiguitar-guitarpro`, `oxiguitar-midi`, ...), plugin ids (`oxiguitar.midi`, ...), the core's advice id `oxiguitar` (`advice::CORE`), `oxiguitar-set.json`, `.oxp` files, and the plugin SDK's git source `https://github.com/mateusrdp/oxiguitar` in plugin `Cargo.toml`s.
- **OxiGuitar's plugin folders as a fallback** (`/usr/lib/oxiguitar/plugins` and the others, searched after FuTab's), and `/usr/share/oxiguitar/soundfonts`.
- **File formats:** the `.oxg` sidecar and anything else written to a user's files. Renaming those would break files people already have.
- **Code comments and design records:** comments in the code (`//`, `///`, `//!`, `#`), `docs/design/` and `docs/adr/` keep OxiGuitar's name, and upstream's changes to them are taken as they are. They record OxiGuitar's design and decisions; renaming them would only make every later merge conflict. FuTab's own design notes and decisions go in `docs/futab-design/` and `docs/futab-adr/`, never into these.
- **Links to upstream as upstream:** the `upstream` remote, links to OxiGuitar's changelog, PRs and issues (`mateusrdp/oxiguitar#N`), the catch-up script.

When a name fits neither list, it's the clash you can't settle: list it with its file and line, and ask me.

## 3. Check that no old name came back

Once no conflicts are left, run these. They cover the lines that merged cleanly too:

```bash
git diff --cached HEAD -U0 | grep -nE '^\+.*(OxiGuitar|oxiguitar|mateusrdp|maintainer@oxiguitar)' | grep -v '^+++'
```

Go through every hit against the two lists: rename what the table renames, leave what stays OxiGuitar's, and ask about the rest. Then:

```bash
git diff --cached --name-only --diff-filter=A HEAD | grep -i oxiguitar
```

These are new files with OxiGuitar in their name; rename them by the table. Then do the build and lint checks (not the tests unless I ask):

```bash
cargo build
```

```bash
cargo fmt --all -- --check
```

```bash
cargo clippy --workspace --all-targets -- -D warnings
```

## Skipping a PR

A PR can be skipped, but **only by merging it and reverting it**, never by leaving it out. Leaving it out would mean cherry-picking around it, which loses the ancestry the catch-up report and every later merge depend on.

The revert is a commit of its own, after the merge commit and in the same branch and PR, so the history says plainly what FuTab turned down. Git can't revert while a merge is uncommitted, so ask me to approve both together. Once I say commit:

```bash
git commit -s
```

```bash
git revert -s --no-edit <sha of #X>
```

Then reword the revert's message to `Skip OxiGuitar's <title> (mateusrdp/oxiguitar#X)`, with the reason in its body. Settle any conflicts as in step 2, check names and build again (step 3), and name every skipped PR, with its reason, in the report and the PR description. Upstream's release commits and FuTab's own version are never handled by skipping: step 2's rules for version numbers cover them.

What skipping means (say this to me when I ask to skip, for that PR in particular):

- **Upstream counts it as merged.** The catch-up report won't list it again, and git won't offer it again. Getting it later takes a deliberate `git revert` of the revert, not another merge.
- **Later upstream PRs may build on it** (for example #289 builds on #270's Harmonize). Before skipping, check whether later missing PRs touch the same files or code (`git diff --stat <sha>^ <sha>`, compared with what later commits change). If they do, they'll conflict or not build once it's skipped. Say which ones, and skip them all or none.
- **The cost grows with every merge.** Each later upstream change to the code the revert removed conflicts again in every future merge. Skipping suits self-contained changes FuTab doesn't want (`FUNDING.yml`, OxiGuitar-only links or branding); for a feature FuTab doesn't want, hiding it behind a setting or a plugin is often cheaper over time than reverting it.
- **The changelog leaves it out**, and the PR description says why.

## 4. Changelog

Add the merge's entry under `## [Unreleased]` → `### Changed` in `CHANGELOG.md`, in the form `.claude/rules/github.md` gives ("Merged OxiGuitar x.y.z", or "Merged OxiGuitar up to mateusrdp/oxiguitar#N" when the target isn't a release; one line per upstream PR in the user's words, `mateusrdp/oxiguitar#N`). Leave out what FuTab dropped, and upstream's release and changelog commits.

## 5. Report and hand over

Tell me, short:

- the upstream PRs merged, and the ones skipped with their reasons;
- every conflict and how it was settled ("name only, kept ours", "upstream's change, FuTab's names", "both kept");
- every name you left as OxiGuitar on purpose, if it's not obvious from the lists;
- what you need me to decide.

Then stop. Commit only when I say so (`git commit -s`, the merge's own message is fine). In the PR, say that it **must be merged with "Create a merge commit", never squash or rebase**: squashing throws away upstream's ancestry, so the next merge would conflict all over again and the catch-up report would list everything again.

### The pull request

When I ask for the PR (push only when I say so):

- **Title:** `Merge upstream to oxiguitar #N`, where `#N` is the last upstream PR the merge brings in (the target's PR, or the last PR before it when the target is a release or other commit without one). For example: `Merge upstream to oxiguitar #290`. Nothing else in the title: no repository prefix, no list of PRs, no release number.
- **Description:** first, the warning to merge with "Create a merge commit", never squash or rebase, and why. Then the upstream PRs merged (as `mateusrdp/oxiguitar#N`, with what each changes and its merge commit), the skipped ones with reasons, what upstream still has, every conflict and how it was settled, the names changed and kept, behaviour changes users will notice, the checks run, and test steps.
- Branch, base and sign-off as in step 1 and `.claude/rules/github.md`.

### Merging the pull request

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

   If the branch rules block it only for want of a review (I can't approve my own PRs), add `--admin` once I've said to merge: that's how I merge them. Never `--squash` or `--rebase`, whatever the repository's default.
3. Check the result: the commit `develop` now points at has **two** parents (`git log -1 --format=%p origin/develop` after `git fetch origin develop`), and the catch-up report against `origin/develop` (`--ours origin/develop`) no longer lists the merged PRs. If either is wrong, go to "If a merge PR was squashed".

### If a merge PR was squashed

You can tell: the PR's commit on `develop` has one parent, and the catch-up report against `develop` lists the PRs it merged as missing again. The code is all there, only upstream's history is gone, but the next merge from upstream would conflict on all of it again. Restore the history with a merge that changes no file:

1. Check that `develop` really has the merged content: the squash commit's tree must equal the merge branch's last commit's tree.

   ```bash
   test "$(git rev-parse <squash commit>^{tree})" = "$(git rev-parse <merge branch tip>^{tree})" && echo same
   ```

   If they differ, stop and tell me what differs: `-s ours` would record upstream's commits as merged while some of their changes are missing.
2. On a branch from up-to-date `origin/develop` named `fix/oxiguitar-history-pr<N>`, record upstream's target commit as merged, keeping `develop`'s files:

   ```bash
   git merge -s ours --no-ff --signoff <upstream target commit>
   ```

   with a message saying which PR was squashed and that the merge changes no file.
3. Check: `git diff origin/develop HEAD` is empty, and the catch-up report on the branch shows the target as the last common commit.
4. Add a changelog entry under `### Fixed` ("Upstream history up to mateusrdp/oxiguitar#N", why it was missing, and that the merge changes no file) as a commit of its own.
5. With my go-ahead, push and open the PR titled `Restore upstream history up to oxiguitar #N`, its description opening with the merge-commit warning, and merge it as above, with `--merge`.

## 6. Update the catch-up report

Straight after the merge commit, and after any skip reverts, run the report again on the merge branch:

```bash
python3 -I scripts/upstream/catchup.py
```

Check it against what was merged:

- every merged PR is gone from "Missing changes", and so is every skipped one (merged, then reverted);
- what's left is upstream's PRs after the target, in merge order;
- "Merging now would conflict in" now describes the *next* merge.

Then tell me in one line what upstream still has that FuTab doesn't (count, and the next PR or two). If a merged PR is still listed, something broke the ancestry (a cherry-pick, a rebase, or a merge of the wrong commit): stop and tell me.

### When is `oxiguitar-catchup.md` up to date?

Never by itself. The file is only rewritten when the script runs, and each run compares `upstream/develop` with the branch that is checked out at that moment (`HEAD`). So:

- **While the merge is in progress (not committed yet):** the file still lists the PRs being merged, because `HEAD` hasn't moved. That's expected, not a fault.
- **After the merge commit on the merge branch:** running the script (this step) drops the merged and skipped PRs; the rest is what FuTab hasn't taken yet.
- **On GitHub:** the Upstream workflow (`.github/workflows/upstream.yml`) checks `develop`. It shows the new state once the merge PR has landed on `develop`, at its next Monday run or straight away with "Run workflow" on the Actions tab.
- **The one thing that makes it wrong:** squash-merging (or rebasing) the merge PR. That throws away upstream's ancestry, so every merged PR shows up as missing again, and the next merge conflicts on all of them. Hence "Create a merge commit" for these PRs, always. If it happens anyway, "If a merge PR was squashed" above puts it right.

The file is gitignored, so it never shows up in commits or PRs; each person or run makes their own.

## Keeping this skill current

If you learn something in a merge that this skill should know (a new rename, a new file that keeps OxiGuitar's name), ask me whether to add it here.
