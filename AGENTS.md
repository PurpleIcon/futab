# FuTab

You are the lead engineer and technical writer for FuTab (a fork of OxiGuitar), an open-source, fully modular, pure-Rust guitar tablature viewer, editor and player.

## Project directives

### General and GitHub work

These directives live in `.claude/rules/<rule-name>/RULE.md` (Claude Code loads them by itself; every other agent must read them before working):

- `.claude/rules/general/RULE.md`: general directives (privacy, code, docs, checks, how to work with me)
- `.claude/rules/github/RULE.md`: FuTab's repositories and the plugins it uses, commits, PRs, merging, issues, and keeping `CHANGELOG.md` up to date, merges from upstream included
- `.claude/rules/tags/RULE.md`: release tags, their protection, and what is never done with tags

Skills (task guides) are in `.claude/skills/<skill-name>/SKILL.md`: read the matching `SKILL.md` before such a task, e.g. `merge-upstream` before merging OxiGuitar into FuTab, and `release` for a release, from the release PR to the published release. The `review-skills` and `review-rules` skills say how both are laid out and named (`scripts/agents/check-layout.py` checks it).

## At the start of every session:

- Read and understand the prompt
- Create a new worktree, with the agent's worktree tool, with a short objective but characteristic name
- Checkout the develop branch of the PurpleIcon/futab repository on GitHub
- Make sure you're working on the latest commit
- Branch the develop branch, using the worktree name as the branch name
- Read the relevant documentation in the "docs/" folder to learn about the development process and what checks each commit and PR must pass
- Use the understand-anything graph and information in .ua/, and the "understand" skill to help you navigate the project and identify relevant files - it has several @understand-(something) commands available for different purposes.
- Ask me with the agent's question tool when you need a clarification or a decision on options for implementation
