# Installing

FuTab doesn't publish releases or packages yet: for now, build it from source. When releases come, this page will list the downloads.

## Building from source

You need Rust 1.99 or newer, from [rustup](https://rustup.rs), and a few system libraries; [Building from source](https://github.com/PurpleIcon/futab#building-from-source) in the README lists them. Then:

```sh
git clone https://github.com/PurpleIcon/futab.git
cd futab
cargo build --release -p futab -p futab-cli
```

The program is `target/release/futab`; `target/release/futab-cli` is the command-line tool, which prints a file's contents, converts it to Guitar Pro 7's .gp, and engraves it to PNG and PDF (`futab-cli --help`). `cargo run --release -p futab -- song.gp` builds and starts FuTab with a file.

### Wayland and X11

FuTab comes in two Linux builds: the **Wayland build**, for today's desktops (GNOME, KDE Plasma and most others run Wayland), and the **X11 build**, for desktops that still run only an X server. Each carries only its own display system's code. `cargo build` makes the Wayland build; on a desktop with only an X server, build the X11 one instead:

```sh
cargo build --release -p futab --no-default-features --features x11
```

If you start the wrong build, it says which one you need. **The X11 build is deprecated** and will be dropped once desktops have left X11.

## The plugins

FuTab opens and plays files only through plugins, and uses OxiGuitar's: FuTab is a fork of OxiGuitar and keeps its plugin interface. Install at least the Guitar Pro and MIDI plugins, and an audio output. Each system's page says how: [Linux](install-linux.md), [Windows](install-windows.md), [macOS](install-macos.md). [The official plugins](official-plugins.md) says what each one does. FuTab says so, once, when it starts without them.

To add other plugins, put their `.oxp` files in your own plugin folder ([Settings and plugins](plugins.md)); when the same plugin is in several folders, FuTab uses the higher version, and the one found last when the versions are equal. **Help → About** lists every folder FuTab searches, and **Tools → Plugins** the plugins it found. To leave out a plugin you don't want, untick it in **Tools → Plugins**.

On macOS, if the system refuses a plugin you downloaded yourself ("cannot be opened because the developer cannot be verified"), clear the download mark on the plugin files and start FuTab again:

```sh
xattr -d com.apple.quarantine ~/Library/Application\ Support/FuTab/plugins/*.oxp
```

## Opening Guitar Pro files with a double click

**Linux.** With the source code, `scripts/install-desktop-entry.sh target/release/futab` gives FuTab its icon, an entry in your desktop's menu and the Guitar Pro file types (.gp, .gpx, .gp5, .gp4, .gp3), so double-clicking such a file opens it in FuTab. It writes only under `~/.local/share`; `--uninstall` removes it.

**Windows.** Right-click a .gp file, choose **Open with → Choose another app**, then **Choose an app on your PC** (or **More apps → Look for another app on this PC**), pick `futab.exe` and tick **Always use this app**. Repeat for .gpx, .gp5, .gp4 and .gp3.
