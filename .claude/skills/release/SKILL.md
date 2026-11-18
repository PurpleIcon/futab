---
name: release
description: Takes a FuTab release from start to finish, or picks one up where it stopped. It covers the release PR (scripts/release/bump.sh), develop into main, the v* tag, the Release packages run, checking the draft, publishing it on the user's yes, and the Publish run. Use whenever the task is to release, cut, tag, ship or publish a FuTab version, to publish a draft release, or to ask where a release stands.
argument-hint: "X.Y.Z | patch | minor | major"
---

# Release FuTab

`$ARGUMENTS` is the version, `X.Y.Z`, or `patch`, `minor` or `major`. If it's missing, ask with the question tool. While FuTab is below 1.0, catching up with upstream or adding features is `minor`, and fixes alone are `patch`.

A release isn't finished until it is **published** and its Publish run has passed. A draft release is not a release. Never wrap up at "the run makes a draft" (v0.2.0 waited as a draft for that reason). If the work has to stop earlier, say plainly in the last message which step the release is at and what is left, and that `/release X.Y.Z` picks it up.

Run everything from the repository root. The rules still apply: `github` (identity, sign-off, push questions, merge methods, `#` numbers, watching CI) and `tags` (making and pushing the tag). This skill orders them, and decides the two lean-CI questions for a release (steps 1 and 3); otherwise it doesn't repeat the rules.

## 0. Where does it stand?

Always start here, so a release begun in an earlier session goes on from its own step.

First, work out `X.Y.Z`. For `patch`, `minor` or `major`, count from FuTab's latest release tag (read from `origin`, so no tag is fetched):

```bash
git fetch --no-tags origin develop main
git ls-remote --tags --refs origin 'v*' | awk -F/ '{print $3}' | sort -V | tail -1
```

Then:

```bash
gh pr list --repo PurpleIcon/futab --state all --head feat/release-X.Y.Z --json number,state,url
git log --oneline -1 --grep '^Release X.Y.Z' origin/develop
git log --oneline -1 --grep '^Release X.Y.Z' origin/main
git ls-remote origin refs/tags/vX.Y.Z
gh release view vX.Y.Z --repo PurpleIcon/futab --json isDraft,publishedAt,url
```

| What you find | Go to |
|---|---|
| No release PR | 1 |
| The release PR is open | 2 |
| `Release X.Y.Z` is on `develop` but not on `main` | 3 |
| It's on `main`, with no tag | 4 |
| A tag, but no release (the run is going, or failed) | 5 |
| A draft release | 6 |
| A published release | 7 |

## 1. The release PR

A release PR is **never lean**: it always runs full CI, so the packages are built and tested before the tag. Don't ask the lean question for it.

1. `develop` is ready: `[Unreleased]` in `CHANGELOG.md` has entries, and its latest CI run passed (`gh run list --repo PurpleIcon/futab --branch develop --workflow CI --limit 1`). Ask the user whether any open PR should go in first.
2. Branch `feat/release-X.Y.Z` from `origin/develop`.
3. Write the release's one-line summary as the first line under `## [Unreleased]`, above the `###` headings: what a user gets, in a sentence. `bump.sh` makes it the metainfo's release text (at most 300 characters), and it opens the release notes. Show it to the user.
4. Run `scripts/release/bump.sh X.Y.Z`. It changes `Cargo.toml`, the `Cargo.lock` files, `debian/changelog`, the test plugins' manifests and the metainfo `<release>`, and turns `[Unreleased]` into `## [X.Y.Z] - DATE`, leaving `[Unreleased]` empty. That makes the release PR the one PR to `develop` that adds no `[Unreleased]` entry (the github rule allows it). If `bump.sh` stops, fix what it names; never bump a file by hand.
5. Update what names the release in words: `git grep -n 'OLD-VERSION'` (leave the changelogs, the metainfo and the lock files' third-party crates alone). Also check:
   - `ROADMAP.md`: the milestone shows as released.
   - The merge-upstream skill's version table, if this release follows a merge from upstream.
   - The plugin guide's minimum FuTab version (`docs/plugins/src/README.md`), if the plugin interface changed.
   - `scripts/package/release-notes.md` and the README, if what is shipped changed.
6. Build and lint only, as the general rule says: `cargo build`, `cargo fmt --all -- --check`, `cargo clippy --workspace --all-targets -- -D warnings`.
7. Ask the user to check the diff. Commit only on their go-ahead, signed off, with the `Release X.Y.Z` subject.
8. Check the commit messages for `#` numbers, as the github rule says (`git log origin/develop..HEAD --format=%B | grep -nE '#[0-9]+'`). Then ask whether to push, offering only **Not yet** and **Yes, push** (full CI). There is no **Lean push** for a release PR.
9. Open the PR into `develop`, without the `lean-ci` label, titled `Release X.Y.Z: <the summary, shortened>`. Its body says what `bump.sh` changed, what else changed, the checks, and "After merging": steps 3 to 7 of this skill. Check the title and body for `#` numbers before creating it.
10. Watch its CI in the background (`gh pr checks N --repo PurpleIcon/futab --watch --fail-fast > /dev/null`), and go on when it ends. If a check fails, show it and fix it on the branch.

## 2. Merge the release PR

When its CI is green, say: "Squash and merge, and keep the message GitHub fills in." The user merges it, or you do when asked (`gh pr merge N --squash`). Straight after, check the squash commit's sign-off (`scripts/check-dco.sh origin/develop^ origin/develop`), as the github rule says.

## 3. `develop` into `main`

1. Decide whether this PR is lean, without asking. It is lean only when both of these hold, so it holds nothing that full CI hasn't already passed:
   - `main` is an ancestor of `develop` (`git merge-base --is-ancestor origin/main origin/develop`): the merge's result is exactly `develop`'s tip;
   - `develop`'s tip is the release's squash commit, and the CI run of its push to `develop` passed (`gh run list --repo PurpleIcon/futab --branch develop --workflow CI --event push --limit 1 --json headSha,conclusion`; its `headSha` is that commit).

   Otherwise it runs full CI. Tell the user which it is, and why when it's full: something unexpected is on one of the branches.
2. Open a PR from `develop` to `main`, titled `Release vX.Y.Z: merge develop into main`, with `--label lean-ci` when it's lean. Its body says what it carries and that the tag goes on its merge commit. Check its title and body for `#` numbers. Watch its CI in the background, as in step 1.
3. When it's green, say in bold: **"Merge #N with Create a merge commit, not Squash and merge."** If it carries upstream's history (a merge from upstream since the last release), add ": it carries upstream's history", as the github rule says. The user merges it, or you do when asked (`gh pr merge N --merge`).
4. After the merge, `git fetch --no-tags origin main`. Check that `origin/main` is that merge commit and its `Cargo.toml` says `X.Y.Z`.

## 4. The tag

Follow the tags rule exactly: only on the user's go-ahead (ask with the question tool), annotated, on `origin/main`, pushed alone by its full name.

## 5. The Release packages run

1. Find the run: `gh run list --repo PurpleIcon/futab --workflow "Release packages" --limit 1`. Give the user its link.
2. Watch it in the background until it ends, and go on when you're told it finished (don't poll):

   ```bash
   gh run watch RUN-ID --repo PurpleIcon/futab --exit-status > /dev/null
   ```

   It takes about half an hour (v0.2.0: 31 minutes). Don't wrap up while it runs: the background watch tells you when it ends.
3. If it fails, show the failing step (`gh run view RUN-ID --repo PurpleIcon/futab --log-failed`). Never move, delete or re-push the tag. A runner or network failure can be re-run (`gh run rerun RUN-ID --failed`) once the user agrees. A fault in the code or packaging needs a fix through a PR and a new patch version: tell the user, and stop.

## 6. Check the draft, then publish it

```bash
gh release view vX.Y.Z --repo PurpleIcon/futab --json isDraft,tagName,assets,body,url
grep -n "'files in all'" .github/workflows/release.yml
```

Check that:
- the release is still a draft;
- it has the number of packages that `release.yml`'s `expect N '*' 'files in all'` line names, plus `SHA256SUMS`;
- its notes open with "Which file do I need?", name `X.Y.Z` in every file name, and end with the version's changelog section;
- the tag points at `origin/main`'s merge commit (`git ls-remote origin 'refs/tags/vX.Y.Z^{}'`).

Then tell the user what publishing does:
- the release becomes public and "Latest";
- it starts the Publish workflow, which checks every file against `SHA256SUMS`;
- if `PACKAGES_TOKEN` is set, Publish tells `PurpleIcon/futab-packages`, which updates the apt, dnf and Flatpak repositories;
- a published release isn't turned back into a draft.

Ask with the question tool, **Publish vX.Y.Z now?**, with exactly two answers: **Publish** and **Not yet**. On **Publish**:

```bash
gh release edit vX.Y.Z --repo PurpleIcon/futab --draft=false
```

On **Not yet**, say plainly that the release is not finished, and that `/release X.Y.Z` publishes it later.

## 7. The Publish run

1. Find it (`gh run list --repo PurpleIcon/futab --workflow Publish --limit 1`) and watch it in the background, as in step 5.
2. Report:
   - its result;
   - whether it told the package repositories: "Told PurpleIcon/futab-packages", or the notice that `PACKAGES_TOKEN` isn't set;
   - if it told them, the Site run in `PurpleIcon/futab-packages`.

   If Publish fails, the release stays published. Show the failing step, and once it's fixed, re-run Publish by hand (Actions → Publish → Run workflow, with the tag).
3. The release is done. Give the user the release's link and the Publish run's link.

## Never

- Tag without the user's go-ahead, or publish without their **Publish** answer.
- Change, add or delete a published release's files, or delete a release or its tag.
- Push tags in bulk (`--tags`, `--follow-tags`) or fetch upstream's.
