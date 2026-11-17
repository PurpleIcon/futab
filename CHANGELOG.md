# Changelog

All notable changes to FuTab. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [Semantic Versioning](https://semver.org/).

FuTab is a fork of [OxiGuitar](https://github.com/mateusrdp/oxiguitar), taken from OxiGuitar 0.19.1 on 13 Nov 2026. This file lists only FuTab's own changes; OxiGuitar's are in [its changelog](https://github.com/mateusrdp/oxiguitar/blob/develop/CHANGELOG.md).

## [Unreleased]

### Added

- **build-test-rpm skill** (#17): the agent skill builds a test `.rpm` from the working copy (release build, licence report, package) and says how to install it with dnf, to test FuTab as a packaged app.
- **upstream-report skill** (#18): the agent skill updates `oxiguitar-catchup.md` with `scripts/upstream/catchup.py` and sums up what OxiGuitar has that FuTab hasn't merged yet, and which files a merge would conflict in. The merge-upstream skill uses it.
- **Lean CI label** (#19): a pull request labelled `lean-ci` runs only formatting, lint and the sign-off check, and skips the tests, packages and other long checks, which still run after the merge into `develop`. CONTRIBUTING.md says when to use it.
- **Lean PRs in the agent rules** (#20): before opening a pull request, the agent asks whether it's lean, and if so opens it with the `lean-ci` label.

### Changed

- **Credits** (#21): CREDITS.md reads as FuTab's: FuTab's own copyright line, and OxiGuitar listed first among the projects FuTab comes from, with its authors and licence.
- **merge-upstream skill** (#22): conflicts show the common ancestor and are settled line by line; a deletion upstream wins over a FuTab rename; OxiGuitar's version numbers never become FuTab's (a table maps them to FuTab releases); the shared folders beside the plugin folders take FuTab's names; upstream's `FUNDING.yml` is never taken; release commits' version changes cover the spikes' lockfiles and the renamed metainfo too.

### Fixed

- **Version numbers in the manual and the plugin guide** (#22): versions from before the fork read as OxiGuitar's again (they had been renamed to FuTab 0.2 to 0.18, versions FuTab never had), and what a plugin needs reads FuTab 0.1.0 or later. The plugin template's copy step uses the folder `git clone` makes again.
- **Desktop icon** (#16): FuTab's icon shows again when searching for the app on the desktop. The icon file opened with a long comment, so desktops didn't recognise it as an SVG image and showed a blank icon.

## [0.1.0] - 2026-11-16

FuTab's first release, from OxiGuitar 0.19.1 with OxiGuitar's changes up to OxiGuitar PR 290.

### Added

- **First release** (#13, #14): FuTab 0.1.0 for Linux (.deb, .rpm, AppImage) and Windows (portable zip), on the Releases page. No macOS download yet: GitHub's macOS build machines were too busy to build it reliably, so on a Mac build FuTab from source. The Flatpak is a preview: it runs, but opens and plays nothing until OxiGuitar publishes its Guitar Pro and audio-output plugins as Flatpaks. FuTab's own version numbers start here, apart from OxiGuitar's.
- **Upstream catch-up report**: `python3 -I scripts/upstream/catchup.py` writes `oxiguitar-catchup.md` (gitignored): the OxiGuitar releases and commits FuTab hasn't merged yet, each with its upstream pull request, and the files a catch-up merge would conflict in. The Upstream workflow runs it every Monday and by hand, and shows it in the run's summary. It holds while FuTab catches up by merging `upstream/develop`, not by cherry-picking.

### Changed

- **No upstream backlinks**: FuTab's commits, PRs and changelog name OxiGuitar's PRs as plain text (`OxiGuitar PR N`), so GitHub no longer posts "referenced this pull request" notices on upstream's PRs. The agent rules and the merge-upstream skill say so.
- **merge-upstream skill: merging and squash recovery**: the skill merges an upstream-merge PR itself with a merge commit (`gh pr merge --merge`) once checks are green, and says how to restore upstream's history when one was squashed anyway (a merge with strategy `ours` that changes no file, as in #8).
- **merge-upstream skill: PR title**: a pull request that merges OxiGuitar is titled `Merge upstream to oxiguitar #N`, after the last upstream PR it brings in, and its description opens with the merge-commit warning.
- **Merged OxiGuitar up to OxiGuitar PR 290** (mateusrdp/oxiguitar@4ae4593):
  - Play Engraved Beat sounds only when a note or rest is entered or deleted, no longer on other edits such as durations or effects (OxiGuitar PR 286)
  - Harmonize… (Tools menu, or right-click on the page) finds chords for the caret's track and writes them above it with their diagrams, as one step for Undo (OxiGuitar PR 270, OxiGuitar PR 289)
  - Copy Bars, Cut Bars and Paste Bars (Ctrl + Shift + C, X and V, also in the Edit menu) work on whole bars, from the caret's track or all tracks; Paste no longer squeezes several bars into one, and runs on over bar lines (OxiGuitar PR 288)
  - The chord dialog is redesigned: a name, a voicing and a diagram that follow one another, chord names in Popular, Jazz, Compact or Custom style, and it remembers the style and "Add diagram" for the next chord (OxiGuitar PR 290)
- **FuTab's own design notes and decision records**: `docs/futab-design/` and `docs/futab-adr/` (numbered from 0001, with its own template) hold FuTab's; `docs/design/` and `docs/adr/` stay OxiGuitar's, merged from upstream and not edited. CONTRIBUTING.md, the agent rules and the merge-upstream skill say so.
- **FuTab**: this fork of OxiGuitar is now called FuTab in the app: window title, About box (which credits OxiGuitar), messages, desktop entry, AppStream metainfo and macOS bundle name. FuTab has its own icon (a plectrum split in two, with a note in each half) in place of the green placeholder pick. The PayPal donation button, QR code and README section are removed. The app ID is `io.github.purpleicon.FuTab`. Settings live in FuTab's own folders (`~/.config/futab`, `~/.local/share/futab`, `~/.cache/futab`; `FuTab` on macOS and Windows), so FuTab never touches an installed OxiGuitar's settings. Plugins are found in FuTab's folders first and then in OxiGuitar's (`/usr/lib/oxiguitar/plugins` and the others), so OxiGuitar's plugin packages work in FuTab. Bug reports go to `PurpleIcon/futab`. The programs are `futab`, `futab-x11` and `futab-cli` (`cargo run -p futab`, `cargo run -p futab-cli`), and the packages `futab` and `futab-x11` (.deb and .rpm), `FuTab-…AppImage`, `FuTab-…flatpak`, `FuTab-…windows-….zip` and `FuTab-…macos-universal.dmg`, with their own man pages, launcher and library folder, so FuTab installs beside OxiGuitar without a file in common. The crates' folders, the other crates and the `OXIGUITAR_*` variables keep OxiGuitar's names.
- **No "OxiGuitar is playing with your system's basic sound set" dialog**: FuTab hides the MIDI plugin's (`oxiguitar.midi`) basic-sounds advice from the start, since its text names OxiGuitar. The plugin's footer messages are unchanged.

### Fixed

- **Upstream history up to OxiGuitar PR 290**: the merge of OxiGuitar #286 to #290 (#7) was squash-merged, which dropped upstream's commits from FuTab's history, so the catch-up report listed them as missing again and the next merge would have conflicted on them. A merge that changes no file links them back in.
- **Linux packages build again** (#12): the .deb packages' description had a line over 80 characters, which Debian's package checker (Lintian) rejects, so the Linux package builds failed. The description is rewrapped; its text is unchanged.

### Removed

- **OxiGuitar's repository tools**: `scripts/new-repo.sh` and `scripts/split-history.sh`, which made and filled plugin repositories under `mateusrdp`, are gone. The workspace's `repository` and `homepage`, and the AppStream screenshots, now point at `PurpleIcon/futab`.
