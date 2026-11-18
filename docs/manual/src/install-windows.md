# Installing on Windows

Download `FuTab-VERSION-windows-x86_64.zip` (or `arm64`) from the [latest release](https://github.com/PurpleIcon/futab/releases/latest), unzip it anywhere and run `futab.exe`. It isn't signed: on SmartScreen's warning choose **More info → Run anyway**. Then install the plugins, below. To build it yourself instead, see [Installing](installing.md).

Plugins are files ending in `.oxp`. FuTab looks for them in the `plugins` folder beside `futab.exe`, in `C:\Program Files\FuTab\plugins` and `C:\Program Files\OxiGuitar\plugins`, and in your own folder, `%APPDATA%\FuTab\plugins`. **Help → About** lists every folder it searches, and **Tools → Plugins…** every plugin it found. [The official plugins](official-plugins.md) says what each does.

## Plugins

FuTab uses OxiGuitar's plugins. Each plugin's releases page (linked from [the official plugins](official-plugins.md)) has a zip for your processor, x86_64 or ARM64:

1. Download the plugin's zip.
2. Unzip it and put the `.oxp` file in `%APPDATA%\FuTab\plugins` (paste that into File Explorer's address bar; create the folder if it isn't there).
3. Start FuTab again. **Tools → Plugins…** lists it.

**You need at least** the Guitar Pro plugin, the MIDI plugin and the WASAPI plugin (the one that sends sound to your speakers). Updates are by hand: download the newer zip and replace the file.

The plugins' setup programs (`oxiguitar-NAME-VERSION-windows-x86_64-setup.exe`) install into OxiGuitar's own folder, `%APPDATA%\OxiGuitar\plugins`, which FuTab doesn't search. If you used one, copy the `.oxp` files from there into `%APPDATA%\FuTab\plugins`.

## The recorded sound sets

The sound-set installer's releases page has `install.ps1`, a PowerShell script that lists what it would download, from where and under which licence, and asks before it fetches anything ([Better sounds](better-sounds.md#the-sound-set-installer)). FuTab itself never downloads anything.

If a plugin is missing, FuTab says so once when it starts and links here.
