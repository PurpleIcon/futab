---
name: tags
description: How FuTab's release tags are made and pushed, how they are protected, and what is never done with tags.
---

# Tags

Rules for git tags on FuTab. A `v*` tag is a FuTab release: pushing one starts the Release packages workflow (`.github/workflows/release.yml`), which builds every package and makes the draft release.

## The protection

- The ruleset **"Protect release tags"** (id 27543198, made 18 Nov 2026) covers `refs/tags/v*` on `PurpleIcon/futab`: creating, moving (updating) and deleting such a tag is restricted. Only organisation admins bypass it (always), so only an org admin can make, move or delete a release tag. See it under Settings → Rules, or `gh api repos/PurpleIcon/futab/rulesets/27543198`.
- It is there against mistakes as much as people: a stray tag, upstream's tags pushed by accident, or a published release's tag moved.
- Never change, switch off or delete the ruleset, and never add a bypass to it, without my explicit go-ahead. A workflow that will create tags (such as a future futab-packages release workflow) needs a bypass entry of its own: ask me first.

## Making a release tag

- Only on my explicit go-ahead, after the release PR (`feat/release-X.Y.Z`) is merged into `develop` and `develop` is merged into `main` with a merge commit.
- On `main`'s merge commit, annotated, with my identity (check `git config user.email` first, as for commits), named `vX.Y.Z` with the message `FuTab X.Y.Z`:

  ```bash
  git fetch origin main
  git tag -a vX.Y.Z -m "FuTab X.Y.Z" origin/main
  ```

  Check first that `origin/main` is that merge commit, and that its `Cargo.toml` has version `X.Y.Z`.
- Push that tag alone, by its full name:

  ```bash
  git push origin refs/tags/vX.Y.Z
  ```

- Then check the Release packages run started for it (`gh run list --repo PurpleIcon/futab --workflow "Release packages" --limit 1`), and tell me its link. The run makes a **draft** release: I check and publish it.

## Never

- Never `git push --tags` or `git push --follow-tags`: they push every local tag, OxiGuitar's included (`v0.19.2` and later), and each would start a release.
- Never fetch upstream's tags: `git fetch --no-tags upstream` (the `upstream` remote should have `tagOpt = --no-tags`). OxiGuitar's version numbers are not FuTab's.
- Never move, re-tag or delete a tag that was pushed, even a wrong one: stop and tell me. A published release's tag must keep pointing at what was released.
- Never make a lightweight (non-annotated) release tag.
