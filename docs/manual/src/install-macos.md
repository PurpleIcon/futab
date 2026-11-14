# Installing on macOS

FuTab has no macOS download yet: build it from source ([Installing](installing.md)). It runs on Intel and Apple silicon. This page is about plugins.

Plugins are files ending in `.oxp`. FuTab looks for them in `/Library/Application Support/FuTab/plugins` and `/Library/Application Support/OxiGuitar/plugins`, and in your own folder, `~/Library/Application Support/FuTab/plugins`. **Help → About** lists every folder it searches, and **Tools → Plugins…** every plugin it found. [The official plugins](official-plugins.md) says what each does.

## Plugins

FuTab uses OxiGuitar's plugins, which come as an installer (.pkg) for each plugin, from its releases page. The installers put the plugin in OxiGuitar's own folder, `~/Library/Application Support/OxiGuitar/plugins`, which FuTab doesn't search, so after installing, copy the plugins into FuTab's folder:

```sh
mkdir -p ~/Library/Application\ Support/FuTab/plugins
cp ~/Library/Application\ Support/OxiGuitar/plugins/*.oxp ~/Library/Application\ Support/FuTab/plugins/
```

You need at least the Guitar Pro plugin, the MIDI plugin and the Core Audio plugin (the one that sends sound to your speakers).

For the free recorded sound sets OxiGuitar recommends, the sound-set installer's releases page has `install.sh`: run it in Terminal (`bash install.sh`); it lists what it would download, from where and under which licence, and asks before it fetches anything ([Better sounds](better-sounds.md#the-sound-set-installer)).

A plugin that came in a download and is refused ("cannot be opened because the developer cannot be verified") is cleared in Terminal:

```sh
xattr -d com.apple.quarantine ~/Library/Application\ Support/FuTab/plugins/*.oxp
```

If a plugin is missing, FuTab says so once when it starts and links here.
