# If a merge PR was squashed

Read this when a merge PR landed on `develop` as a squash commit: the check after merging (in [pull-request.md](pull-request.md)) fails, or the `upstream-report` skill lists PRs already merged as missing.

You can tell: the PR's commit on `develop` has one parent, and the catch-up report against `develop` lists the PRs it merged as missing again. The code is all there, only upstream's history is gone, but the next merge from upstream would conflict on all of it again. Restore the history with a merge that changes no file:

1. Check that `develop` really has the merged content: the squash commit's tree must equal the merge branch's last commit's tree.

   ```bash
   test "$(git rev-parse <squash commit>^{tree})" = "$(git rev-parse <merge branch tip>^{tree})" && echo same
   ```

   If they differ, stop and tell me what differs: `-s ours` would record upstream's commits as merged while some of their changes are missing.
2. On a branch from up-to-date `origin/develop` named `fix/oxiguitar-history-pr<N>`, record upstream's target commit as merged, keeping `develop`'s files:

   ```bash
   git merge -s ours --no-ff --signoff <upstream target commit>
   ```

   with a message saying which PR was squashed and that the merge changes no file, naming the target as `OxiGuitar PR N`.
3. Check: `git diff origin/develop HEAD` is empty, and the catch-up report on the branch shows the target as the last common commit.
4. Add a changelog entry under `### Fixed` ("Upstream history up to OxiGuitar PR N", why it was missing, and that the merge changes no file) as a commit of its own.
5. With my go-ahead, push and open the PR titled `Restore history FROM upstream OxiGuitar PR N` (no `#`), its description opening with the merge-commit warning, and merge it as above, with `--merge`.
