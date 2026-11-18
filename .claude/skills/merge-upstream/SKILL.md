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
2. Update the catch-up report as the `upstream-report` skill says (`python3 -I scripts/upstream/catchup.py`) and read `oxiguitar-catchup.md`: the upstream PRs coming in, the releases, and the files that will conflict. Tell me what's coming, in a few lines, before you start.
3. Merge without committing, so the checks in step 3 below also cover lines that merged cleanly:

   ```bash
   git -c merge.conflictStyle=zdiff3 merge --no-ff --no-commit <target>
   ```

   `zdiff3` shows the common ancestor in each conflict (the `|||||||` part), so you can see which side changed which line.

   `<target>` is `upstream/develop` when merging everything, else the commit from step 0.

   Never cherry-pick or rebase upstream commits. FuTab tracks upstream by git ancestry: a copy of a commit keeps it on the catch-up list forever, and the next merge conflicts again.

   Never bring OxiGuitar's tags into FuTab: FuTab's `v*` tags are its own releases (from 0.1.0), and a pushed `v*` tag starts FuTab's release workflow. Fetch upstream without tags (`git fetch --no-tags upstream`, or once `git config remote.upstream.tagOpt --no-tags`), and never push with `--tags` or `--follow-tags`.

## 2. Resolving conflicts

Go conflict by conflict (`git diff --name-only --diff-filter=U`). Settle each hunk line by line against the ancestor: a hunk often holds lines only one side changed, and a line only one side changed keeps that side's change. For example, upstream adds a table row next to a line where FuTab wrote "OxiGuitar recommends" for upstream's "we recommend": keep the new row and FuTab's line. The kinds below are for lines both sides changed. For each, decide which kind it is:

- **Name only:** ours and theirs differ only in a name from the table below. Keep ours.
- **Behaviour, with names in it:** upstream changed code, text or config, and the text it touched has FuTab's names on our side. Take upstream's version, then put every name back to FuTab's using the table. Check the result line by line against both sides: nothing of upstream's change dropped, no OxiGuitar name brought back. If upstream deleted or rewrote lines that FuTab changed only for the name, take upstream's side: a deletion stays deleted, with no FuTab name to put back.
- **Both changed behaviour:** FuTab changed the same lines for a reason of its own (for example the hidden MIDI advice in `crates/oxiguitar-host/src/advice.rs`). Keep both if they combine; if they don't, stop and ask me, quoting both sides.

Files:

- `CHANGELOG.md`: always keep ours, conflict or not: `git checkout HEAD -- CHANGELOG.md`. Not `--ours`, which does nothing when there's no conflict: upstream's entries, and even its release heading (`## [0.20.1]` above FuTab's entries, from OxiGuitar PR 306), can merge in cleanly. Check after every merge, before adding the merge's own entry (step 4): `git diff --cached --name-only HEAD -- CHANGELOG.md` must print nothing. FuTab's changelog lists FuTab's changes only.
- `ROADMAP.md` is FuTab's own roadmap: never merge anything from upstream into it, conflict or not. Keep ours (`git checkout --ours ROADMAP.md`). A file only upstream changed merges without a conflict, so check after every merge: `git diff --cached --name-only HEAD -- ROADMAP.md` must print nothing. Upstream's mentions of `ROADMAP.md` elsewhere (its milestones M1, M2…, "see ROADMAP.md") mean OxiGuitar's roadmap: in FuTab's files write them as "OxiGuitar's roadmap" (plain text, no link), as in `CREDITS.md`; comments, `docs/design/`, `docs/adr/` and `docs/parity.md` keep them as they are. Step 3 checks for them.
- `CREDITS.md` is FuTab's:
  - **The opening is static**, everything from `# Credits` to the end of `## Special thanks` (FuTab's copyright, FuTab's intro, "FuTab is a fork of OxiGuitar", OxiGuitar's copyright, the thanks). Keep ours exactly; take none of upstream's changes there, not even a wording change.
  - **The sections after Special thanks** (the projects, the crates, fonts and assets) merge as usual: upstream's changes, with FuTab's names. FuTab's own rows (the OxiGuitar row, the FuTab icon) stay. No row names a version (since OxiGuitar PR 295: "MuseScore Studio", not "MuseScore Studio 4.7"; the licence report from `Cargo.lock` has the exact ones), FuTab's OxiGuitar row included: "OxiGuitar", not "OxiGuitar 0.19.1".
  - **Trademarks:** keep FuTab's sentence, "FuTab mirrors Guitar Pro's layout and shortcuts only: …". Take upstream's other changes to the section.
- Install instructions (`README.md`'s install sections, `docs/manual/src/installing.md` and `docs/manual/src/install-*.md`) are FuTab's: FuTab's own package, then only OxiGuitar's plugin packages. From upstream take only which plugins there are: a plugin package added or removed goes into FuTab's commands and lists, with its one-line description (for example OxiGuitar PR 296 added `oxiguitar-wah` to FuTab's `apt install` and `dnf install` lines and to `install-linux.md`'s list). Never take upstream's instructions for the `oxiguitar` package itself, or its download sections FuTab removed (AppImage, Windows, macOS). Whatever upstream changes there, keep FuTab's:
  - **The order:** install FuTab first, then OxiGuitar's plugins (`install-linux.md`'s "1. Install FuTab" and "2. Install the plugins").
  - **FuTab's downloads:** the links to FuTab's latest release (`PurpleIcon/futab/releases/latest`), the tables of FuTab's files (`futab-VERSION-1.x86_64.rpm`, `futab_VERSION_amd64.deb`, `FuTab-VERSION-x86_64.AppImage`, `FuTab-VERSION-windows-x86_64.zip`), the `futab-x11` note, and "FuTab installs beside OxiGuitar without sharing a file or a setting with it".
  - **What FuTab's packages do:** they recommend the Guitar Pro, MIDI, ALSA and PipeWire plugins, so adding OxiGuitar's repository first installs them with FuTab. If upstream changes which plugins `scripts/package/linux.sh` recommends, change this sentence to match.
  - **What FuTab has and hasn't released:** Linux and Windows downloads; macOS builds from source until FuTab publishes a macOS download. Never bring back "no packages yet" or "no download yet" for a system FuTab releases for.
- A file FuTab renamed (desktop entry, metainfo, mime XML, man pages, `debian/*.manpages`, `scripts/package/oxiguitar-start`, icons): upstream's changes go into **FuTab's** file. If git reports modify/delete or leaves upstream's old-named file behind, apply upstream's change to FuTab's file and `git rm` the old name. An upstream change to the metainfo that only adds a `<release>` (every upstream release commit makes one) brings nothing to FuTab's file, by the version rule below: just `git rm` the old name.
- A file FuTab deleted on purpose (`scripts/new-repo.sh`, `scripts/split-history.sh`, the PayPal button and QR code, the placeholder icon): keep it deleted. If upstream changed it, tell me in one line.
- `README.md` sections FuTab removed: upstream's Status, its feature showcase (the screenshots, "Hear it", paragraphs such as OxiGuitar PR 301's "Drums") and its own privacy wording stay removed; drop upstream's additions there, and any new file only they use (`git rm` it, as `docs/readme/drums.png`). FuTab's README keeps its own structure; its install sections follow the install-docs rule above.
- A file upstream added: keep it. If its name or contents carry OxiGuitar names that the table renames, rename them.
- `.github/FUNDING.yml`: never take upstream's (it points at OxiGuitar's donations). If FuTab has its own, keep ours (`git checkout --ours .github/FUNDING.yml`). If FuTab has none, take it out of the merge (`git rm -f .github/FUNDING.yml`). A file only upstream added or changed merges without a conflict, so check this after every merge, conflicts or not (`git diff --cached --name-only HEAD -- .github/FUNDING.yml` must print nothing). This is settled in the merge, not by skipping the PR that brought it.
- Version numbers (`Cargo.toml`, `Cargo.lock`, `spikes/*/Cargo.lock`, `debian/changelog`, the test plugins' `manifest.json`, metainfo `<release>`): FuTab has its own version (0.1.0 was its first release; OxiGuitar's are 0.19 and up). Upstream's release commits ("Release x.y.z", no PR) change only these and its changelog, and conflict in every merge that crosses one. Keep FuTab's version, FuTab's `debian/changelog` entries and FuTab's metainfo `<release>` entries only (never add upstream's), and take only upstream's dependency changes in the `Cargo.lock` files (a spike's lists the core's crates at the app's version too). If `Cargo.lock` doesn't settle cleanly, take theirs and then run `cargo build` so Cargo writes FuTab's own entries back; for a spike's, take theirs and run `cargo metadata --manifest-path spikes/<name>/Cargo.toml --format-version 1 > /dev/null`, which rewrites its lock without building. If upstream's release is a good point for a FuTab release too, say so; don't bump anything yourself.

## The name table

What FuTab renamed: always FuTab's side in a merge.

| OxiGuitar (upstream) | FuTab |
| --- | --- |
| `OxiGuitar` (the app's name, in text users read: UI strings, messages, the user manual `docs/manual/`, the plugin guide `docs/plugins/`, man pages, metainfo, README) | `FuTab` |
| package and binary `oxiguitar`, `oxiguitar-x11`, `oxiguitar-cli` (`cargo run -p ...`, `target/.../oxiguitar*`, `/usr/bin/...`, `/app/bin/...`, `oxiguitar.exe`) | `futab`, `futab-x11`, `futab-cli`, `futab.exe` |
| package `oxiguitar-app` (`-p`, `--exclude`, `cargo tree -p`, messages such as "build oxiguitar-app with…") | `futab` (the folder `crates/oxiguitar-app/` stays) |
| app ID `io.github.mateusrdp.OxiGuitar` (and file names that use it) | `io.github.purpleicon.FuTab` |
| repository `mateusrdp/oxiguitar` as **this** project's home: `repository`/`homepage`, bug reports, issues, discussions, screenshots (web addresses: only those in "Web addresses" below; ask about any other) | `PurpleIcon/futab` |
| settings, data and cache folders `oxiguitar` / `OxiGuitar` | `futab` / `FuTab` |
| FuTab's own plugin folders: `lib/oxiguitar/plugins`, `~/.local/share/oxiguitar/plugins`, `Application Support/OxiGuitar/plugins` (searched first), and the shared folders beside them (`lib/oxiguitar/<name>`, `~/.local/share/oxiguitar/<name>`, such as `soundfonts`, `nam` or a plugin's own) | `lib/futab/plugins`, `~/.local/share/futab/plugins`, `Application Support/FuTab/plugins`; `lib/futab/<name>`, `~/.local/share/futab/<name>`. Where text lists the system folders, add OxiGuitar's after FuTab's (`/usr/lib/futab/<name>`, then `/usr/lib/oxiguitar/<name>`): FuTab searches both |
| release files `OxiGuitar-…AppImage`, `…flatpak`, `…windows-….zip`, `…macos-universal.dmg`; `dist/OxiGuitar-…` | `FuTab-…` |
| launcher `oxiguitar-start`, man pages `oxiguitar.1`, `oxiguitar-cli.1` | `futab-start`, `futab.1`, `futab-cli.1` |
| icon `oxiguitar-*.png`, `oxiguitar-placeholder.svg` | `futab-*.png`, `futab.svg` |
| the core's advice dialog title / plugin name "OxiGuitar" (`Asked::core`) | "FuTab" |
| debian package `oxiguitar`, maintainer `OxiGuitar <maintainer@oxiguitar.invalid>` | `futab`, `FuTab <maintainer@futab.invalid>` |

**Versions in text.** FuTab's version numbers are its own, so "OxiGuitar 0.18" never becomes "FuTab 0.18". What a requirement needs ("Needs OxiGuitar 0.18 or later") becomes the first FuTab release that holds that OxiGuitar release, from the table below. A note about OxiGuitar's past ("Called SoundFont in OxiGuitar 0.10 and earlier") stays OxiGuitar's. If a requirement is newer than every FuTab release, ask me. Add a row with each FuTab release.

| OxiGuitar | First FuTab release that holds it |
| --- | --- |
| up to 0.19.1, and up to OxiGuitar PR 290 (mateusrdp/oxiguitar@4ae4593) | 0.1.0 |
| 0.19.2 up to 0.21.1 (mateusrdp/oxiguitar@e72d200) | 0.2.0 |

What stays OxiGuitar's: never rename these, in a merge or anywhere else.

- **Credit and copyright:** SPDX headers (`Copyright (C) 2026 Mateus Rocha de Paula and the OxiGuitar contributors`), `authors` in manifests, OxiGuitar's copyright line and row in CREDITS.md (the file itself is FuTab's: see step 2), the About box's credit to OxiGuitar, "a fork of OxiGuitar".
- **Code names:** crate folders (`crates/oxiguitar-*`), the library crates and their Rust names (`oxiguitar_plugin`, `oxiguitar_host`, ...), the `OXIGUITAR_*` environment variables (`OXIGUITAR_HOME`, ...).
- **Plugins** (OxiGuitar's, used as they are): plugin repo and package names (`oxiguitar-guitarpro`, `oxiguitar-midi`, ...), plugin ids (`oxiguitar.midi`, ...), the core's advice id `oxiguitar` (`advice::CORE`), `oxiguitar-set.json`, `.oxp` files, and the plugin SDK's git source `https://github.com/mateusrdp/oxiguitar` in plugin `Cargo.toml`s.
- **OxiGuitar's plugin folders as a fallback** (`/usr/lib/oxiguitar/plugins` and the others, searched after FuTab's), the shared folders beside them (`/usr/lib/oxiguitar/<name>`), and `/usr/share/oxiguitar/soundfonts`.
- **File formats:** the `.oxg` sidecar and anything else written to a user's files. Renaming those would break files people already have.
- **Code comments and design records:** comments in the code (`//`, `///`, `//!`, `#`), `docs/design/`, `docs/adr/` and `docs/parity.md` (OxiGuitar's feature check against Guitar Pro, TuxGuitar and alphaTab, from OxiGuitar PR 298) keep OxiGuitar's name, and upstream's changes to them are taken as they are. They record OxiGuitar's design, decisions and checks; renaming them would only make every later merge conflict. FuTab's own design notes and decisions go in `docs/futab-design/` and `docs/futab-adr/`, never into these.
- **Links to upstream as upstream:** the `upstream` remote, links to OxiGuitar's changelog, PRs and issues, the catch-up script. In anything that reaches GitHub (commit messages, PR text, the changelog), name upstream PRs as `OxiGuitar PR N`, never `mateusrdp/oxiguitar#N`: see Referring to upstream in `.claude/rules/github.md`.

When a name fits neither list, it's the clash you can't settle: list it with its file and line, and ask me.

## Web addresses

Never merge a link to OxiGuitar (`github.com/mateusrdp/...`, or any other site of OxiGuitar's) as it is, and never rename one to FuTab's on your own: each needs a decision. The links decided so far, in code, docs, scripts and workflows:

| Link | Points at |
| --- | --- |
| Help → About's **Credits** link (`links::CREDITS` in `crates/oxiguitar-app/src/links.rs`, and its test) | `https://github.com/PurpleIcon/futab/blob/main/CREDITS.md` |
| Bug reports and issues of the app (`ISSUES_URL` in `inventory.rs`, `ISSUES` in `crash.rs`, the packages' bug address) | `https://github.com/PurpleIcon/futab/issues` (`/issues/new` where upstream opens a new one) |
| The project's home (`repository`, `homepage`, the packages' and release notes' links to FuTab) | `https://github.com/PurpleIcon/futab` |
| About's "a fork of OxiGuitar" line | `https://github.com/mateusrdp/oxiguitar` (stays) |
| Where the plugins are published (`PLUGINS_URL` in `inventory.rs`), the release notes' links to OxiGuitar's plugins | OxiGuitar's (stays) |
| The plugin SDK's git source (plugin `Cargo.toml`s, `scripts/check-plugin-template.sh`, the plugin guide), the `upstream` remote and `scripts/upstream/catchup.py` | OxiGuitar's (stays) |

For any other link to OxiGuitar that a merge brings in, new or changed: stop and ask me, with its file, line and what it's for, and what you'd point it at. Then add my answer to this table. The step-3 check below finds them (`mateusrdp`).

## 3. Check that no old name came back

Once no conflicts are left, run these. They cover the lines that merged cleanly too:

```bash
git diff --cached HEAD -U0 | grep -nE '^\+.*(OxiGuitar|oxiguitar|mateusrdp|maintainer@oxiguitar)' | grep -v '^+++'
```

Go through every hit against the two lists: rename what the table renames, leave what stays OxiGuitar's, and ask about the rest. Then:

```bash
git diff --cached --name-only --diff-filter=A HEAD | grep -i oxiguitar
```

These are new files with OxiGuitar in their name; rename them by the table. Then:

```bash
git diff --cached HEAD -U0 -- . ':!docs/design' ':!docs/adr' ':!docs/parity.md' | grep -n '^+.*ROADMAP' | grep -v '^[0-9]*:+++'
```

These are mentions of upstream's roadmap: write each as "OxiGuitar's roadmap" (step 2, `ROADMAP.md`), unless it's a code comment. Then:

```bash
git diff --cached HEAD -U0 -- . ':!docs/design' ':!docs/adr' ':!docs/parity.md' ':!CHANGELOG.md' | grep -nE '^\+.*(-p oxiguitar(-app|-cli)?\b|--exclude oxiguitar-app|\boxiguitar-(app|cli|x11)\b[^/]|/bin/oxiguitar|oxiguitar\.exe|target/[a-z]+/oxiguitar)' | grep -v '^[0-9]*:+++'
```

These are package and binary names, often in lines that merged cleanly (OxiGuitar PR 305's new Clippy steps in `ci.yml` used `-p oxiguitar-app`, which would have failed FuTab's CI). The first check above lists them too, but among the crate names that stay; this one lists only these. Rename each by the table (`oxiguitar-app` → `futab`, `oxiguitar-cli` → `futab-cli`, `oxiguitar-x11` → `futab-x11`), except crate folder paths (`crates/oxiguitar-app/…`) and code comments. Then do the build and lint checks (not the tests unless I ask):

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

Then reword the revert's message to `Skip OxiGuitar's <title> (OxiGuitar PR X)`, with the reason in its body. Settle any conflicts as in step 2, check names and build again (step 3), and name every skipped PR, with its reason, in the report and the PR description. Upstream's release commits and FuTab's own version are never handled by skipping: step 2's rules for version numbers cover them.

What skipping means (say this to me when I ask to skip, for that PR in particular):

- **Upstream counts it as merged.** The catch-up report won't list it again, and git won't offer it again. Getting it later takes a deliberate `git revert` of the revert, not another merge.
- **Later upstream PRs may build on it** (for example #289 builds on #270's Harmonize). Before skipping, check whether later missing PRs touch the same files or code (`git diff --stat <sha>^ <sha>`, compared with what later commits change). If they do, they'll conflict or not build once it's skipped. Say which ones, and skip them all or none.
- **The cost grows with every merge.** Each later upstream change to the code the revert removed conflicts again in every future merge. Skipping suits self-contained changes FuTab doesn't want (OxiGuitar-only links or branding; `FUNDING.yml` has its own rule in step 2); for a feature FuTab doesn't want, hiding it behind a setting or a plugin is often cheaper over time than reverting it.
- **The changelog leaves it out**, and the PR description says why.

## 4. Changelog

Add the merge's entry under `## [Unreleased]` → `### Changed` in `CHANGELOG.md`, in the form `.claude/rules/github.md` gives ("Merged OxiGuitar x.y.z", or "Merged OxiGuitar up to OxiGuitar PR N" when the target isn't a release; one line per upstream PR in the user's words, `OxiGuitar PR N`). Leave out what FuTab dropped, and upstream's release and changelog commits.

## 5. Report and hand over

Tell me, short:

- the upstream PRs merged, and the ones skipped with their reasons;
- every conflict and how it was settled ("name only, kept ours", "upstream's change, FuTab's names", "both kept");
- every name you left as OxiGuitar on purpose, if it's not obvious from the lists;
- what you need me to decide.

Then stop. Commit only when I say so (`git commit -s`, the merge's own message is fine). In the PR, say that it **must be merged with "Create a merge commit", never squash or rebase**: squashing throws away upstream's ancestry, so the next merge would conflict all over again and the catch-up report would list everything again.

### The pull request

When I ask for the PR (push only when I say so):

- **Title:** `Merge FROM upstream oxiguitar #N`, where `#N` is the last upstream PR the merge brings in (the target's PR, or the last PR before it when the target is a release or other commit without one). For example: `Merge FROM upstream oxiguitar #290`. The capital FROM keeps the direction plain: FuTab takes OxiGuitar's changes, nothing goes back to OxiGuitar. Never a title that could read as merging into upstream (the old `Merge upstream to oxiguitar #N` did). Nothing else in the title: no repository prefix, no list of PRs, no release number.
- **Description:** first, the warning to merge with "Create a merge commit", never squash or rebase, and why. Then the upstream PRs merged (as `OxiGuitar PR N`, never `mateusrdp/oxiguitar#N`, with what each changes and its merge commit), the skipped ones with reasons, what upstream still has, every conflict and how it was settled, the names changed and kept, behaviour changes users will notice, the checks run, and test steps.
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

   If the branch rules block it only for want of a review (I can't approve my own PRs), add `--admin` once I've said to merge: that's how I merge them. Never `--squash` or `--rebase`, whatever the repository's default. If the admin merge is refused (the session's permission check may block it), don't work around it: ask me to merge it on GitHub, saying plainly: **"Merge #N with Create a merge commit, not Squash and merge: it carries upstream's history."**
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

   with a message saying which PR was squashed and that the merge changes no file, naming the target as `OxiGuitar PR N`.
3. Check: `git diff origin/develop HEAD` is empty, and the catch-up report on the branch shows the target as the last common commit.
4. Add a changelog entry under `### Fixed` ("Upstream history up to OxiGuitar PR N", why it was missing, and that the merge changes no file) as a commit of its own.
5. With my go-ahead, push and open the PR titled `Restore history FROM upstream oxiguitar #N`, its description opening with the merge-commit warning, and merge it as above, with `--merge`.

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

When the report says what, and why it can lag behind, is in the `upstream-report` skill (`.claude/skills/upstream-report/SKILL.md`).

## Keeping this skill current

If you learn something in a merge that this skill should know (a new rename, a new file that keeps OxiGuitar's name), ask me whether to add it here.
