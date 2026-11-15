# GitHub work

Rules for commits, PRs and issues on FuTab (moved here from AGENTS.md).

- IMPORTANT: ALWAYS signoff the commits / pushes / PRs (`git commit -s`), with the identity of the contributor you're working for: their own name and email, from their git configuration (`git config user.name` and `git config user.email`). Never use another person's identity. If the identity isn't set, or doesn't look like the contributor's own, stop and ask
- IMPORTANT: ALWAYS add to the `[Unreleased]` section of `CHANGELOG.md` in every PR, merges from upstream included: see Changelog below. A release fails if `[Unreleased]` is empty
- IMPORTANT: ALWAYS ask me to check and test your work before committing changes, and ONLY commit after I've explicitly told you to do it
- Link the issue to the fix's PR and ask me if you can close the conversation
- When there are comments in the issue, what my user says last goes. Don't consider other user's propositions, unless I didn't say anything.
- When a PR is created, watch its CI in the background until it's all green as you work through your tasks, and fix errors as they appear

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


## Changelog

`CHANGELOG.md` lists FuTab's own changes only (OxiGuitar's history stays in [its changelog](https://github.com/mateusrdp/oxiguitar/blob/develop/CHANGELOG.md)). Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

- Every PR to `develop` adds at least one entry under `## [Unreleased]`, in the PR itself, under `### Added`, `### Changed`, `### Fixed` or `### Removed` (create the heading if it isn't there). CI's release-script check and `scripts/release/bump.sh` need the `## [Unreleased]` heading; a release fails if the section is empty.
- One entry per change: `- **Short name** (#N): what the user sees, in a sentence or two.` `#N` is a FuTab issue or PR; write an upstream one as `mateusrdp/oxiguitar#N`, since a bare `#N` points at FuTab's.
- Never touch a released `## [x.y.z]` section; `scripts/release/bump.sh` turns `[Unreleased]` into it.

### Merges from upstream

Merging OxiGuitar into FuTab follows the `merge-upstream` skill (`.claude/skills/merge-upstream/SKILL.md`): FuTab's names win where a clash is only about the name, and upstream's behaviour wins, in FuTab's names, where it's about behaviour. In short:

- Merge `upstream/develop`; never cherry-pick or rebase upstream commits (the catch-up report and the next merge go by git ancestry).
- The merge's PR is merged with **"Create a merge commit"**, never squashed or rebased, unlike every other PR: a squash throws upstream's ancestry away.
- `CHANGELOG.md` always conflicts: keep FuTab's (`git checkout --ours CHANGELOG.md`), then add one entry under `### Changed` naming what was merged, one line per upstream PR, in the user's words:

   ```markdown
   - **Merged OxiGuitar 0.19.2** (up to mateusrdp/oxiguitar@f66b344):
     - Harmonize: chords found for a melody (mateusrdp/oxiguitar#270)
     - Copy, Cut and Paste Bars (mateusrdp/oxiguitar#288)
   ```

   Name the upstream release when the merge reaches one, else the upstream commit. Leave out upstream changes FuTab drops in the merge (and say in the PR why), and upstream's own release and changelog commits.
