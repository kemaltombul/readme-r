#!/usr/bin/env python3
"""
detect_changes.py - Repository & Codebase Change Detector for README Updates.

Analyzes working tree modifications, git diffs, package manifests, and project
structure to report what functionality, dependencies, or interfaces changed and
identify candidate README.md files requiring updates.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


def run_cmd(cmd: List[str], cwd: Optional[Path] = None) -> str:
    """Run a shell command and return stdout as string."""
    try:
        res = subprocess.run(
            cmd,
            cwd=cwd or Path.cwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        return res.stdout.strip()
    except Exception:
        return ""


def is_git_repo(repo_path: Path) -> bool:
    """Check if target path is inside a git repository."""
    out = run_cmd(["git", "rev-parse", "--is-inside-work-tree"], cwd=repo_path)
    return out == "true"


def get_git_status_files(repo_path: Path) -> Dict[str, List[str]]:
    """Return categorized files from git status."""
    st_output = run_cmd(["git", "status", "--porcelain"], cwd=repo_path)
    modified = []
    added = []
    deleted = []
    untracked = []

    for line in st_output.splitlines():
        if not line or len(line) < 3:
            continue
        status_code = line[:2]
        filepath = line[3:].strip()
        # Handle rename syntax 'old -> new'
        if " -> " in filepath:
            filepath = filepath.split(" -> ")[1].strip()

        if "?" in status_code:
            untracked.append(filepath)
        elif "A" in status_code:
            added.append(filepath)
        elif "D" in status_code:
            deleted.append(filepath)
        else:
            modified.append(filepath)

    return {
        "modified": modified,
        "added": added,
        "deleted": deleted,
        "untracked": untracked,
    }


def get_recent_git_diff(repo_path: Path, max_lines: int = 500) -> str:
    """Extract diff summary from working tree or latest commit."""
    # First attempt: unstaged + staged diff
    diff = run_cmd(["git", "diff", "HEAD"], cwd=repo_path)
    if not diff:
        diff = run_cmd(["git", "diff", "--cached"], cwd=repo_path)
    if not diff:
        # Check last commit diff
        diff = run_cmd(["git", "diff", "HEAD~1", "HEAD"], cwd=repo_path)

    lines = diff.splitlines()
    if len(lines) > max_lines:
        return "\n".join(lines[:max_lines]) + f"\n... [diff truncated, total {len(lines)} lines]"
    return diff


def inspect_manifests(repo_path: Path) -> Dict[str, Any]:
    """Inspect ecosystem manifests (package.json, pyproject.toml, Cargo.toml, go.mod)."""
    manifest_info: Dict[str, Any] = {}

    # Node.js
    pkg_json = repo_path / "package.json"
    if pkg_json.exists():
        try:
            with open(pkg_json, "r", encoding="utf-8") as f:
                data = json.load(f)
            manifest_info["nodejs"] = {
                "name": data.get("name"),
                "version": data.get("version"),
                "description": data.get("description"),
                "scripts": list(data.get("scripts", {}).keys()),
                "dependencies": list(data.get("dependencies", {}).keys()),
                "devDependencies": list(data.get("devDependencies", {}).keys()),
                "bin": data.get("bin"),
            }
        except Exception as e:
            manifest_info["nodejs"] = {"error": str(e)}

    # Python pyproject.toml
    pyproject = repo_path / "pyproject.toml"
    if pyproject.exists():
        try:
            content = pyproject.read_text(encoding="utf-8")
            scripts = re.findall(r"(\w[\w.-]*)\s*=\s*[\"'][\w.:]+[\"']", content)
            deps = re.findall(r"[\"']([a-zA-Z0-9_\-\[\]]+)(?:[><=~^!].*)?[\"']", content)
            manifest_info["python"] = {
                "path": "pyproject.toml",
                "detected_scripts": scripts[:10],
                "sample_dependencies": deps[:15],
            }
        except Exception as e:
            manifest_info["python"] = {"error": str(e)}

    # Rust Cargo.toml
    cargo = repo_path / "Cargo.toml"
    if cargo.exists():
        try:
            content = cargo.read_text(encoding="utf-8")
            pkg_name_match = re.search(r'name\s*=\s*"([^"]+)"', content)
            pkg_name = pkg_name_match.group(1) if pkg_name_match else None
            manifest_info["rust"] = {
                "path": "Cargo.toml",
                "package_name": pkg_name,
            }
        except Exception as e:
            manifest_info["rust"] = {"error": str(e)}

    # Go go.mod
    gomod = repo_path / "go.mod"
    if gomod.exists():
        try:
            content = gomod.read_text(encoding="utf-8")
            module_match = re.search(r"module\s+([^\s]+)", content)
            manifest_info["go"] = {
                "path": "go.mod",
                "module": module_match.group(1) if module_match else None,
            }
        except Exception as e:
            manifest_info["go"] = {"error": str(e)}

    return manifest_info


def find_target_readmes(repo_path: Path, changed_files: List[str]) -> Dict[str, Any]:
    """Find root README and any module/subpackage READMEs affected by changes."""
    root_readme = None
    for candidate in ["README.md", "readme.md", "README", "readme"]:
        if (repo_path / candidate).exists():
            root_readme = str(repo_path / candidate)
            break

    sub_readmes: Dict[str, Dict[str, Any]] = {}
    
    # Check all existing READMEs in subdirectories
    for root, dirs, files in os.walk(repo_path):
        # Skip hidden and dependency folders
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("node_modules", "vendor", "dist", "build", "target", "__pycache__")]
        current_dir = Path(root)
        if current_dir == repo_path:
            continue
        
        for f in files:
            if f.lower() == "readme.md":
                rel_dir = str(current_dir.relative_to(repo_path))
                sub_readmes[rel_dir] = {
                    "path": str(current_dir / f),
                    "exists": True,
                    "changed_files_in_dir": []
                }

    # Group changed files into directories to detect submodules needing a new or updated README
    for file_str in changed_files:
        p = Path(file_str)
        parent_dir = str(p.parent)
        top_folder = p.parts[0] if len(p.parts) > 1 else ""

        # Map to existing sub_readme
        for r_dir in sub_readmes:
            if file_str.startswith(r_dir + "/") or file_str == r_dir:
                sub_readmes[r_dir]["changed_files_in_dir"].append(file_str)

        # If it's a modular directory (e.g. packages/foo, services/bar, apps/web) without a README
        if top_folder in ("packages", "services", "apps", "plugins", "modules", "libs", "skills"):
            if len(p.parts) >= 2:
                module_dir = os.path.join(p.parts[0], p.parts[1])
                if module_dir not in sub_readmes and (repo_path / module_dir).is_dir():
                    sub_readmes[module_dir] = {
                        "path": str(repo_path / module_dir / "README.md"),
                        "exists": (repo_path / module_dir / "README.md").exists(),
                        "changed_files_in_dir": [file_str]
                    }

    return {
        "root_readme": {
            "path": root_readme or str(repo_path / "README.md"),
            "exists": root_readme is not None,
        },
        "hierarchical_readmes": sub_readmes,
    }


def analyze_repository(repo_path: Path) -> Dict[str, Any]:
    """Run comprehensive analysis on repo changes."""
    is_git = is_git_repo(repo_path)
    git_status = get_git_status_files(repo_path) if is_git else {"modified": [], "added": [], "deleted": [], "untracked": []}
    
    all_changed_files = (
        git_status["modified"]
        + git_status["added"]
        + git_status["untracked"]
    )
    
    diff_snippet = get_recent_git_diff(repo_path) if is_git else ""
    manifests = inspect_manifests(repo_path)
    readme_targets = find_target_readmes(repo_path, all_changed_files)

    # Classify types of changes detected
    has_dep_changes = any(
        f.endswith(("package.json", "pyproject.toml", "Cargo.toml", "go.mod", "requirements.txt", "Gemfile"))
        for f in all_changed_files
    )
    has_new_files = bool(git_status["added"] or git_status["untracked"])
    has_config_changes = any(
        f.endswith((".env.example", "tsconfig.json", "docker-compose.yml", "Dockerfile", ".yml", ".yaml"))
        for f in all_changed_files
    )
    
    summary = {
        "is_git_repository": is_git,
        "total_changed_files": len(all_changed_files),
        "changed_files": all_changed_files,
        "git_status": git_status,
        "has_dependency_changes": has_dep_changes,
        "has_new_files_or_modules": has_new_files,
        "has_configuration_changes": has_config_changes,
        "target_readmes": readme_targets,
        "manifests": manifests,
        "diff_snippet": diff_snippet[:2000] if diff_snippet else "No git diff available.",
    }
    return summary


def main():
    parser = argparse.ArgumentParser(description="Detect code changes for README synchronization.")
    parser.add_argument("--path", type=str, default=".", help="Root path of repository (default: current working directory)")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    target_path = Path(args.path).resolve()
    data = analyze_repository(target_path)

    if args.json:
        print(json.dumps(data, indent=2))
        return

    print("=" * 60)
    print(f"README Change Detection Summary: {target_path}")
    print("=" * 60)
    print(f"Git Repository: {data['is_git_repository']}")
    print(f"Total Modified/New Files: {data['total_changed_files']}")
    print(f"Dependency Manifest Changes: {data['has_dependency_changes']}")
    print(f"Configuration Changes: {data['has_configuration_changes']}")
    print(f"New Modules/Files: {data['has_new_files_or_modules']}")
    print("\n--- Target READMEs ---")
    root_rm = data['target_readmes']['root_readme']
    print(f"Root README: {root_rm['path']} (Exists: {root_rm['exists']})")
    
    hier_rms = data['target_readmes']['hierarchical_readmes']
    if hier_rms:
        print(f"Hierarchical Sub-READMEs ({len(hier_rms)} detected):")
        for dir_name, info in hier_rms.items():
            print(f"  - [{dir_name}] -> {info['path']} (Exists: {info['exists']}, Relevant files: {len(info['changed_files_in_dir'])})")
    else:
        print("Hierarchical Sub-READMEs: None detected")

    if data['changed_files']:
        print("\n--- Sample Changed Files ---")
        for f in data['changed_files'][:15]:
            print(f"  * {f}")
        if len(data['changed_files']) > 15:
            print(f"  ... and {len(data['changed_files']) - 15} more")

    print("\n[Recommendation] Proceed to draft or update sections based on detected changes.")


if __name__ == "__main__":
    main()
