# Installing and sharing

Installing a plugin means putting its `.oxp` file in a plugin folder; removing it means deleting the file. Nothing is unpacked or registered, and FuTab itself never downloads, copies or removes plugins.

## Where users put the file

Each user has a plugin folder, which FuTab creates the first time it starts:

| System | The user's plugin folder |
| --- | --- |
| Linux | `~/.local/share/futab/plugins/` (`$XDG_DATA_HOME/futab/plugins/` when that is set) |
| macOS | `~/Library/Application Support/FuTab/plugins/` |
| Windows | `%APPDATA%\FuTab\plugins\` |

FuTab also searches the system's plugin folders, where packages install plugins for every user: FuTab's first, then OxiGuitar's, since FuTab keeps OxiGuitar's plugin interface and a plugin works in both:

| System | The program's plugin folder |
| --- | --- |
| Linux | `<bin>/../lib/futab/plugins/` (beside the program), `/usr/lib/futab/plugins/`, `/usr/local/lib/futab/plugins/`, then `<bin>/../lib/oxiguitar/plugins/`, `/usr/lib/oxiguitar/plugins/`, `/usr/local/lib/oxiguitar/plugins/` |
| macOS | `FuTab.app/Contents/PlugIns/`, then `/Library/Application Support/FuTab/plugins/` and `/Library/Application Support/OxiGuitar/plugins/` |
| Windows | `plugins\` beside `futab.exe`, then `C:\Program Files\FuTab\plugins\` and `C:\Program Files\OxiGuitar\plugins\` |

The system's folders are searched first, then the user's. Help → About lists every folder in the order searched. A `plugin_folders` list in settings.json replaces the defaults, and `OXIGUITAR_HOME` puts settings.json and `plugins/` in one folder (for tests and portable copies).

Only `.oxp` files directly in a folder count, not in subfolders. The file's name doesn't matter, but keep it recognisable: `example.oxp`, or the download's own name, `example-0.1.0-linux-x86_64.oxp`.

## What FuTab does with it

At the next start, FuTab reads the file's manifest and lists it in **Tools → Plugins**, with a tickbox to enable or disable it from the next start (it writes the plugin's id under `disabled` in settings.json). The plugin is loaded the first time one of its contributions is used.

When two files carry the same plugin `id`, the higher version is used and the other is listed as replaced; on a tie, the build needing more of the processor's features (the `cpu` condition), then the file in the later folder, then the earlier name in one folder. So a user who installs your new version beside an old one gets the new one, and a user's own copy wins over a package's of the same version.

A file that can't be used is listed with the reason: another system's or processor's file, a damaged file, a manifest problem, an interface newer than this FuTab has, or conditions that don't hold here.

## macOS: the download mark

macOS marks downloaded files, and refuses to load an unsigned library that carries the mark ("cannot be opened because the developer cannot be verified"). FuTab's own plugins aren't signed either; the user manual tells users to clear the mark:

```sh
xattr -d com.apple.quarantine ~/Library/Application\ Support/FuTab/plugins/example.oxp
```

Say the same in your README, or sign and notarise your file with an Apple Developer ID.

## What to tell your users

- What the plugin adds, and which FuTab it needs: 0.2 or later.
- Which file is for which system, and where to put it (the table above).
- **What it does beyond FuTab.** A plugin is native code with the user's rights; FuTab's promises (no telemetry, never upload, never download) cover the app and our own plugins, not yours. If your plugin never touches the network, say so; if it does, say when and why.
- Its licence. The SDK is MIT OR Apache-2.0, so any GPL-compatible licence works.
- Where to report its bugs. When FuTab refuses a file your plugin's extension names, it suggests reporting a bug at FuTab's tracker; we will point people to you, but a line in your README saves them the trip.

## Sharing it

Host it wherever you like: a GitHub release (the template's workflow makes one), your own site, a package for your Linux distribution installing into `/usr/lib/oxiguitar/plugins/`. FuTab names no plugin source of its own beyond its footer's pointer to OxiGuitar's releases page when nothing can be opened. If you'd like your plugin mentioned in FuTab's documentation, open an issue.
