---
name: build-test-rpm
description: Builds a test .rpm of FuTab from the working copy (committed or not), for the user to install with dnf and test as a packaged app (desktop entry, icons, file types). Use whenever the task is to build, make or package a test or local rpm, or to test a change "from the rpm" or "as installed".
---

# Build a test .rpm

Builds the Wayland build's `.rpm` the way the release workflow does, from this checkout, so the user can install it and test FuTab as a packaged app. Run everything from the repository root (`futab/`). Never install the package, never use `sudo` and never run the app: the user does those.

## 1. cargo-about

`scripts/package/licenses.sh` needs `cargo-about`. If `command -v cargo-about` finds it, skip this step. If not, install it (it downloads from crates.io; this skill is the user's request to do so):

```bash
cargo install cargo-about --features cli --locked
```

## 2. Release binaries

```bash
cargo build --release --locked -p futab -p futab-cli
```

A build from clean takes several minutes: run it in the background and wait for it to finish, without polling. If it fails, stop and show the user the error.

## 3. Licence report

```bash
scripts/package/licenses.sh
```

Writes `dist/THIRD-PARTY-LICENSES.html`, which every package carries.

## 4. The .rpm

```bash
scripts/package/linux.sh rpm "$(scripts/package/version.sh)"
```

The last line says `Built …/dist/futab-VERSION-1.x86_64.rpm`. VERSION is the workspace version plus `~dev.DATE.gCOMMIT`, which sorts before the real release, so the release later replaces it. COMMIT is `HEAD`, but the package holds the working copy's files, uncommitted changes included. The warning `%source_date_epoch_from_changelog is set, but %changelog has no entries` is harmless.

`dist/` is ignored by git and may hold older `.rpm` files, so name the new one by its full file name below, not by a glob.

## 5. Tell the user how to install and test

Give the install command with the file built in step 4, in its own `bash` block, for the user to run:

```bash
sudo dnf install ./dist/futab-VERSION-1.x86_64.rpm
```

dnf asks for the user's password and a `y` to confirm. Then give detailed test instructions for the change being tested (where to look, what to expect). For desktop integration (the launcher, icons, file types), say to log out and back in after installing. To go back to the released package later: `sudo dnf remove futab`, then install the release's `.rpm`.
