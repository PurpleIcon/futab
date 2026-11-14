# FuTab

<p align="center"><img src="assets/icon/futab.svg" alt="FuTab icon: a guitar plectrum split in two, with a music note in each half" width="96"></p>

> **Work in progress.** FuTab is being set up as a project of its own: there are no releases or packages yet, and things will change. To try it now, [build it from source](#building-from-source).

**FuTab** is a Free, Open-Source fully modular guitar tablature and score viewer, editor and player for Windows, macOS and Linux.

FuTab is a fork of [OxiGuitar](https://github.com/mateusrdp/oxiguitar), created by Mateus Rocha de Paula ([@mateusrdp](https://github.com/mateusrdp)) and the OxiGuitar contributors. Nearly all of what FuTab does is their work, and FuTab uses OxiGuitar's plugins as they are. Thank you to them.

It is written entirely in Rust. 

It opens the industry’s usual files (Guitar Pro 3 to 8, MusicXML, MIDI and TuxGuitar files), because no one wants to have to rewrite their entire tab collection. It shows them as standard notation and tablature and allows you to play, edit and save them. Every input/output format is a plugin, so you can write your own if we still don’t support what you need.

Playback is also big. The most basic is a MIDI synthesizer that plays whatever sound fonts your computer already has (Windows and macOS come with one; on Linux there is an plugin). But we REALLY recommend that you get yourself some better ones – it makes a massive difference. We do have a few suggestions of nice free ones, with instructions on how to download, install and use them with FuTab. 

## Privacy

FuTab values your privacy first. It never uploads anything. No telemetry, no analytics, no automatic crash reports, no accounts, no background requests — not a single bit of data. It downloads nothing either: better sounds and plugins are files you get yourself and put in a folder, and the manual says where. The only network use ever planned is an update check you start yourself. If it crashes, it writes a log to your disk and tells you where it is; sending it to us is up to you. A CI test even runs FuTab under a system-call tracer and fails if it ever tries to open a network connection to keep us honest. We don’t collect your data EVER. 

These promises cover FuTab itself and nothing else: we make no promises about plugins you get from anywhere else.  Please refer to OxiGuitar for their Privacy statement on Oxiguitar Plugins you use. FuTab is fully modular, open-source and encourages the community to collaborate! **Anyone** can write plugins for it! **Be careful where you get your plugins from!** It’s **your** responsibility to check.

## Install

FuTab doesn't publish packages yet. Until it does, build it from source (see [Building from source](#building-from-source)).

FuTab is the program plus **plugins**: it opens, plays and exports files only through them. It uses OxiGuitar's plugins, as they are, and finds them where OxiGuitar's packages install them. A usable set is the **Guitar Pro** and **MIDI** plugins and an audio output; **WAV** (export your song as audio), **NAM** (amp models) and **Equalizer** are extras.

On Debian, Ubuntu and relatives, add OxiGuitar's signed repository once, then install the plugins only:

```sh
sudo install -d -m 0755 /etc/apt/keyrings
sudo curl -fsSL https://mateusrdp.github.io/oxiguitar-packages/oxiguitar.gpg -o /etc/apt/keyrings/oxiguitar.gpg
sudo curl -fsSL https://mateusrdp.github.io/oxiguitar-packages/oxiguitar.sources -o /etc/apt/sources.list.d/oxiguitar.sources
sudo apt update
sudo apt install oxiguitar-guitarpro oxiguitar-midi oxiguitar-pipewire oxiguitar-wav oxiguitar-nam oxiguitar-eq
```

On Fedora and relatives:

```sh
sudo curl -fsSL https://mateusrdp.github.io/oxiguitar-packages/oxiguitar.repo -o /etc/yum.repos.d/oxiguitar.repo
sudo dnf install oxiguitar-guitarpro oxiguitar-midi oxiguitar-pipewire oxiguitar-wav oxiguitar-nam oxiguitar-eq
```

Install only the plugin packages, never the `oxiguitar` package itself, or you get OxiGuitar alongside FuTab. The plugins and their repository are OxiGuitar's, signed with its maintainer's key; report problems you meet through FuTab [here](https://github.com/PurpleIcon/futab/issues) first. Elsewhere, download each plugin from its own repository's latest release (for example [Guitar Pro](https://github.com/mateusrdp/oxiguitar-guitarpro/releases/latest)) and put its `.oxp` file in your own plugin folder (`~/.local/share/futab/plugins/` on Linux).

### After installing

Open a song. FuTab plays each kind of track with the matching recorded set by itself (clean, overdriven and distorted guitars, nylon and steel strings, bass, drums); **Tools → Plugins…** lists the plugins it found and **Settings…** on MIDI changes the sets. OxiGuitar's [manual](https://mateusrdp.github.io/oxiguitar/) says more (FuTab works the same way; it has no manual of its own yet), and its [Better sounds](https://mateusrdp.github.io/oxiguitar/better-sounds.html) page lists the sets.

## How to get involved

FuTab is a young project, and every bit of help counts, whether you play, code, or both.

- **Come and say hello** in [Discussions](https://github.com/PurpleIcon/futab/discussions): share what you think, ask questions, suggest ideas, or tell us what you play with it.
- **Report bugs** in [Issues](https://github.com/PurpleIcon/futab/issues) when something doesn't work the way you expect.
- **Try it on your system.** If you use Windows, macOS, an ARM machine or a Linux other than Fedora, your testing is especially welcome (see [Testers wanted](#testers-wanted)).
- **Contribute code or documentation.** Pull requests are welcome: [CONTRIBUTING.md](CONTRIBUTING.md) explains how.

# Technical Section

## Supported systems

| System | Versions | CPUs |
| --- | --- | --- |
| Windows | 10 and later | x86\_64, ARM64 |
| Linux | the AppImage: distributions with glibc 2.35 or newer (Debian 12 and later, Ubuntu 22.04+, Fedora 36+); the .deb and .rpm: glibc 2.39 or newer (Debian trixie and sid, Ubuntu 24.04+, Fedora 40+) | x86\_64, ARM64 |
| macOS | the current release | Apple Silicon and Intel (one universal app) |

FuTab doesn't publish releases yet: build it from source (see [Install](#install)). When it does, it will offer the same downloads as OxiGuitar: a portable .exe for Windows (in a zip), an AppImage for any Linux, a .deb and an .rpm, and a .dmg for macOS. None will carry the plugins, which are OxiGuitar's and have releases, packages and updates of their own ([oxiguitar-guitarpro](https://github.com/mateusrdp/oxiguitar-guitarpro), [oxiguitar-midi](https://github.com/mateusrdp/oxiguitar-midi), [oxiguitar-nam](https://github.com/mateusrdp/oxiguitar-nam), [oxiguitar-wav](https://github.com/mateusrdp/oxiguitar-wav) and the audio outputs).

On Linux, the Wayland build is the default; a desktop with only an X server needs the X11 build (see [Building from source](#building-from-source)). The X11 build is deprecated and will be dropped.

## Building from source

You need Rust 1.99 or newer, from [rustup](https://rustup.rs): distributions' own Rust packages are usually older. On Debian and Ubuntu:

```
sudo apt install git build-essential pkg-config rustup \
  libfontconfig1-dev libxkbcommon-dev libwayland-dev \
  libasound2-dev libpipewire-0.3-dev libclang-dev
rustup default stable
git clone https://github.com/PurpleIcon/futab.git
cd futab
cargo build --release
cargo test
```

Elsewhere, install rustup from your system's packages or from [rustup.rs](https://rustup.rs). The `lib…-dev` packages are the system libraries FuTab needs: fontconfig, xkbcommon and Wayland for fonts, keyboard and windows, and ALSA and PipeWire (with libclang, which builds PipeWire's bindings) for the audio-device plugins.

The program opens files only through format plugins (one per format, `.oxp` files), which are built from the plugin repositories ([oxiguitar-guitarpro](https://github.com/mateusrdp/oxiguitar-guitarpro) and the others; each has a `build-oxp.sh`). A build from source looks for them in `target/lib/futab/plugins/` beside the program on Linux (then in OxiGuitar's system plugin folders), in `plugins\` beside the .exe on Windows, and in your own plugin folder everywhere; `cargo test` takes the latest releases of the plugins it needs by itself (`OXIGUITAR_PLUGINS_DIR` points it at a folder of your own builds instead).

Run the desktop app, optionally with a file to open:

```
cargo run --release -p oxiguitar-app -- path/to/your/song.gp
```

That is the Wayland build, the default. On a desktop with only an X server, build the X11 one instead: `cargo run --release -p oxiguitar-app --no-default-features --features x11 -- song.gp`. Each build carries only its own display system's code, and says which build you need if it can't find its session.

File → New starts a score; OxiGuitar's manual pages [Editing](https://mateusrdp.github.io/oxiguitar/editing.html) and [Keyboard and mouse](https://mateusrdp.github.io/oxiguitar/keys.html) list the keys, which are the same in FuTab. On Linux, the Open and Export dialogs come from the desktop portal (`xdg-desktop-portal` with your desktop's backend, installed by default with GNOME and KDE). The binary is `target/release/oxiguitar`; it finds the plugins in `target/lib/futab/plugins/`, in OxiGuitar's system plugin folders, and in your own plugin folder (`~/.local/share/futab/plugins/` on Linux; OxiGuitar's manual page [Settings and plugins](https://mateusrdp.github.io/oxiguitar/plugins.html) explains the folders, which FuTab names `futab` instead). On Wayland, desktops take an app's icon from its desktop entry rather than from the window; to give a build from source (or an AppImage) its icon, a menu entry and the Guitar Pro file types, run `scripts/install-desktop-entry.sh [path to the program]` (it writes only to `~/.local/share`; `--uninstall` removes it).

Try the command-line tool, which reads files through the same plugins (Guitar Pro 3 to 8: .gp3, .gp4, .gp5, .gpx, .gp) and engraves them into PNG pages and a PDF:

```
cargo run --release -p oxiguitar-cli -- info fixtures/gp/oxiguitar-test-song.gp
cargo run --release -p oxiguitar-cli -- info --bars path/to/your/song.gp5
cargo run --release -p oxiguitar-cli -- render path/to/your/song.gp --png page --pdf song.pdf
cargo run --release -p oxiguitar-cli -- render path/to/your/song.gp --tracks all --dark --pdf song-dark.pdf
cargo run --release -p oxiguitar-cli -- render path/to/your/song.gp --tool infer-key-signatures --no-dynamics --pdf keys.pdf
cargo run --release -p oxiguitar-cli -- convert path/to/your/song.gp3 song.gp
cargo run --release -p oxiguitar-cli -- play path/to/your/song.gp --wav song.wav
```

## Writing plugins

Every file format, tool and tab in FuTab is a plugin: one `.oxp` file, a native library with a small manifest, built from Rust with the SDK in this repository. FuTab keeps OxiGuitar's plugin interface, so a plugin works in both. OxiGuitar's [plugin developer guide](https://mateusrdp.github.io/oxiguitar/plugin-guide/) walks through it from its template (`docs/plugins/template/`), and plugins may use any GPL-compatible license, since the interface and the SDK are MIT OR Apache-2.0.

## Testers wanted

The maintainer tests by hand on x86\_64 Fedora only. Everything else — **Windows, macOS, other Linux distributions, and any ARM64 machine** — is built and tested automatically, but nobody has clicked through FuTab there yet. If you can try test builds on one of those systems, please say hello in [Discussions](https://github.com/PurpleIcon/futab/discussions) or [open an issue](https://github.com/PurpleIcon/futab/issues) with what you find.

Test builds of every change on `develop` (the program for each system, its plugins, and the songs we write as .gp and .gp5 for checking in Guitar Pro) are under the [Actions](https://github.com/PurpleIcon/futab/actions/workflows/builds.yml) tab, kept for 14 days (you need to be signed in to GitHub to download them). FuTab doesn't publish packages yet.

## Contributing

Pull requests are welcome from day one. Read [CONTRIBUTING.md](CONTRIBUTING.md) first: it covers code standards, the sign-off rule and how to add a file format or an effect. [ARCHITECTURE.md](ARCHITECTURE.md) explains how the code fits together, and [docs/adr/](docs/adr/) records why things are the way they are.

## License

FuTab is free software under the [GNU General Public License, version 3](LICENSE). It is a fork of [OxiGuitar](https://github.com/mateusrdp/oxiguitar), under the same license. Our own code is GPL-3.0-or-later; the program as distributed is GPL-3.0, because code ported from MuseScore keeps its GPL-3.0-only license. The plugin interface and the SDK for plugin authors (`oxiguitar-plugin-api`, `oxiguitar-plugin`) are MIT OR Apache-2.0, so plugins may use any GPL-compatible license.

Copyright (C) 2026 Mateus Rocha de Paula and the OxiGuitar contributors.\
Copyright (C) 2026 The FuTab contributors.

[CREDITS.md](CREDITS.md) lists every project we build on and thanks everyone who has contributed.

Guitar Pro is a trademark of Arobas Music. MuseScore is a trademark of Muse Group. FuTab is not affiliated with either, nor with the OxiGuitar project, whose name it uses only to say where FuTab comes from.
