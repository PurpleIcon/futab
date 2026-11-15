# General

Project directives for every agent working on FuTab (moved here from AGENTS.md).

- Prefer the agent's own tools for reading, searching and editing files over shell commands
- Ask me with the agent's question tool when you need a clarification or a decision on options for implementation
- VERY IMPORTANT: THE APPLICATION MUST NEVER COLLECT USER DATA, UPLOAD TELEMETRY OR ANY DATA WHATSOEVER
- VERY IMPORTANT: NEVER UPLOAD, COMMIT OR COPY ANY FILE OF THE TEST CORPUS ANYWHERE. THOSE FILES MUST STAY LOCAL ONLY.
- VERY IMPORTANT: THE APPLICATION MUST NEVER UPLOAD OR DOWNLOAD ANY DATA (100% offline), with the exception of scripts, and only when I explicitly ask you to do it
- Try your best to only use rust code in this app. Ask me beforehand if you need to use another language. The exceptions are when you're writing supporting scripts, or when I ask you to automate a task for me. Prefer bash and python in these cases.
- Always credit the source when using 3rd party intellectual property (including code and libs)
- Always prefer to delegate functionality to existing rust libraries. If one doesn't exist in rust, write a port from another language if it exists. If not, write the functionality from scratch.
- Try to keep the application stack and code as lean as possible: avoid having hardcoded options and exceptions - in these cases consider making the feature a plugin, which is only loaded where required
- Always prioritise correctness, reliability and performance in your design. No polling should be used.
- Keep the code clean and maintainable: no hacks or workarounds.
- Keep the code readable. A human will eventually need to understand it. And make it easy for other agents too.
- Remember to update the relevant documentation and the decision records (`docs/adr/`) once we make changes. Keep short and objective inline documentation in the code to facilitate reviewing and debugging.
- Always write it into the project's rules when I tell you to remember something: the matching file in `.claude/rules/`, or AGENTS.md for the session-start steps
- When you learn or discover something worth remembering for this project, ask me if you should add it to the rules
- Always be objective when talking to me: do not be too verbose, only give me the information I need to inform a decision
- When you ask me to test something, give me detailed instructions on how to run it
- Never offer me patches, or ask me to change sections of text or code: give me drop in replacements to avoid confusion
- Always fix both errors AND warnings
- While FuTab is being set up from OxiGuitar (the migration, from November 2026): check your work by building and linting only (`cargo build`, `cargo fmt --all -- --check`, `cargo clippy --workspace --all-targets -- -D warnings`). Don't run the test suites, not even before committing or pushing; run them only when I ask
- Always prefer the simpler approach. If a simple prompt leads to a big change, ask me first.
- The test corpus goes in `corpus/files/` (ignored by git; `corpus/README.md` and `corpus/MANIFEST.toml` say what belongs there)
- When implementing/updating a feature that should be persisted, check compatibility with all File Format plugins
- Never run the app for me, I'll build and run it myself, or else the run might time out mid test
