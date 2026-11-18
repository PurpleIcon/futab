# FuTab's package repositories (`PurpleIcon/futab-packages`)

**Status:** plan, not built; every decision in section 10 settled (18 Nov 2026). Nothing below exists yet: no repository, key, secret or token. Each of those is made only on the user's go-ahead.

**Goal:** FuTab's own signed apt, dnf and Flatpak repositories, served from GitHub Pages, so `apt upgrade`, `dnf upgrade` and `flatpak update` keep FuTab and FuTab's own plugins current, as OxiGuitar's repositories already do for its plugins.

**Model:** OxiGuitar's `mateusrdp/oxiguitar-packages` (read at `070d367`, 17 Nov 2026), whose Site workflow does exactly this for OxiGuitar. FuTab takes the part that builds and serves the repositories first, and its plugin packaging (`plugin-release.yml`, `plugin-publish.yml`) when FuTab's first plugin is ready (section 8). Winget is left out.

**Why a repository of its own** (D1, settled 18 Nov 2026), rather than a site built inside `PurpleIcon/futab`: FuTab will have plugins of its own, each in its own repository (the first, audio tracks, is coming), and they all feed one site. `futab-packages` lists those repositories and builds the site from their latest releases; a site inside `futab` could see only `futab`'s releases, and would share `futab`'s one Pages site with the manual. It belongs to the **PurpleIcon organisation**, beside `futab`: the site's address (`purpleicon.github.io/futab-packages`), which users write into their apt, dnf and Flatpak setup, must never change, and moving a repository between accounts would change it; the org's admins, rulesets and token owner are then the same as `futab`'s.

## 1. How it works, end to end

1. A `v*` tag on `PurpleIcon/futab` starts `release.yml`, which builds and tests every package and attaches them, with `SHA256SUMS`, to a **draft** release (as today).
2. The user publishes the draft. That starts `publish.yml` (as today): it checks the files against `SHA256SUMS`, then sends `repository_dispatch` (`event_type: plugin-published`, `client_payload: {plugin: "futab", tag, repository}`) to `PurpleIcon/futab-packages`. Today it sends nothing because `PACKAGES_TOKEN` isn't set.
3. In `futab-packages`, the Site workflow receives the event, downloads the `.deb`, `.rpm` and `.flatpak` files of the **latest published release** of each repository in `repositories.txt` (`PurpleIcon/futab`, and later FuTab's plugins), checks each against that release's `SHA256SUMS`, builds the apt, dnf and Flatpak repositories from scratch, signs them, tests installing from them, and deploys them to Pages.
4. Users who added the repositories get the new version on their next upgrade. Nothing polls.

The repositories hold only the latest published release (as OxiGuitar's do): there is no downgrade from them. Older versions stay on the GitHub releases.

**Size:** one release is about 160 MB on the site (4 `.deb` at about 11 MB, 4 `.rpm` at about 17 MB, 2 Flatpak bundles at about 21 MB, imported into OSTree). That is well under Pages' 1 GB limit.

## 2. The repository's layout

A new public repository, `PurpleIcon/futab-packages`, licensed GPL-3.0-or-later, holding scripts only (no package files are committed):

| Path | What it is | Source |
|---|---|---|
| `repositories.txt` | The repositories whose latest published release goes in: `PurpleIcon/futab` (FuTab's plugins are added as they come, section 8) | new |
| `scripts/fetch-packages.sh` | Downloads and checks the `.deb`, `.rpm` and `.flatpak` files | copied from oxiguitar-packages; skips pre-releases as well as drafts |
| `scripts/build-site.sh` | apt (`apt-ftparchive`, `InRelease`, `Release.gpg`), dnf (`rpmsign`, `createrepo_c`, signed `repomd.xml`), the public key, `futab.sources`, `futab.repo`, the page | copied; `oxiguitar` names become `futab`, `SITE_URL` defaults to `https://purpleicon.github.io/futab-packages` |
| `scripts/flatpak-repo.sh` | Imports the bundles into one signed OSTree repository, writes `futab.flatpakrepo` and `io.github.purpleicon.FuTab.flatpakref` (`RuntimeRepo` = Flathub) | copied; app ID `io.github.purpleicon.FuTab` |
| `scripts/test-install.sh` | Serves the site locally and installs `futab` with apt (Debian) and dnf (Fedora), signatures checked | copied; checks `/usr/bin/futab` instead of a plugin file |
| `scripts/test-flatpak.sh` | Installs the app from the `.flatpakref` and opens the sample in the sandbox | copied; FuTab's app ID, no plugin extensions of its own |
| `scripts/make-test-packages.sh` | Made-up `.deb`/`.rpm`/bundle for CI | copied, trimmed |
| `scripts/check-dco.sh` | Sign-off check | copied from FuTab |
| `site-src/index.html` | The site's page: how to add both FuTab's and OxiGuitar's repositories, and the key's fingerprint | rewritten for FuTab |
| `.github/workflows/site.yml` | Build, sign, test, deploy (section 3) | copied, adapted |
| `.github/workflows/ci.yml` | Shellcheck, DCO, and "Repositories": a site built from test packages with a throwaway key, installed with apt and dnf; `ci-success` | copied, trimmed |
| `.github/CODEOWNERS` | `* @cgullcharlie` | as in futab |
| `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `LICENSE`, `.gitignore` | `.gitignore` excludes `*.key`, `*.pem`, `*.gpg` and `*.asc` at the top level, so a key file can't be committed by accident | new |

The copied scripts keep their SPDX header and OxiGuitar's copyright line, with FuTab's added, and the README credits oxiguitar-packages (by commit hash, per FuTab's rule on referring to upstream).

**Not copied in the first PR:** the plugin packaging (`plugin-release.yml`, `plugin-release-try.yml`, `plugin-publish.yml`, `scripts/plugin-package/`, `plugins/trial/` and the Rust files that serve only the trial plugins: `Cargo`, `clippy.toml`, `deny.toml`), which comes with FuTab's first plugin (section 8); winget (`docs/winget.md`, `scripts/make-winget-manifests.sh`); and the Release button (`release.yml`, `scripts/release/`), which comes later (section 9).

**A new repository, not a fork** of oxiguitar-packages: Actions are off by default on a fork, a fork's history and default branch are upstream's, and the scripts taken are about 400 lines now (more with the plugin packaging). The cost: fixes upstream makes to these scripts are taken by hand (an `upstream-report`-style check isn't worth it at this size).

### Branches and rules

- **One branch, `main`**, the default, and Pages deploys from it. Upstream has `develop` as its default and `main` for Pages, which needs a "hand-over" job (a `repository_dispatch` always runs on the default branch). FuTab's repository has no releases of its own, so a single branch is simpler and drops that job.
- The same ruleset as futab's (no deletion or force push, changes by PR with one code-owner approval, stale approvals dismissed, org admins bypass by PR only), on `main`. Squash merges, signed off, as in futab.
- Pages: source "GitHub Actions"; the `github-pages` environment allows `main` only (GitHub's default for this environment).

## 3. The Site workflow

```text
on: repository_dispatch (types: [plugin-published]), workflow_dispatch
concurrency: site (never cancelled: each run rebuilds from scratch, so the last one wins)

build (environment: signing; runs only on main)
  tools: apt-utils createrepo-c rpm gnupg flatpak ostree dbus
  import the key from the environment's secrets into a temporary GNUPGHOME
  fetch-packages.sh   (GITHUB_TOKEN reads the public releases)
  build-site.sh       (apt, dnf, Flatpak, futab.gpg, futab.asc, futab.sources, futab.repo, index.html)
  test-install.sh     (apt in Debian, dnf in Fedora, signatures checked)
  test-flatpak.sh     (app from the .flatpakref, runtime from Flathub; with OxiGuitar's
                       Guitar Pro extension installed from OxiGuitar's remote, the sample opens)
  upload-pages-artifact
deploy (pages: write, id-token: write) -> deploy-pages
```

The run's log says who sent the event (`client_payload.repository`, `tag`), and the job summary lists what the site holds (`packages.txt`).

The Flatpak test installs OxiGuitar's `io.github.mateusrdp.OxiGuitar.Plugin.guitarpro` from OxiGuitar's own remote, to check the extension point still matches, as a FuTab user would. It downloads from OxiGuitar's site, which is a workflow, not the app: the app itself still downloads nothing.

**Started by hand** (Actions → Site → Run workflow) for the first build, and after the key changes.

## 4. The signing key

One key signs all three repositories (apt `Release`/`InRelease`, every `.rpm` and `repomd.xml`, the OSTree commits and summary), as upstream does.

- **Type:** RSA 4096, signing only, as upstream (`gpg --quick-generate-key 'FuTab packages (https://github.com/PurpleIcon/futab-packages)' rsa4096 sign never`; no expiry, D4). RSA works with every apt, rpm and OSTree in use; Ed25519 would be smaller but isn't checked by older rpm versions.
- **Who makes and holds it:** the user, on their own machine, never Claude. Its private part exists in three places only:
  1. the secrets `APT_SIGNING_KEY` (armoured private key) and `APT_SIGNING_PASSPHRASE` of an **environment `signing`** in `futab-packages`, restricted to `main`, so a workflow on any other branch or a pull request can't read it (stricter than upstream's repository secrets);
  2. an offline backup the user keeps (an encrypted USB stick, or a password manager);
  3. with it, a **revocation certificate** (`gpg --gen-revoke`), kept offline beside the backup.
- **Never committed,** in any repository; never pasted into an issue, PR, log or chat. The workflow imports it into a temporary `GNUPGHOME` on the runner, which is thrown away with the runner.
- **The public key and its fingerprint** are published: `futab.gpg` and `futab.asc` on the site, the fingerprint on the site's page, in `futab-packages`' README and in FuTab's install docs, so users can check what they downloaded.
- **Kept apart from OxiGuitar's key:** apt sources use `Signed-By:` per source, so OxiGuitar's key is trusted only for OxiGuitar's repository and FuTab's only for FuTab's.
- **If it leaks:** publish the revocation, make a new key, replace the secrets, rebuild the site, and tell users in FuTab's README and release notes to fetch the new key. Users still holding the old key then get an unknown-key error on their next upgrade, so nobody stays on the old key silently; apt, dnf and Flatpak never check revocations by themselves, so the error and the notice are what move them. A stolen key alone is not enough to fool them: the thief must also serve the files, from our Pages site or their network.

## 5. `PACKAGES_TOKEN`

`publish.yml` in `PurpleIcon/futab` reads the secret `PACKAGES_TOKEN` and calls `POST /repos/PurpleIcon/futab-packages/dispatches` with it.

- **What it must be:** a **fine-grained personal access token**, resource owner **PurpleIcon**, repository access **only `PurpleIcon/futab-packages`**, permissions **Contents: Read and write** (what the dispatches endpoint asks for) and Metadata: Read (set automatically). Nothing else: no access to `futab`, no Actions, Pages, Secrets or Administration.
- **Owner:** made by `cgullcharlie`. If PurpleIcon requires approval of fine-grained tokens, the org owner approves it (the same person).
- **Expiry:** one year, with a reminder to renew. An expired token makes Publish fail visibly (the API returns 401), which is the signal to renew it; the release itself is not affected, and Publish can be re-run by hand (`workflow_dispatch` with the tag) once a new token is set.
- **Where:** a repository secret named `PACKAGES_TOKEN` (Settings → Secrets and variables → Actions) in `PurpleIcon/futab`, and in each FuTab plugin repository as it comes (section 8). The same token serves them all: it grants nothing in the repositories that hold it, only dispatching to `futab-packages`.
- **When:** only after `futab-packages` exists. Set earlier, the dispatch gets a 404 and Publish fails. Once the repository exists, a dispatch before `site.yml` is on `main` succeeds and starts nothing.
- **Alternative:** a GitHub App installed on PurpleIcon with Contents read/write on `futab-packages` only, and `actions/create-github-app-token` in `publish.yml`. No expiry and not tied to a person's account, but it changes `publish.yml` and adds two secrets. Worth it once the Release button (section 9) needs an App anyway; one App can then do both.

## 6. Beside OxiGuitar's plugin repositories

FuTab's repositories hold FuTab (`futab`, `futab-x11`, and the Flatpak `io.github.purpleicon.FuTab`) and, as they come, FuTab's own plugins (section 8). OxiGuitar's plugins stay in OxiGuitar's repositories, signed with OxiGuitar's key. Users add both:

| | FuTab's | OxiGuitar's |
|---|---|---|
| apt | `/etc/apt/keyrings/futab.gpg`, `/etc/apt/sources.list.d/futab.sources` | `oxiguitar.gpg`, `oxiguitar.sources` (as today) |
| dnf | `/etc/yum.repos.d/futab.repo` | `oxiguitar.repo` (as today) |
| Flatpak | remote `futab` (`futab.flatpakrepo`), and `flathub` for the runtime | remote `oxiguitar` (`oxiguitar.flatpakrepo`) |

- **No package name is in both**, so neither repository can replace the other's packages: FuTab's are `futab*` (its plugins included), OxiGuitar's are `oxiguitar*`.
- **The `.deb` and `.rpm` already recommend** `oxiguitar-guitarpro`, `oxiguitar-midi`, `oxiguitar-alsa` and `oxiguitar-pipewire`, and suggest NAM, the equalizer, the wah and the file-format plugins (`scripts/package/linux.sh`). apt resolves them across every configured source, and dnf installs weak dependencies by default, so with both repositories added, `apt install futab` or `dnf install futab` brings the plugins. Without OxiGuitar's repository, FuTab still installs, with no plugins. No change to the packages is needed.
- **Flatpak:** FuTab's manifest declares OxiGuitar's extension point, `io.github.mateusrdp.OxiGuitar.Plugin`, so OxiGuitar's plugin extensions, installed from the `oxiguitar` remote, attach to FuTab. A `.flatpakref` can add only one remote (plus its runtime repository), so the `oxiguitar` remote is still added by its own command.
- **Users must not install `oxiguitar` itself** (or `io.github.mateusrdp.OxiGuitar`): the install docs keep saying so. Nothing in FuTab's packages pulls it in.
- **Risk kept from today** (`../publishing.md` §1): an OxiGuitar plugin release built for a newer plugin interface than FuTab's core reaches FuTab users on their next upgrade. Mirroring pinned plugin versions into FuTab's repositories would fix that, but see decision D7.

## 7. Changes in FuTab afterwards

One PR on `PurpleIcon/futab`, after the first site build works:

- **`README.md`** (Install) and **`docs/manual/src/install-linux.md`:** the repositories become the first way to install on Linux: add FuTab's and OxiGuitar's repositories, then `sudo apt install futab` / `sudo dnf install futab` (the plugins come with it), or `flatpak install futab io.github.purpleicon.FuTab` plus the plugin extensions from `oxiguitar`. FuTab's key fingerprint beside OxiGuitar's. The downloaded `.deb`, `.rpm` and bundle stay as the second way. "Never install `oxiguitar` itself" stays.
- **`scripts/package/release-notes.md`:** says that the Linux packages are also in FuTab's repositories, with a link to the site.
- **`.github/workflows/publish.yml`:** its header comment names `PurpleIcon/futab-packages` instead of OxiGuitar's repository and drops the tap; its file check adds the Flatpak bundles (`FuTab-${v}-x86_64.flatpak`), which the repository now serves. The step name loses "and the tap".
- **`.github/workflows/release.yml`** (Flatpak job comment) and **`scripts/package/io.github.purpleicon.FuTab.yml`** (header): "FuTab has no Flatpak repository yet" becomes a pointer to `futab-packages`.
- **`CHANGELOG.md`:** an `### Added` entry under `[Unreleased]`, e.g. "**Package repositories** (#N): FuTab's own signed apt, dnf and Flatpak repositories; `apt upgrade`, `dnf upgrade` and `flatpak update` now keep FuTab current."
- **`docs/futab-adr/`:** a record for running FuTab's own repositories (and the choices in section 10), if the user wants one.
- This note's status becomes "built".

## 8. FuTab's own plugins

The first is the audio-tracks plugin, coming soon; its repository's name is still to be chosen (for example `PurpleIcon/futab-audio-tracks`). Each FuTab plugin lives in its own PurpleIcon repository, with its own releases, as OxiGuitar's plugins do. When the first one is ready to release:

1. **`futab-packages` takes upstream's plugin packaging:** the reusable workflows `plugin-release.yml` (builds, tests and attaches the plugin's `.deb`, `.rpm`, Flatpak extension and `SHA256SUMS` to a draft release) and `plugin-publish.yml` (on publishing: checks the files, then dispatches `plugin-published` here), with `scripts/plugin-package/`, adapted to FuTab's names. The plugin repository calls them with a few lines, pinned to a commit of `futab-packages`.
2. **The plugin's packages:** named `futab-<plugin>` (`.deb`, `.rpm`), installed into `lib/futab/plugins`, and depending on `futab`. FuTab's `.deb` and `.rpm` may then recommend it, as they do OxiGuitar's.
3. **Its Flatpak extension** is `io.github.purpleicon.FuTab.Plugin.<name>`, attaching to FuTab's own extension point (D10), which FuTab's manifest declares beside OxiGuitar's; its `plugins/` folder appears in `/app/lib/futab/plugins`, which FuTab already searches first.
4. **`repositories.txt`** gets the plugin's repository, and the plugin repository gets the `PACKAGES_TOKEN` secret (section 5).
5. **The plugin repository** gets the same ruleset, CODEOWNERS and `CHANGELOG.md` rules as `futab`, and the `github` rule's list of repositories names it.

## 9. Later, not in this plan

- **The Release button** in `futab-packages` (`../.claude/rules/github/RULE.md`: "the Release workflow in futab-packages will create releases for the core app"): a GitHub App with a bypass in futab's branch ruleset and in "Protect release tags". The tags rule says to ask the user before adding any bypass, so it is a plan of its own.
- **A setup package** (`futab-repos.deb`/`.rpm`, as RPM Fusion's `-release` packages) that installs both repositories' definitions and keys in one step.

## 10. Open decisions for the user

| # | Decision | Recommendation |
|---|---|---|
| D1 | Where the site is built | **Settled (18 Nov 2026):** a new repository of its own, `PurpleIcon/futab-packages`, in the PurpleIcon organisation, with copied scripts (not a fork) |
| D2 | Branches: `main` only, or `develop` + `main` as in futab and upstream | **Settled (18 Nov 2026):** `main` only, with futab's ruleset |
| D3 | The key's user ID: which address, or none (`FuTab packages (https://github.com/PurpleIcon/futab-packages)`) | **Settled (18 Nov 2026):** no address: `FuTab packages (https://github.com/PurpleIcon/futab-packages)` |
| D4 | The key's expiry: never (upstream) or a date (for example 3 years, extended before it lapses) | **Settled (18 Nov 2026):** never, as upstream; revoked and replaced if it leaks (section 4) |
| D5 | Passphrase on the key | **Settled (18 Nov 2026):** yes, kept as `APT_SIGNING_PASSPHRASE` and in the offline backup |
| D6 | `PACKAGES_TOKEN`: fine-grained PAT (one year, Contents read/write on `futab-packages` only) or a GitHub App | **Settled (18 Nov 2026):** the PAT now; an App when the Release button comes |
| D7 | Plugins: users add OxiGuitar's repositories (this plan), or FuTab mirrors pinned OxiGuitar plugin versions into its own (one repository to add, versions FuTab tested, but FuTab then re-signs and redistributes binaries it didn't build, must offer their source, and updates them by hand) | **Settled (18 Nov 2026):** users add both, as now |
| D8 | Pre-releases: kept out of the repositories (this plan), or a second channel (`testing` suite, `beta` Flatpak branch) | **Settled (18 Nov 2026):** kept out, no pre-release channel |
| D9 | When to publish v0.2.0 | **Settled:** v0.2.0 was published on 18 Nov 2026 |
| D10 | The extension point FuTab's plugins attach to in Flatpak: OxiGuitar's (`io.github.mateusrdp.OxiGuitar.Plugin`, so the plugin's ID would be `io.github.mateusrdp.OxiGuitar.Plugin.<name>`), or a second one of FuTab's own (`io.github.purpleicon.FuTab.Plugin`) declared beside OxiGuitar's, so OxiGuitar's plugins still attach | **Settled (18 Nov 2026):** FuTab's own point, `io.github.purpleicon.FuTab.Plugin` (directory `lib/futab`), declared beside OxiGuitar's; FuTab's plugins then don't attach to OxiGuitar's Flatpak, which is intended |

## 11. Order of work

Each step that creates something on GitHub, or a key or token, waits for the user's go-ahead.

1. ~~The user settles the open decisions~~: all settled on 18 Nov 2026 (section 10).
2. **User:** creates `PurpleIcon/futab-packages` (public, empty), its ruleset and CODEOWNERS; enables Pages with source "GitHub Actions".
3. **User**, on their machine: makes the key, the revocation certificate and the offline backup; creates the environment `signing` (branch `main` only) with the secrets `APT_SIGNING_KEY` and `APT_SIGNING_PASSPHRASE`; gives Claude the fingerprint (public).
4. **Claude:** the repository's first PR (section 2: scripts, workflows, README with the fingerprint, page), checked by its CI with a throwaway key.
5. After merge, the user runs Site by hand on `main`, then checks from their own machine: adds both repositories and installs `futab` with dnf (Fedora), and the Flatpak from `futab.flatpakref`.
6. **User:** makes `PACKAGES_TOKEN` (section 5) and sets it in `PurpleIcon/futab`. Test: Actions → Publish → Run workflow with the latest published tag, which must start Site in `futab-packages`.
7. **Claude:** FuTab's docs PR (section 7).
8. When FuTab's first plugin is ready to release: section 8.
