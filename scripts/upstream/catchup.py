#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 the FuTab contributors
"""What upstream OxiGuitar has that FuTab hasn't taken yet.

    python3 -I scripts/upstream/catchup.py [--ours REF] [--theirs REF]
                                           [--no-fetch] [-o PATH]

Writes a Markdown report (by default oxiguitar-catchup.md at the
repository's root, which is gitignored; `-o -` prints it): the upstream
releases and commits not in --ours (default HEAD), each with its pull
request, and the files a catch-up merge would conflict in.

The list is git's ancestry, `ours..theirs`, so it is only true while
FuTab catches up by MERGING upstream/develop. A cherry-picked or squashed
copy of an upstream commit has another hash and stays on the list for
good; to turn an upstream change down, merge it and revert it.

Read-only, apart from adding the `upstream` remote when it is missing and
fetching it (upstream's tags go to refs/upstream-tags/, so they never
clash with FuTab's own). It informs and fails nothing.
"""

import argparse
import datetime
import re
import subprocess
import sys
from pathlib import Path

UPSTREAM_URL = "https://github.com/mateusrdp/oxiguitar.git"
UPSTREAM_WEB = "https://github.com/mateusrdp/oxiguitar"
TAGS = "refs/upstream-tags"
# Conflicts that every catch-up merge has, and how to settle them.
EXPECTED = {"CHANGELOG.md": "expected: FuTab keeps its own; resolve with ours"}
# The last "(#123)" of a squash-merged subject is its pull request; any
# number before it is an issue.
PR = re.compile(r"\(#(\d+)\)\s*$")


def git(*args, check=True):
    """Runs git, returns its standard output."""
    done = subprocess.run(["git", *args], capture_output=True, text=True)
    if check and done.returncode != 0:
        sys.exit(f"git {' '.join(args)}: {done.stderr.strip()}")
    return done


def out(*args):
    return git(*args).stdout.strip()


def fetch(note):
    remotes = out("remote").split()
    if "upstream" not in remotes:
        git("remote", "add", "upstream", UPSTREAM_URL)
        note.append(f"Added the remote `upstream` ({UPSTREAM_URL}).")
    git("fetch", "--quiet", "--no-tags", "upstream",
        "+refs/heads/develop:refs/remotes/upstream/develop",
        f"+refs/tags/v*:{TAGS}/v*")


def conflicts(ours, theirs):
    """The files a merge of theirs into ours would conflict in, or None
    when this git can't tell (merge-tree --write-tree needs git 2.38)."""
    done = git("merge-tree", "--write-tree", "--name-only", "--no-messages",
               ours, theirs, check=False)
    if done.returncode not in (0, 1):
        return None
    return done.stdout.splitlines()[1:]


def commits(ours, theirs):
    """The non-merge commits of theirs not in ours, oldest first, each
    with the files it changes."""
    sep = "\x1e"
    log = out("log", "--reverse", "--no-merges", "--name-only",
              f"--format={sep}%H%x1f%h%x1f%as%x1f%an%x1f%s",
              f"{ours}..{theirs}")
    found = []
    for block in log.split(sep):
        if not block.strip():
            continue
        head, _, files = block.partition("\n")
        full, short, date, author, subject = head.split("\x1f")
        found.append({
            "full": full, "short": short, "date": date, "author": author,
            "subject": subject,
            "files": [f for f in files.splitlines() if f.strip()],
        })
    return found


def cell(text):
    return text.replace("|", "\\|")


def report(ours, theirs, note):
    ours_tip = out("rev-parse", "--short", ours)
    theirs_tip = out("rev-parse", "--short", theirs)
    base = out("merge-base", ours, theirs)
    base_line = out("log", "-1", "--format=%h (%as) %s", base)
    missing = commits(ours, theirs)
    merges = int(out("rev-list", "--count", "--merges", f"{ours}..{theirs}"))
    releases = out("for-each-ref", f"--merged={theirs}", f"--no-merged={ours}",
                   "--sort=version:refname", "--format=%(refname:lstrip=2)",
                   f"{TAGS}/v*").split()
    clash = conflicts(ours, theirs)
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = ["# OxiGuitar catch-up", ""]
    lines += [
        f"What upstream OxiGuitar (`{theirs}`, {theirs_tip}) has that FuTab "
        f"(`{ours}`, {ours_tip}) hasn't merged. Made {now} by "
        "`scripts/upstream/catchup.py`.",
        "",
        "Catch up by **merging** `upstream/develop`; a cherry-picked commit "
        "stays on this list. To turn a change down, merge it and revert it.",
        "",
    ]
    lines += [f"- {n}" for n in note]
    lines += [
        f"- Last common commit: {base_line}",
        f"- Missing: **{len(missing)}** commits"
        + (f" (and {merges} merge commit{'s' if merges > 1 else ''})" if merges else ""),
        "",
        "## Upstream releases not in FuTab",
        "",
    ]
    lines += ([f"- [{t}]({UPSTREAM_WEB}/releases/tag/{t})" for t in releases]
              or ["None."])
    lines += ["", "## Merging now would conflict in", ""]
    if clash is None:
        lines.append("Unknown: this git is older than 2.38 (needs `merge-tree --write-tree`).")
    elif not clash:
        lines.append("Nothing: `upstream/develop` merges cleanly.")
    else:
        lines += [f"- `{f}`" + (f" ({EXPECTED[f]})" if f in EXPECTED else "")
                  for f in clash]
    lines += ["", "## Missing changes", ""]
    if not missing:
        lines.append("None: FuTab has everything upstream has.")
    else:
        lines += ["| Date | PR | Change | Commit | Files | Conflicts |",
                  "| --- | --- | --- | --- | --- | --- |"]
        hot = set(clash or []) - set(EXPECTED)
        for c in missing:
            m = PR.search(c["subject"])
            pr = f"[#{m[1]}]({UPSTREAM_WEB}/pull/{m[1]})" if m else "no PR"
            subject = PR.sub("", c["subject"]).strip() if m else c["subject"]
            touched = sorted(hot.intersection(c["files"]))
            flag = ", ".join(f"`{f}`" for f in touched) if touched else ""
            lines.append(
                f"| {c['date']} | {pr} | {cell(subject)} ({cell(c['author'])}) "
                f"| [{c['short']}]({UPSTREAM_WEB}/commit/{c['full']}) "
                f"| {len(c['files'])} | {flag} |")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--ours", default="HEAD", help="FuTab's side (default HEAD)")
    parser.add_argument("--theirs", default="upstream/develop",
                        help="upstream's side (default upstream/develop)")
    parser.add_argument("--no-fetch", action="store_true", help="use what is fetched already")
    parser.add_argument("-o", "--output", help="where to write it; - for stdout "
                        "(default oxiguitar-catchup.md at the repository's root)")
    args = parser.parse_args()

    root = Path(out("rev-parse", "--show-toplevel"))
    note = []
    if not args.no_fetch:
        fetch(note)
    text = report(args.ours, args.theirs, note)
    if args.output == "-":
        sys.stdout.write(text)
        return
    path = Path(args.output) if args.output else root / "oxiguitar-catchup.md"
    path.write_text(text, encoding="utf-8")
    print(f"Wrote {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
