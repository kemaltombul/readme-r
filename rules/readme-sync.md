# Rule: Automatic README Synchronization (`readme-sync`)

## Directive
Whenever you modify, add, or refactor code, package dependencies, environment configurations, or project directory structures:
You **MUST** automatically evaluate and update the relevant `README.md` file(s) using the `readme-r` skill before concluding your task or presenting your final response.

---

## When to Trigger
Automatically invoke the `readme-r` skill workflow when any of the following occur during the conversation:
1. **New or Modified Functionality**: New features, updated API routes, CLI arguments, or changed component behaviors.
2. **Dependency & Environment Updates**: Added or removed packages in manifests (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.) or new configuration keys in `.env` / `.env.example`.
3. **Structural Changes**: New submodules, packages, or services created under directories such as `packages/`, `services/`, `apps/`, `skills/`, or `plugins/`.
4. **Bugfixes or Refactors with Behavioral Impact**: Any architectural change altering how developers run, test, build, or deploy the application.

---

## Execution Protocol
1. **Detect Changes**: Run `python3 <skill_path>/scripts/detect_changes.py` or inspect `git status` / `git diff` to identify the full scope of changes.
2. **Contextual Merge**:
   - For existing `README.md` files: Preserve all existing user branding, tone, and untouched sections. Surgically update or insert sections for features, setup, configuration, and usage.
   - For new modules or projects without a README: Generate a comprehensive README using the standard template in `<skill_path>/resources/standard_template.md`.
3. **Hierarchical Scope**: Update the root `README.md`, and if a submodule/package was added or altered, update or create that submodule's local `README.md`.
4. **Preview & Apply**: Save the updated files, verify with `git diff`, and include a clear, concise summary of the updated sections in your final report.

---

## Installation / Activation Options
- **Project-Level**: Place this file in `.agents/rules/readme-sync.md` in the repository root.
- **Global-Level**: Place this file in `~/.gemini/config/rules/readme-sync.md` to automatically apply across all repositories on this machine.
- **Inline**: Append the directive above to `GEMINI.md` or `AGENTS.md`.
