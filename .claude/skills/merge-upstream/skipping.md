# Skipping a PR

Read this when the merge's arguments have `skip #X`. Steps 2 and 3 are those of [SKILL.md](SKILL.md).

A PR can be skipped, but **only by merging it and reverting it**, never by leaving it out. Leaving it out would mean cherry-picking around it, which loses the ancestry the catch-up report and every later merge depend on.

The revert is a commit of its own, after the merge commit and in the same branch and PR, so the history says plainly what FuTab turned down. Git can't revert while a merge is uncommitted, so ask me to approve both together. Once I say commit:

```bash
git commit -s
```

```bash
git revert -s --no-edit <sha of #X>
```

Then reword the revert's message to `Skip OxiGuitar's <title> (OxiGuitar PR X)`, with the reason in its body. Settle any conflicts as in step 2, check names and build again (step 3), and name every skipped PR, with its reason, in the report and the PR description. Upstream's release commits and FuTab's own version are never handled by skipping: step 2's rules for version numbers cover them.

What skipping means (say this to me when I ask to skip, for that PR in particular):

- **Upstream counts it as merged.** The catch-up report won't list it again, and git won't offer it again. Getting it later takes a deliberate `git revert` of the revert, not another merge.
- **Later upstream PRs may build on it** (for example OxiGuitar PR 289 builds on PR 270's Harmonize). Before skipping, check whether later missing PRs touch the same files or code (`git diff --stat <sha>^ <sha>`, compared with what later commits change). If they do, they'll conflict or not build once it's skipped. Say which ones, and skip them all or none.
- **The cost grows with every merge.** Each later upstream change to the code the revert removed conflicts again in every future merge. Skipping suits self-contained changes FuTab doesn't want (OxiGuitar-only links or branding; `FUNDING.yml` has its own rule in step 2); for a feature FuTab doesn't want, hiding it behind a setting or a plugin is often cheaper over time than reverting it.
- **The changelog leaves it out**, and the PR description says why.
