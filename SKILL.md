---
name: readme-r
description: >-
  Use this skill automatically after completing any code change, feature addition,
  bugfix, refactor, dependency update, or project restructuring, or whenever the user
  asks to create, update, or synchronize root and hierarchical README.md file(s).
---

# `readme-r`: Automatic README Synchronization Skill

This skill guides the agent through an intelligent, safe, and structured workflow for generating, updating, and synchronizing project `README.md` files after making code changes. It ensures repository documentation never becomes stale, preserves existing custom prose and structure, maintains hierarchical subfolder READMEs, and presents a clear summary of updates.

---

## Workflow Steps

### Step 1: Run Change Detection

Execute the bundled change detector script to inspect repository modifications, git diffs, package manifests, and changed modules:

```bash
python3 scripts/detect_changes.py
# (Or: python3 ~/.gemini/config/skills/readme-r/scripts/detect_changes.py)
# (Or: python3 .agents/skills/readme-r/scripts/detect_changes.py)
```

For automated JSON parsing:
```bash
python3 scripts/detect_changes.py --json
```

**Key Information to Extract:**
1. **Modified Files**: What specific features, routes, components, or utilities were touched?
2. **Dependency Manifests**: Were packages added or removed in `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.?
3. **Environment Changes**: Were new environment variables introduced in `.env`, `.env.example`, or configuration files?
4. **Target README Locations**: Determine whether updates affect the root `README.md`, sub-module READMEs, or both.

---

### Step 2: Target README Resolution

Consult the [Documentation Guidelines](./references/doc_guidelines.md) for hierarchical rules:

1. **Root README**:
   - Path: `README.md` in repository root.
   - Purpose: Project high-level architecture, primary features, installation prerequisites, global configuration, and module directory map.
2. **Hierarchical Sub-READMEs**:
   - Paths: `<submodule>/README.md` (e.g. `packages/<pkg>/README.md`, `services/<svc>/README.md`, `apps/<app>/README.md`, `skills/<skill>/README.md`).
   - Purpose: Package-specific APIs, local commands, isolated setup, and scoped examples.
   - **Rule**: If a new submodule, package, or service was created, generate a dedicated `README.md` in that folder. If an existing submodule was altered, update its local `README.md`.

---

### Step 3: Contextual Merging & Drafting

#### Scenario A: Existing `README.md` (Intelligent Contextual Merge)
Do **not** overwrite the whole file. Follow the contextual merge protocol in [doc_guidelines.md](./references/doc_guidelines.md):
- **Preserve**: Keep project title, branding, badges, mission statement, custom callouts, existing ordering, and untouched sections.
- **Update / Insert**:
  - **Features**: Append bullet points for new capabilities; update descriptions for modified behaviors.
  - **Quick Start / Prerequisites**: Update runtime versions or required dependencies if new ones were introduced.
  - **Usage & Examples**: Update or add realistic code snippets demonstrating new functions, CLI flags, or API endpoints.
  - **Configuration**: Synchronize the environment variables table with `.env.example`.
  - **Scripts & Commands**: Add any new npm/cargo/poetry scripts or Makefile targets.
  - **Architecture / Directory Tree**: Update file tree or Mermaid diagram if new directories were created.

#### Scenario B: New or Missing `README.md`
If no README exists, use the [Comprehensive Modern GitHub Template](./resources/standard_template.md) as the blueprint. Populate:
- Project title, concise tagline, and status badges.
- Core features and problem statement.
- Architecture diagram (`mermaid`) and directory structure.
- Prerequisites, step-by-step installation, and environment setup.
- Working usage examples with syntax-highlighted code blocks.
- Configuration table and development/testing commands.
- License information.

---

### Step 4: Apply Updates & Verify Diffs

1. Use `replace_file_content` or `write_to_file` to write the updated content.
2. Run `git diff` on the target README file(s) to verify:
   ```bash
   git diff README.md
   ```
3. Check that:
   - Formatting and markdown syntax are clean and valid.
   - Code blocks have proper language tags (`bash`, `typescript`, `python`, `json`, etc.).
   - All relative links and anchors are intact.

---

### Step 5: Report Summary to User

Following the **Preview & Apply** approach:
1. Provide a concise, bulleted summary of the sections that were updated or created.
2. Highlight any newly documented environment variables, commands, or API features.
3. Show a brief diff excerpt or section preview so the user can quickly confirm the documentation matches their expectations.

---

## Automatic Enforcement

To ensure this skill runs automatically whenever code changes occur, install the companion rule:
- Copy [rules/readme-sync.md](./rules/readme-sync.md) to `.agents/rules/readme-sync.md` (for the current project) or `~/.gemini/config/rules/readme-sync.md` (for global enforcement).
