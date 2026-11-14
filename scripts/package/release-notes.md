## Which file do I need?

One download for your system. FuTab is a fork of [OxiGuitar](https://github.com/mateusrdp/oxiguitar). **None of these carries plugins**: FuTab uses OxiGuitar's plugins, which open Guitar Pro files and play them and have releases and packages of their own ([oxiguitar-guitarpro](https://github.com/mateusrdp/oxiguitar-guitarpro), [oxiguitar-midi](https://github.com/mateusrdp/oxiguitar-midi) and the others). On Linux, install them from OxiGuitar's package repositories (the plugin packages only, never the `oxiguitar` package itself); on Windows and macOS each plugin has an installer. FuTab's [README](https://github.com/PurpleIcon/futab#install) explains how.

| System | Download |
| --- | --- |
| Windows 10 and 11 (x86_64) | `FuTab-@VERSION@-windows-x86_64.zip` |
| Windows on ARM | `FuTab-@VERSION@-windows-arm64.zip` |
| macOS (Apple Silicon and Intel) | `FuTab-@VERSION@-macos-universal.dmg` |
| Any Linux (x86_64; `aarch64` for ARM) | `FuTab-@VERSION@-x86_64.AppImage`, for Wayland and X11 desktops alike |
| Debian, Ubuntu (x86_64; `arm64` for ARM) | `futab_@VERSION@_amd64.deb` |
| Fedora (x86_64; `aarch64` for ARM) | `futab-@VERSION@-1.x86_64.rpm` |
| Any Linux, as a Flatpak (x86_64; `aarch64` for ARM) | `FuTab-@VERSION@-x86_64.flatpak` |

The .deb and .rpm above are the Wayland build; a Linux desktop without Wayland takes the files named `futab-x11` instead. SHA256SUMS holds every file's checksum.
