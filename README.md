# `readme-r`: Automatic README Synchronization Skill

A specialized Antigravity skill and companion rule that automatically synchronizes, updates, and creates root and hierarchical `README.md` files whenever code, dependencies, or project structures change.

---

## 🚀 Features

- **Autonomous Self-Execution**: Works with the bundled `rules/readme-sync.md` rule so agents automatically review and synchronize README documentation after making code changes.
- **Hierarchical Documentation**: Manages both root project `README.md` files and modular/nested subfolder READMEs (monorepos, `packages/*`, `services/*`, `skills/*`).
- **Intelligent Contextual Merging**: Preserves existing human branding, prose, and structure while surgically updating features, configuration, usage snippets, and scripts.
- **Fast Change Detection**: Bundles a standalone Python script (`scripts/detect_changes.py`) that analyzes git diffs, package manifests (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`), and project structure.
- **Modern GitHub Standards**: Ships with a comprehensive, professional README template featuring badges, Mermaid architecture diagrams, environment tables, and quick-start guides.

---

## 📁 Package Structure

```text
readme-r/
├── SKILL.md                          # Main skill runbook and procedure instructions
├── scripts/
│   └── detect_changes.py             # Change detection & manifest inspection utility
├── resources/
│   └── standard_template.md          # Comprehensive GitHub README template
├── references/
│   └── doc_guidelines.md             # Contextual merge principles & style guidelines
├── rules/
│   └── readme-sync.md                # Companion rule to enforce automatic execution
└── README.md                         # Skill documentation and setup guide
```

---

## 🛠️ Installation & Setup

### 1. Workspace-Level (Project Specific)
Place the skill and rule inside your project's `.agents/` directory:
```bash
# In your repository root:
mkdir -p .agents/skills/readme-r .agents/rules
cp -r /path/to/readme-r/* .agents/skills/readme-r/
cp .agents/skills/readme-r/rules/readme-sync.md .agents/rules/readme-sync.md
```

### 2. Global-Level (All Projects on Machine)
Install globally in `~/.gemini/config/`:
```bash
mkdir -p ~/.gemini/config/skills/readme-r ~/.gemini/config/rules
cp -r /path/to/readme-r/* ~/.gemini/config/skills/readme-r/
cp ~/.gemini/config/skills/readme-r/rules/readme-sync.md ~/.gemini/config/rules/readme-sync.md
```

---

## 💡 Usage

### Change Detection Helper
To test or manually inspect what the skill detects:
```bash
python3 scripts/detect_changes.py
# Or for JSON output:
python3 scripts/detect_changes.py --json
```

### Automatic Execution
When the `readme-sync.md` rule is active, the agent will automatically run this skill after completing any code change, feature, bug fix, or refactor before finishing the task.

---

## 📄 License
MIT
