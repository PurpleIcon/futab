# Installing on Linux

FuTab has no Linux packages yet: build it from source ([Installing](installing.md)). This page is about where plugins go, and how to get them.

Plugins are files ending in `.oxp`. FuTab looks for them in its own folders first (`lib/futab/plugins` beside the program, `/usr/lib/futab/plugins`, `/usr/local/lib/futab/plugins`), then in OxiGuitar's (`lib/oxiguitar/plugins` beside the program, `/usr/lib/oxiguitar/plugins`, `/usr/local/lib/oxiguitar/plugins`), and last in your own folder, `~/.local/share/futab/plugins/`. **Help → About** lists every folder it searches, and **Tools → Plugins…** every plugin it found. [The official plugins](official-plugins.md) says what each does.

## From OxiGuitar's apt repository (Debian, Ubuntu and relatives)

The plugins are OxiGuitar's packages (`oxiguitar-guitarpro`, `oxiguitar-midi`, `oxiguitar-nam`, and so on), kept in OxiGuitar's signed repository on GitHub Pages. Add it once, then install the plugins only:

```sh
sudo install -d -m 0755 /etc/apt/keyrings
sudo curl -fsSL https://mateusrdp.github.io/oxiguitar-packages/oxiguitar.gpg -o /etc/apt/keyrings/oxiguitar.gpg
sudo curl -fsSL https://mateusrdp.github.io/oxiguitar-packages/oxiguitar.sources -o /etc/apt/sources.list.d/oxiguitar.sources
sudo apt update
sudo apt install oxiguitar-guitarpro oxiguitar-midi oxiguitar-pipewire oxiguitar-alsa
```

Add `oxiguitar-nam` for amp models, `oxiguitar-eq` for an equalizer, and `oxiguitar-musicxml`, `oxiguitar-midi-file` and `oxiguitar-tuxguitar` to open and save MusicXML, MIDI and TuxGuitar files. **Never install the `oxiguitar` package itself**, or you get OxiGuitar beside FuTab. `sudo apt upgrade` then keeps the plugins current. They install into `/usr/lib/oxiguitar/plugins`, where FuTab finds them. The repository and its key are OxiGuitar's; its fingerprint is on the [repository's page](https://github.com/mateusrdp/oxiguitar-packages). Report problems you meet through FuTab to [FuTab](https://github.com/PurpleIcon/futab/issues) first.

## From OxiGuitar's dnf repository (Fedora and relatives)

The same repository serves dnf, signed the same way:

```sh
sudo curl -fsSL https://mateusrdp.github.io/oxiguitar-packages/oxiguitar.repo -o /etc/yum.repos.d/oxiguitar.repo
sudo dnf install oxiguitar-guitarpro oxiguitar-midi oxiguitar-pipewire oxiguitar-alsa
```

`sudo dnf upgrade` keeps them current. Again, install the plugins only, never `oxiguitar`.

## The recorded sound sets

`oxiguitar-midi` suggests `oxiguitar-bettersounds-soundfonts`, the installer of the free recorded sound sets OxiGuitar recommends (about 1.2 GB; [Better sounds](better-sounds.md#the-sound-set-installer)). Installing it downloads the sets into `/usr/share/oxiguitar/soundfonts`, where the MIDI plugin looks and uses them by itself: with apt it asks first (yes is the default, so an unattended install downloads them), with dnf it just does. If you say no, or a download fails, `sudo oxiguitar-install-sounds --system` chooses and downloads them any time later. FuTab itself never downloads anything.

## By hand

Without the repositories, each plugin's releases page (linked from [the official plugins](official-plugins.md)) has a Linux zip for your processor, x86_64 or ARM64:

1. Download the plugin's zip.
2. Unzip it and put the `.oxp` file in `~/.local/share/futab/plugins/`.
3. Start FuTab again. **Tools → Plugins…** lists it.

You need the essential ones: a plugin that reads Guitar Pro files, the MIDI plugin, and an audio output (PipeWire on most desktops, ALSA otherwise). Plugins added this way are updated by hand: download the newer zip and replace the file.

If a plugin is missing, FuTab says so once when it starts and links here.
