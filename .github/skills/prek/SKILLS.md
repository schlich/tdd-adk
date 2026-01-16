---
name: prek-quality-checks
description: Pre-commit hook management using prek (Rust-based pre-commit alternative). Use for code quality validation, formatting checks, and ensuring clean commits. Works alongside jj workflows since jj auto-snapshots the working copy.
version_target: "0.2.x"
---

# Prek Pre-Commit Hooks

## Overview

[prek](https://prek.j178.dev/) is a faster, Rust-based reimplementation of pre-commit. It's fully compatible with `.pre-commit-config.yaml` files and provides:

- 🚀 Single binary, no Python dependency
- ⚡ Faster execution with parallel hook runs
- 🔄 Full pre-commit config compatibility
- 📦 Built-in Rust-native hooks (offline, zero setup)

## Integration with Jujutsu (jj)

Since jj doesn't have native pre-commit hook support, prek is run **manually** before pushing or as part of the workflow:

```bash
# Before pushing to remote
prek run --all-files && jj git push

# Quick check on working copy changes
prek run

# Check files in a specific jj revision (export then check)
jj diff -r <rev> --summary | awk '{print $2}' | xargs prek run --files
```

### Why Manual Instead of Hooks?

jj's architecture differs from git:
- **Auto-snapshotting**: jj continuously snapshots the working copy
- **No staging area**: There's no "pre-commit" moment like in git
- **Colocated repos**: While `.git` hooks exist, they may not trigger for jj operations

**Best practice**: Run `prek` explicitly before `jj git push` or integrate into your editor/CI.

## Essential Commands

```bash
# Run on staged/modified files (default)
prek run

# Run on all files in repo
prek run --all-files

# Run specific hooks
prek run trailing-whitespace check-yaml

# Run manual-stage hooks (tests, comprehensive checks)
prek run --hook-stage manual

# Run on files from last commit
prek run --last-commit

# Run on specific directory
prek run --directory src/

# Skip specific hooks
PREK_SKIP=nix-fmt prek run
# or
prek run --skip nix-fmt

# Dry run (show what would run)
prek run --dry-run

# List all configured hooks
prek list

# Validate configuration
prek validate-config
```

## Project Hooks

Our `.pre-commit-config.yaml` includes:

### Built-in Fast Hooks (Rust-native)
| Hook | Purpose |
|------|---------|
| `trailing-whitespace` | Remove trailing whitespace |
| `end-of-file-fixer` | Ensure files end with newline |
| `check-yaml` | Validate YAML syntax |
| `check-toml` | Validate TOML syntax |
| `check-json` | Validate JSON syntax |

### Standard Hooks
| Hook | Purpose |
|------|---------|
| `check-merge-conflict` | Detect unresolved merge markers |
| `check-added-large-files` | Prevent committing large files (>500KB) |
| `detect-private-key` | Prevent committing private keys |
| `check-case-conflict` | Detect case-insensitive filename conflicts |

### Project-Specific Hooks
| Hook | Purpose |
|------|---------|
| `d2-validate` | Format and validate D2 diagrams |
| `nix-fmt` | Format Nix files with alejandra |

### Manual Stage Hooks
| Hook | Purpose |
|------|---------|
| `check-all` | Run all hooks on entire codebase |

## TDD Integration

Combine prek with TDD workflow:

```bash
# Before GREEN phase: ensure code quality
prek run

# After REFACTOR phase: full validation
prek run --all-files

# Before pushing TDD cycle
prek run --all-files && jj git push -b feature-branch
```

### Adding Test Hooks

For test-focused hooks, add to manual stage:

```yaml
- repo: local
  hooks:
    - id: pytest
      name: Run tests
      language: system
      entry: pytest -xvs
      pass_filenames: false
      always_run: true
      stages: [manual]
```

Then run with: `prek run --hook-stage manual`

## Troubleshooting

### Hook Failed - View Output
```bash
prek run --show-diff-on-failure
```

### Check Hook Environments
```bash
prek cache dir        # Show cache location
prek cache clean      # Clear all caches
prek cache gc         # Remove unused caches
```

### Debug Hook Execution
```bash
prek run -v           # Verbose output
prek run -vv          # Very verbose
```

### Skip Hooks Temporarily
```bash
# Via environment variable
PREK_SKIP=hook1,hook2 prek run

# Via CLI
prek run --skip hook1 --skip hook2
```

## CI Integration

For GitHub Actions:

```yaml
- uses: j178/prek-action@v1
  # or manually:
- run: |
    curl -fsSL https://prek.j178.dev/install.sh | sh
    prek run --all-files
```

## Configuration Reference

Key config options in `.pre-commit-config.yaml`:

```yaml
# Require minimum prek version
minimum_prek_version: '0.2.0'

# Global file filters
files: '.*'
exclude: '^vendor/'

# Stop on first failure
fail_fast: false

# Default stages for all hooks
default_stages: [pre-commit]
```

Hook-level options:

```yaml
hooks:
  - id: my-hook
    name: Display name
    entry: command to run
    language: system|python|node|rust|...
    files: '\.py$'              # Regex filter
    exclude: 'test_.*\.py$'     # Regex exclude
    types: [python]             # File type filter
    pass_filenames: true        # Pass matched files to command
    always_run: false           # Run even if no files match
    stages: [pre-commit]        # When to run
    priority: 0                 # Execution order (lower = earlier)
```

## See Also

- [prek documentation](https://prek.j178.dev/)
- [Pre-commit hooks reference](https://pre-commit.com/hooks.html)
- `.github/prompts/prek-check.md` for the agent prompt
- `.github/skills/jj-tdd/SKILLS.md` for jj+TDD workflow
