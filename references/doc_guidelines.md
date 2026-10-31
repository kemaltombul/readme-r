# README Documentation & Synchronization Guidelines

This guide outlines principles and protocols for updating and maintaining `README.md` files in existing or new codebases.

---

## 1. Principles of Contextual Merging

When updating an existing `README.md`, do **not** blindly replace the entire file. Human authors often invest significant effort in branding, bespoke tone, special warnings, and custom explanations.

### What to Preserve:
1. **Existing Tone & Voice**: Keep the project's established voice (casual, enterprise, academic, minimal).
2. **Custom Human Badges & Links**: Preserve sponsor links, discord badges, custom CI badges, and author bio sections.
3. **Existing Section Layout**: If the project already places "Installation" before "Features", maintain that existing ordering unless specifically requested to reorganize.
4. **Custom Notes, Warnings & Caveats**: Never overwrite callouts or alert blocks (`> [!WARNING]`, `> [!NOTE]`).

### What to Surgically Update:
1. **Features List**: Append new features or modify existing feature bullets if functionality was altered or expanded.
2. **Installation & Prerequisites**: If new runtimes, CLI tools, or system packages were added (e.g. Docker, Redis, Bun), reflect them in prerequisites.
3. **Environment & Configuration Table**: Check `.env.example` or code configs (`process.env`, `os.environ`) and ensure all new variables are documented with type, default, and purpose.
4. **Usage Snippets**: Ensure code examples match the latest API function signatures, import paths, and command options.
5. **Project / Directory Tree**: If folders or core modules were added, renamed, or restructured, update the directory ASCII tree or Mermaid diagram.
6. **Scripts / Commands**: If `package.json` scripts, `Makefile` targets, or CLI commands were added/removed, sync the command reference table.

---

## 2. Hierarchical Documentation Strategy

For projects with multiple packages, services, or plugins (e.g., monorepos, microservices, skill libraries):

### Root `README.md`:
- **Scope**: Repository-wide picture.
- **Focus**: Overall architecture, workspace tooling (e.g. `lerna`, `turborepo`, `poetry`), how services interact, repository setup instructions, and a directory index linking to sub-modules.
- **Example**:
  ```markdown
  ### Modules & Packages
  - [core](./packages/core): Core business logic and database drivers.
  - [web](./apps/web): Next.js frontend application.
  - [cli](./packages/cli): Developer command-line tool.
  ```

### Submodule / Package `README.md`:
- **Scope**: Specific package or service.
- **Focus**: Dedicated setup, isolated test/run commands, exported package APIs, specific dependencies, and component usage examples.
- **Creation Rule**: Create a new sub-README if a new module or package is introduced under `packages/`, `services/`, `apps/`, `skills/`, or `plugins/`.

---

## 3. High-Impact Writing Standards

- **Active & Imperative Mood**: Use "Run the test suite with `npm test`" instead of "The test suite can be run using...".
- **Real & Tested Code Examples**: Never put pseudo-code or broken imports. Use exact module names and working syntax.
- **Mermaid Diagrams**:
  - Keep diagrams clean and concise (prefer top-to-bottom `graph TD` or left-to-right `graph LR`).
  - Quote labels containing special characters: `client["Client (REST / CLI)"]`.
  - Avoid unnecessary nesting or over-complicated nodes.
- **Tables for Structured Data**: Use GitHub markdown tables for configuration variables, CLI arguments, and API routes.

---

## 4. Verification Checklist Before Saving
- [ ] Are all relative links (`./docs/...`, `./src/...`) valid?
- [ ] Did you preserve existing custom sections that were not affected by the changes?
- [ ] Are code block syntax highlighters specified (`bash`, `typescript`, `python`, `json`, `yaml`)?
- [ ] Are all new environment variables from `.env.example` accounted for?
- [ ] Did you verify the changes using `git diff README.md`?
