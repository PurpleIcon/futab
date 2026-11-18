# Installing on Linux

Install FuTab first, then OxiGuitar's plugins: FuTab opens, plays and exports files only through them.

## 1. Install FuTab

Download FuTab for your processor (x86_64 or ARM64) from the [latest release](https://github.com/PurpleIcon/futab/releases/latest), then install it:

| System | Install |
| --- | --- |
| Fedora and relatives | `sudo dnf install ./futab-VERSION-1.x86_64.rpm` |
| Debian, Ubuntu and relatives | `sudo apt install ./futab_VERSION_amd64.deb` |
| Any Linux | Make the AppImage executable (`chmod +x FuTab-VERSION-x86_64.AppImage`) and run it |
| Any Linux, as a Flatpak | `flatpak install --user ./FuTab-VERSION-x86_64.flatpak`, then its plugins and a sound set: see [Flatpak](#flatpak) below |

On a desktop without Wayland, take the `futab-x11` .deb or .rpm instead. FuTab installs beside OxiGuitar without sharing a file or a setting with it. To build it yourself instead, see [Installing](installing.md).

## 2. Install the plugins

Plugins are files ending in `.oxp`. FuTab looks for them in its own folders first (`lib/futab/plugins` beside the program, `/usr/lib/futab/plugins`, `/usr/local/lib/futab/plugins`), then in OxiGuitar's (`lib/oxiguitar/plugins` beside the program, `/usr/lib/oxiguitar/plugins`, `/usr/local/lib/oxiguitar/plugins`), and last in your own folder, `~/.local/share/futab/plugins/`. **Help → About** lists every folder it searches, and **Tools → Plugins…** every plugin it found. [The official plugins](official-plugins.md) says what each does.

### From OxiGuitar's apt repository (Debian, Ubuntu and relatives)

The plugins are OxiGuitar's packages (`oxiguitar-guitarpro`, `oxiguitar-midi`, `oxiguitar-nam`, and so on), kept in OxiGuitar's signed repository on GitHub Pages. Add it once, then install the plugins only:

```sh
sudo install -d -m 0755 /etc/apt/keyrings
sudo curl -fsSL https://mateusrdp.github.io/oxiguitar-packages/oxiguitar.gpg -o /etc/apt/keyrings/oxiguitar.gpg
sudo curl -fsSL https://mateusrdp.github.io/oxiguitar-packages/oxiguitar.sources -o /etc/apt/sources.list.d/oxiguitar.sources
sudo apt update
sudo apt install oxiguitar-guitarpro oxiguitar-midi oxiguitar-pipewire oxiguitar-alsa
```

Add `oxiguitar-nam` for amp models, `oxiguitar-eq` for an equalizer, `oxiguitar-wah` for a wah-wah pedal, and `oxiguitar-musicxml`, `oxiguitar-midi-file` and `oxiguitar-tuxguitar` to open and save MusicXML, MIDI and TuxGuitar files. **Never install the `oxiguitar` package itself**, or you get OxiGuitar beside FuTab. `sudo apt upgrade` then keeps the plugins current. They install into `/usr/lib/oxiguitar/plugins`, where FuTab finds them. The repository and its key are OxiGuitar's; its fingerprint is on the [repository's page](https://github.com/mateusrdp/oxiguitar-packages). Report problems you meet through FuTab to [FuTab](https://github.com/PurpleIcon/futab/issues) first.

### From OxiGuitar's dnf repository (Fedora and relatives)

The same repository serves dnf, signed the same way:

```sh
sudo curl -fsSL https://mateusrdp.github.io/oxiguitar-packages/oxiguitar.repo -o /etc/yum.repos.d/oxiguitar.repo
sudo dnf install oxiguitar-guitarpro oxiguitar-midi oxiguitar-pipewire oxiguitar-alsa
```

`sudo dnf upgrade` keeps them current. Again, install the plugins only, never `oxiguitar`.

FuTab's .deb and .rpm recommend the Guitar Pro, MIDI, ALSA and PipeWire plugins: add the repository before installing FuTab, and apt or dnf installs them with it.

### Flatpak

FuTab's Flatpak takes OxiGuitar's plugins as Flatpak packages, from OxiGuitar's signed Flatpak repository, with Flathub for the runtime they run on. Add both once, then install the plugins, in the same installation as FuTab (`--user` for both, or for neither):

```sh
flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak remote-add --user --if-not-exists oxiguitar https://mateusrdp.github.io/oxiguitar-packages/flatpak/oxiguitar.flatpakrepo
flatpak install --user oxiguitar io.github.mateusrdp.OxiGuitar.Plugin.guitarpro io.github.mateusrdp.OxiGuitar.Plugin.midi io.github.mateusrdp.OxiGuitar.Plugin.pipewire
```

Each plugin is named `io.github.mateusrdp.OxiGuitar.Plugin.` and the plugin's short name: `guitarpro`, `midi`, `alsa`, `pipewire`, `nam`, `eq`, `wah`, `wav`, `musicxml`, `midi-file`, `tuxguitar`. Take at least `guitarpro`, `midi` and an audio output (`pipewire` on most desktops, `alsa` otherwise). **Never install `io.github.mateusrdp.OxiGuitar` itself**, or you get OxiGuitar beside FuTab. `flatpak update` keeps the plugins current.

The Flatpak sees only the files you open in its dialogs and its own folders, not your system's or OxiGuitar's. Create a folder if it isn't there yet:

| Folder | What goes in it |
| --- | --- |
| `~/.var/app/io.github.purpleicon.FuTab/data/futab/plugins/` | Plugin files (`.oxp`) that are not Flatpak packages |
| `~/.var/app/io.github.purpleicon.FuTab/data/futab/soundfonts/` | Sound sets |
| `~/.var/app/io.github.purpleicon.FuTab/data/futab/nam/` | Amp models and cabinets ([Amp models (NAM)](amp-models.md)) |

**It plays nothing until it has a sound set there**: the MIDI plugin says "no sound set found" until then. Run the sound-set installer into that folder ([Better sounds](better-sounds.md#the-sound-set-installer)):

```sh
bash install.sh --dir ~/.var/app/io.github.purpleicon.FuTab/data/futab/soundfonts
```

or copy a set you have there, such as Fedora's General MIDI set: `cp /usr/share/soundfonts/FluidR3_GM.sf2 ~/.var/app/io.github.purpleicon.FuTab/data/futab/soundfonts/`.

### The recorded sound sets

`oxiguitar-midi` suggests `oxiguitar-bettersounds-soundfonts`, the installer of the free recorded sound sets OxiGuitar recommends (about 1.2 GB; [Better sounds](better-sounds.md#the-sound-set-installer)). Installing it downloads the sets into `/usr/share/oxiguitar/soundfonts`, where the MIDI plugin looks and uses them by itself: with apt it asks first (yes is the default, so an unattended install downloads them), with dnf it just does. If you say no, or a download fails, `sudo oxiguitar-install-sounds --system` chooses and downloads them any time later. FuTab itself never downloads anything.

### By hand (and with the AppImage)

Without the repositories, and with the AppImage, each plugin's releases page (linked from [the official plugins](official-plugins.md)) has a Linux zip for your processor, x86_64 or ARM64:

1. Download the plugin's zip.
2. Unzip it and put the `.oxp` file in `~/.local/share/futab/plugins/`.
3. Start FuTab again. **Tools → Plugins…** lists it.

You need the essential ones: a plugin that reads Guitar Pro files, the MIDI plugin, and an audio output (PipeWire on most desktops, ALSA otherwise). Plugins added this way are updated by hand: download the newer zip and replace the file.

If a plugin is missing, FuTab says so once when it starts and links here.
