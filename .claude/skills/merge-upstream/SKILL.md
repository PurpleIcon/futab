---
name: merge-upstream
description: Merge upstream OxiGuitar (mateusrdp/oxiguitar, the `upstream` remote) into FuTab while keeping FuTab's names. Use whenever the task is to catch up with, sync from, pull in or merge OxiGuitar or upstream changes, or to resolve conflicts from such a merge.
---

# Merge upstream OxiGuitar into FuTab

FuTab is OxiGuitar renamed, plus FuTab's own changes. Upstream keeps moving, and every change it makes lands on files FuTab renamed. This skill takes upstream's **changes** and keeps FuTab's **names**.

**Main rule:** in a clash that is only about the name, FuTab wins. In a clash about behaviour, upstream's behaviour wins, written with FuTab's names. If you can't tell which kind of clash it is, ask; don't guess.

## 1. Before merging

1. Check the work tree is clean (`git status`) and that you're on a branch made from up-to-date `origin/develop`, named `feat/merge-oxiguitar-<version>` (or `-<short sha>` when the merge doesn't reach an upstream release).
2. Run `python3 -I scripts/upstream/catchup.py` and read `oxiguitar-catchup.md`: the upstream PRs coming in, the releases, and the files that will conflict. Tell me what's coming, in a few lines, before you start.
3. Merge without committing, so the checks in step 3 below also cover lines that merged cleanly:

   ```bash
   git merge --no-ff --no-commit upstream/develop
   ```

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
| `OxiGuitar` (the app's name, in text people read: UI strings, messages, docs, manual, man pages, metainfo, README) | `FuTab` |
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

## 4. Changelog

Add the merge's entry under `## [Unreleased]` → `### Changed` in `CHANGELOG.md`, in the form `.claude/rules/github.md` gives ("Merged OxiGuitar x.y.z", one line per upstream PR in the user's words, `mateusrdp/oxiguitar#N`). Leave out what FuTab dropped, and upstream's release and changelog commits.

## 5. Report and hand over

Tell me, short:

- the upstream PRs merged;
- every conflict and how it was settled ("name only, kept ours", "upstream's change, FuTab's names", "both kept");
- every name you left as OxiGuitar on purpose, if it's not obvious from the lists;
- what you need me to decide.

Then stop. Commit only when I say so (`git commit -s`, the merge's own message is fine). In the PR, say that it **must be merged with "Create a merge commit", never squash or rebase**: squashing throws away upstream's ancestry, so the next merge would conflict all over again and the catch-up report would list everything again. After it lands, run the catch-up script again: those changes are gone from the report.

If you learn something in a merge that this skill should know (a new rename, a new file that keeps OxiGuitar's name), ask me whether to add it here.
