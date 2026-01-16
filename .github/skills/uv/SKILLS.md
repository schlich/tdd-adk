# uv Python Package Manager Skill

## Overview

This project uses **uv** for Python package management, providing fast, reliable dependency resolution and installation.

## Installation

uv is available in the Nix development shell:
```bash
nix develop
```

Or install globally:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Core Commands

### Project Setup
```bash
# Initialize a new project (already done for this project)
uv init

# Install all dependencies from lock file
uv sync

# Install with all optional dependencies (dev, test, etc.)
uv sync --all-extras
```

### Managing Dependencies
```bash
# Add a runtime dependency
uv add <package-name>

# Add a development dependency
uv add --dev <package-name>

# Add with version constraint
uv add "pydantic>=2.0.0"

# Remove a dependency
uv remove <package-name>

# Upgrade a specific package
uv add <package-name> --upgrade

# Upgrade all packages
uv lock --upgrade
```

### Running Code
```bash
# Run a Python script
uv run python script.py

# Run a module
uv run python -m tdd_eval.cli

# Run pytest
uv run pytest

# Run with arguments
uv run pytest tests/test_models.py -v
```

### Lock File Management
```bash
# Update lock file after changing pyproject.toml
uv lock

# Upgrade all dependencies to latest compatible versions
uv lock --upgrade

# Verify lock file is in sync
uv sync --locked
```

## Project Structure

- **pyproject.toml** - Project metadata, dependencies, and build configuration
- **uv.lock** - Locked dependency versions (always commit this)
- **.python-version** - Python version for uv to use
- **.venv/** - Virtual environment (gitignored)

## Workflow Integration

### With Git
```bash
# Always commit the lock file
git add uv.lock pyproject.toml
git commit -m "Update dependencies"
```

### With Nix
This project uses `uv2nix` for Nix integration:
```bash
# Build with Nix
nix build .#tdd-eval

# Development shell includes uv
nix develop
```

### With CI/CD
GitHub Actions workflows use uv:
- `.github/workflows/ci.yml` - Main CI with uv
- `.github/workflows/prek.yml` - Pre-commit hooks with uv

## Common Workflows

### Adding a New Feature with Dependencies
```bash
# Add the dependency
uv add new-package

# Update lock file (happens automatically)
# Verify it works
uv run python -c "import new_package; print('OK')"

# Commit changes
git add pyproject.toml uv.lock
git commit -m "Add new-package dependency"
```

### Updating Dependencies
```bash
# Update a specific package
uv add package-name --upgrade

# Or update all packages
uv lock --upgrade

# Test the updates
uv run pytest

# Commit if all tests pass
git add uv.lock
git commit -m "Update dependencies"
```

### Reproducing an Environment
```bash
# Clean install from lock file
rm -rf .venv
uv sync --locked

# Verify
uv run pytest
```

## Performance Benefits

- **Speed**: 10-100x faster than pip
- **Reliability**: Lock file ensures reproducible installs
- **Simplicity**: Single tool replaces pip, pip-tools, virtualenv
- **Compatibility**: Works with standard pyproject.toml

## Troubleshooting

### "Lock file is not up-to-date"
```bash
uv lock
```

### "Cannot find Python"
Check `.python-version` file or set explicitly:
```bash
uv python install 3.12
```

### Virtual Environment Issues
```bash
# Remove and recreate
rm -rf .venv
uv sync --all-extras
```

### Dependency Conflicts
```bash
# See resolution details
uv add package-name --verbose

# Try with different version constraints
uv add "package-name>=1.0,<2.0"
```

## Best Practices

1. **Always commit uv.lock** - Ensures reproducible builds
2. **Use `uv sync --locked` in CI** - Fails if lock file is out of sync
3. **Pin Python version** in `.python-version`
4. **Use `uv run`** instead of activating virtual environment
5. **Update regularly** but test after updates

## Resources

- [uv GitHub](https://github.com/astral-sh/uv)
- [uv Documentation](https://docs.astral.sh/uv/)
- [uv2nix Integration](https://github.com/adisbladis/uv2nix)
- [PEP 621 - pyproject.toml](https://peps.python.org/pep-0621/)
