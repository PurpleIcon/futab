# Changelog

All notable changes to FuTab. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [Semantic Versioning](https://semver.org/).

FuTab is a fork of [OxiGuitar](https://github.com/mateusrdp/oxiguitar), taken from OxiGuitar 0.19.1 on 13 Nov 2026. This file lists only FuTab's own changes; OxiGuitar's are in [its changelog](https://github.com/mateusrdp/oxiguitar/blob/develop/CHANGELOG.md).

## [Unreleased]

### Added

- **Upstream catch-up report**: `python3 -I scripts/upstream/catchup.py` writes `oxiguitar-catchup.md` (gitignored): the OxiGuitar releases and commits FuTab hasn't merged yet, each with its upstream pull request, and the files a catch-up merge would conflict in. The Upstream workflow runs it every Monday and by hand, and shows it in the run's summary. It holds while FuTab catches up by merging `upstream/develop`, not by cherry-picking.

### Changed

- **FuTab's own design notes and decision records**: `docs/futab-design/` and `docs/futab-adr/` (numbered from 0001, with its own template) hold FuTab's; `docs/design/` and `docs/adr/` stay OxiGuitar's, merged from upstream and not edited. CONTRIBUTING.md, the agent rules and the merge-upstream skill say so.
- **FuTab**: this fork of OxiGuitar is now called FuTab in the app: window title, About box (which credits OxiGuitar), messages, desktop entry, AppStream metainfo and macOS bundle name. FuTab has its own icon (a plectrum split in two, with a note in each half) in place of the green placeholder pick. The PayPal donation button, QR code and README section are removed. The app ID is `io.github.purpleicon.FuTab`. Settings live in FuTab's own folders (`~/.config/futab`, `~/.local/share/futab`, `~/.cache/futab`; `FuTab` on macOS and Windows), so FuTab never touches an installed OxiGuitar's settings. Plugins are found in FuTab's folders first and then in OxiGuitar's (`/usr/lib/oxiguitar/plugins` and the others), so OxiGuitar's plugin packages work in FuTab. Bug reports go to `PurpleIcon/futab`. The programs are `futab`, `futab-x11` and `futab-cli` (`cargo run -p futab`, `cargo run -p futab-cli`), and the packages `futab` and `futab-x11` (.deb and .rpm), `FuTab-…AppImage`, `FuTab-…flatpak`, `FuTab-…windows-….zip` and `FuTab-…macos-universal.dmg`, with their own man pages, launcher and library folder, so FuTab installs beside OxiGuitar without a file in common. The crates' folders, the other crates and the `OXIGUITAR_*` variables keep OxiGuitar's names.
- **No "OxiGuitar is playing with your system's basic sound set" dialog**: FuTab hides the MIDI plugin's (`oxiguitar.midi`) basic-sounds advice from the start, since its text names OxiGuitar. The plugin's footer messages are unchanged.

### Removed

- **OxiGuitar's repository tools**: `scripts/new-repo.sh` and `scripts/split-history.sh`, which made and filled plugin repositories under `mateusrdp`, are gone. The workspace's `repository` and `homepage`, and the AppStream screenshots, now point at `PurpleIcon/futab`.
