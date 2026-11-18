## Which file do I need?

One download for your system. FuTab is a fork of [OxiGuitar](https://github.com/mateusrdp/oxiguitar). **None of these carries plugins**: FuTab uses OxiGuitar's plugins, which open Guitar Pro files and play them and have releases and packages of their own ([oxiguitar-guitarpro](https://github.com/mateusrdp/oxiguitar-guitarpro), [oxiguitar-midi](https://github.com/mateusrdp/oxiguitar-midi) and the others). On Linux, install them from OxiGuitar's package repositories (the plugin packages only, never the `oxiguitar` package itself); on Windows, put each plugin's `.oxp` file in FuTab's plugin folder (OxiGuitar's plugin installers use OxiGuitar's own folder, which FuTab doesn't look in). FuTab's [README](https://github.com/PurpleIcon/futab#install) explains how. None of the files is code-signed, so Windows warns the first time it runs.

**No macOS download yet**: GitHub's macOS build machines were too busy to build it reliably. On a Mac, build FuTab from source ([README](https://github.com/PurpleIcon/futab#building-from-source)).

| System | Download |
| --- | --- |
| Windows 10 and 11 (x86_64) | `FuTab-@VERSION@-windows-x86_64.zip` |
| Windows on ARM | `FuTab-@VERSION@-windows-arm64.zip` |
| Any Linux (x86_64; `aarch64` for ARM) | `FuTab-@VERSION@-x86_64.AppImage`, for Wayland and X11 desktops alike |
| Debian, Ubuntu (x86_64; `arm64` for ARM) | `futab_@VERSION@_amd64.deb` |
| Fedora (x86_64; `aarch64` for ARM) | `futab-@VERSION@-1.x86_64.rpm` |
| Any Linux, as a Flatpak (x86_64; `aarch64` for ARM) | `FuTab-@VERSION@-x86_64.flatpak` |

**The Flatpak** takes OxiGuitar's plugins from OxiGuitar's Flatpak repository, as Flatpak extensions: at least Guitar Pro, MIDI and PipeWire. It sees only its own folders, so it plays once a sound set is in its `soundfonts` folder. The [Linux install page](https://purpleicon.github.io/futab/install-linux.html#flatpak) explains how.

The .deb and .rpm above are the Wayland build; a Linux desktop without Wayland takes the files named `futab-x11` instead. SHA256SUMS holds every file's checksum.
