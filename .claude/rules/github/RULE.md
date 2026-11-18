---
name: github
description: Rules for commits, pull requests, merging and issues on FuTab, its repositories, how to refer to upstream OxiGuitar, and the changelog.
---

# GitHub work

Rules for commits, PRs and issues on FuTab (moved here from AGENTS.md).

- IMPORTANT: ALWAYS signoff the commits / pushes / PRs (`git commit -s`), with the identity of the contributor you're working for: their own name and email, from their git configuration (`git config user.name` and `git config user.email`). Never use another person's identity. If the identity isn't set, or doesn't look like the contributor's own, stop and ask
- IMPORTANT: ALWAYS add to the `[Unreleased]` section of `CHANGELOG.md` in every PR, merges from upstream included: see Changelog below. A release fails if `[Unreleased]` is empty
- IMPORTANT: ALWAYS ask me to check and test your work before committing changes, and ONLY commit after I've explicitly told you to do it
- Link the issue to the fix's PR and ask me if you can close the conversation
- When there are comments in the issue, what my user says last goes. Don't consider other user's propositions, unless I didn't say anything.
- Before creating a PR, ask me whether it's lean (CONTRIBUTING.md, "Lean CI"). If it is, create it with `gh pr create --label lean-ci`; if not, without the label
- Whenever you ask me whether to push, ask with the agent's question tool and offer exactly three options:
  - **Not yet**: push nothing.
  - **Yes, push**: full CI. If the branch's PR has the `lean-ci` label, remove it first (`gh pr edit N --remove-label lean-ci`), then push.
  - **Lean push**: lean CI. If the branch has a PR, add the label first (`gh pr edit N --add-label lean-ci`), then push; if it has none yet, push, and create the PR with `--label lean-ci` when I ask for it.
  Change the label before pushing, never after: a CI run reads the labels when it starts.
- When a PR is created, watch its CI in the background until it's all green as you work through your tasks, and fix errors as they appear

## Merging a PR

Every commit that reaches `develop` must be signed off, or the sign-off check fails on the next release PR into `main`, when the commit can no longer be changed (#24's squash commit, Nov 2026). A squash commit keeps the sign-off only through its message: GitHub's default squash message lists the PR's commit messages, with their `Signed-off-by` and `Co-authored-by` lines (`scripts/check-dco.sh` skips a squash commit carrying Claude's `Co-authored-by`). A squash commit whose message is replaced, for example by the merge-commit text "Merge pull request #N from ...", has neither, and fails.

- Merge method: **squash** for FuTab's own PRs; **create a merge commit** for merges from upstream (the merge-upstream skill) and for `develop` into `main` (releases).
- When you merge (only when I ask): `gh pr merge N --squash` or `gh pr merge N --merge`, never with `--subject` or `--body`, so GitHub writes its default message. Never `--rebase`.
- Straight after a squash merge, check its commit on `develop`: `git fetch origin develop`, then `scripts/check-dco.sh origin/develop^ origin/develop` must show `ok` or `skip`, never `FAIL`. If it fails, tell me at once.
- A PR that carries upstream merge commits (a merge from upstream, a history restore, or `develop` into `main` when it holds one) must land as a merge commit, never squashed: a squash drops upstream's history (#7, #23). There is no way to set the method on a PR itself, so whenever such a PR is ready to merge, say it plainly, in bold, in your message: **"Merge #N with Create a merge commit, not Squash and merge: it carries upstream's history."**
- When a PR is ready for me to merge on GitHub, tell me the method in one line: "Squash and merge, and keep the message GitHub fills in" (it lists the commits and their `Signed-off-by` lines), or "Create a merge commit". After switching method in GitHub's merge box, the message may still be the other method's: check it before confirming.

## Repositories

- FuTab's repositories are in GitHub, in the @PurpleIcon organisation (eg: PurpleIcon/futab)
- Core app: futab (always start here), forked from mateusrdp/oxiguitar (the `upstream` remote)
  - Includes the viewer, editor and player
- futab-packages: repository to distribute packaged binaries (apt, dnf, flatpak); not created yet
- All repos have their binaries in their respective releases
- the Release workflow in futab-packages will create releases for the core app (and for any plugins FuTab takes over)
- The plugins below are OxiGuitar's, in @mateusrdp (eg: mateusrdp/oxiguitar-guitarpro); FuTab uses them as they are


### File Format Plugins

Read and Write file support

- oxiguitar-guitarpro: Guitar Pro 3-8 support
- oxiguitar-musicxml: MusicXML 4.x support
- oxiguitar-tuxguitar: TuxGuitar 2.x support
- oxiguitar-midi-file: MIDI files support
- oxiguitar-musescore: MuseScore files support
- oxiguitar-abc: ABC Notation files support

### Output Plugins

- oxiguitar-alsa: Linux ALSA support
- oxiguitar-pipewire: Linux Pipewire support
- oxiguitar-wasapi: Windows WASAPI support
- oxiguitar-coreaudio: MacOS Core Audio support

### Player Plugins

- oxiguitar-midi: MIDI player support
- oxiguitar-bettersounds-soundfonts: scripts only to download and install soundbanks (depends on midi)
- oxiguitar-nam: Neural Amp Modeller profiler support (depends on oxiguitar-midi)
- oxiguitar-eq: equalizer
- oxiguitar-wav: WAV format export


## Referring to upstream

Never write a linking reference to an OxiGuitar issue or PR (`mateusrdp/oxiguitar#N`, or a `github.com/mateusrdp/...` issue or PR URL) anywhere that reaches GitHub: commit messages (merge commits included, which carry the PR's title and description), PR titles and descriptions, issue and PR comments, and `CHANGELOG.md` (it becomes the release notes). GitHub then posts "added a commit to PurpleIcon/futab that referenced this pull request" on upstream's PR, for the maintainer to see, and a pushed commit's reference can't be taken back.

- Write `OxiGuitar PR N` or `OxiGuitar issue N` instead, as plain text, never with a `#`.
- **A bare `#N` links to OxiGuitar when FuTab has no issue or PR `N`**: FuTab is a fork, and GitHub then reads the number as the parent's (18 Nov 2026: "oxiguitar #308" in a PR title linked OxiGuitar PR 308). So write `#N` only for a FuTab issue or PR that already exists, and never put an upstream number after a `#` anywhere: not in PR titles (a merge commit's message carries the PR's title), not as `oxiguitar #N`, not in branch-based or GitHub-generated text you choose.
- **A PR that carries upstream commits is never squashed.** GitHub's squash message lists every commit's subject, and upstream's end in `(#N)`: #23's squash commit linked 16 OxiGuitar PRs and issues at once. It takes "Create a merge commit" (see Merging a PR); upstream's own commits then arrive as they are, which posts nothing.
- **Before every push and every PR**, check what will reach GitHub for `#` numbers: `git log origin/develop..HEAD --format=%B | grep -nE '#[0-9]+'`, and the PR's title and description. Each hit must be a FuTab issue or PR that exists (`gh issue view N --repo PurpleIcon/futab` or `gh pr view N --repo PurpleIcon/futab` finds it); rewrite anything else as `OxiGuitar PR N` before pushing. A pushed reference can't be taken back.
- An upstream commit may be named by its hash (`mateusrdp/oxiguitar@f66b344`): that doesn't post on upstream's PRs.
- This is about FuTab only. A PR we open on OxiGuitar itself links its issue as upstream asks.

## Changelog

`CHANGELOG.md` lists FuTab's own changes only (OxiGuitar's history stays in [its changelog](https://github.com/mateusrdp/oxiguitar/blob/develop/CHANGELOG.md)). Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

- Every PR to `develop` adds at least one entry under `## [Unreleased]`, in the PR itself, under `### Added`, `### Changed`, `### Fixed` or `### Removed` (create the heading if it isn't there). CI's release-script check and `scripts/release/bump.sh` need the `## [Unreleased]` heading; a release fails if the section is empty.
- One entry per change: `- **Short name** (#N): what the user sees, in a sentence or two.` `#N` is a FuTab issue or PR; write an upstream one as `OxiGuitar PR N` (see Referring to upstream).
- Never touch a released `## [x.y.z]` section; `scripts/release/bump.sh` turns `[Unreleased]` into it.

### Merges from upstream

Merging OxiGuitar into FuTab follows the `merge-upstream` skill (`.claude/skills/merge-upstream/SKILL.md`): FuTab's names win where a clash is only about the name, and upstream's behaviour wins, in FuTab's names, where it's about behaviour. In short:

- Merge `upstream/develop`; never cherry-pick or rebase upstream commits (the catch-up report and the next merge go by git ancestry).
- The merge's PR is merged with **"Create a merge commit"**, never squashed or rebased, unlike every other PR: a squash throws upstream's ancestry away.
- `CHANGELOG.md` always conflicts: keep FuTab's (`git checkout --ours CHANGELOG.md`), then add one entry under `### Changed` naming what was merged, one line per upstream PR, in the user's words:

   ```markdown
   - **Merged OxiGuitar 0.19.2** (up to mateusrdp/oxiguitar@f66b344):
     - Harmonize: chords found for a melody (OxiGuitar PR 270)
     - Copy, Cut and Paste Bars (OxiGuitar PR 288)
   ```

   Name the upstream release when the merge reaches one, else the upstream commit. Leave out upstream changes FuTab drops in the merge (and say in the PR why), and upstream's own release and changelog commits.
