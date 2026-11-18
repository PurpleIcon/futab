#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 the FuTab contributors
"""Checks the layout of the agent skills and rules under .claude/.

    python3 -I scripts/agents/check-layout.py skills|rules|all

Skills are .claude/skills/<name>/SKILL.md, rules .claude/rules/<name>/RULE.md:
  - <name> is kebab-case: lower-case letters, digits and hyphens only,
    1 to 64 characters;
  - the file's name is exactly SKILL.md or RULE.md (case-sensitive);
  - the file opens with YAML front matter (between two `---` lines) holding
    a non-empty `name` and `description`, and `name` equals <name>.
Nothing else belongs directly under .claude/skills/ or .claude/rules/.

Prints one line per problem and exits 1 if there is any, else prints "ok"
and exits 0. Reads only; changes nothing (the review-skills and
review-rules skills fix what it finds, once the user says so).
"""

import pathlib
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("check-layout.py needs PyYAML (python3-pyyaml, or pip install pyyaml)")

ROOT = pathlib.Path(__file__).resolve().parents[2]
KINDS = {"skills": "SKILL.md", "rules": "RULE.md"}
NAME = re.compile(r"[a-z0-9-]{1,64}")


def front_matter(path):
    """The YAML front matter of `path` as a dict, or a problem as a string."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return "doesn't open with YAML front matter (a first line of ---)"
    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        return "front matter has no closing ---"
    try:
        data = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as e:
        return f"front matter isn't valid YAML: {e}".replace("\n", " ")
    if not isinstance(data, dict):
        return "front matter isn't a YAML mapping"
    return data


def check(kind):
    """Problems found in .claude/<kind>/, as strings."""
    file_name = KINDS[kind]
    base = ROOT / ".claude" / kind
    if not base.is_dir():
        return []
    problems = []
    for entry in sorted(base.iterdir()):
        rel = entry.relative_to(ROOT)
        if not entry.is_dir():
            problems.append(f"{rel}: not a folder; expected {base.relative_to(ROOT)}/<name>/{file_name}")
            continue
        if not NAME.fullmatch(entry.name):
            problems.append(f"{rel}: folder name isn't kebab-case (a-z, 0-9, -, at most 64 characters)")
        target = entry / file_name
        if not target.is_file():
            others = [p.name for p in entry.iterdir() if p.name.lower() == file_name.lower()]
            hint = f" (found {others[0]}: the name is case-sensitive)" if others else ""
            problems.append(f"{rel}: no {file_name}{hint}")
            continue
        data = front_matter(target)
        trel = target.relative_to(ROOT)
        if isinstance(data, str):
            problems.append(f"{trel}: {data}")
            continue
        for key in ("name", "description"):
            value = data.get(key)
            if not isinstance(value, str) or not value.strip():
                problems.append(f"{trel}: front matter has no {key}")
        name = data.get("name")
        if isinstance(name, str) and name != entry.name:
            problems.append(f"{trel}: name '{name}' doesn't match its folder '{entry.name}'")
    return problems


def main():
    args = sys.argv[1:]
    if len(args) != 1 or args[0] not in (*KINDS, "all"):
        sys.exit("usage: check-layout.py skills|rules|all")
    kinds = list(KINDS) if args[0] == "all" else args
    problems = [p for kind in kinds for p in check(kind)]
    for p in problems:
        print(p)
    if problems:
        sys.exit(1)
    print("ok")


if __name__ == "__main__":
    main()
