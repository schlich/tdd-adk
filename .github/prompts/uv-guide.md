---
mode: agent
description: Guide for using uv for Python dependency management in this project
tools:
  - read_file
  - run_in_terminal
  - list_dir
---

# Using uv for Python Dependency Management

This project uses [uv](https://github.com/astral-sh/uv) for fast, reliable Python package management.

## Quick Reference

### Installation & Setup
```bash
# Install dependencies (reads from pyproject.toml and uv.lock)
uv sync

# Install with dev dependencies
uv sync --all-extras

# Install a new package
uv add <package-name>

# Install a dev dependency
uv add --dev <package-name>
```

### Running Commands
```bash
# Run Python scripts
uv run python script.py

# Run module
uv run python -m tdd_eval.cli examples/simple_tdd_cycle.json

# Run pytest
uv run pytest tests/ -v

# Run linter
uv run ruff check .
uv run ruff format .
```

### Development Workflow
```bash
# Update dependencies
uv lock

# Upgrade specific package
uv add <package-name> --upgrade

# Remove a package
uv remove <package-name>

# Show installed packages
uv pip list
```

## Integration with Nix

This project uses `uv2nix` to integrate uv with Nix:

```bash
# Enter development shell (includes uv)
nix develop

# Build the Python package with Nix
nix build .#tdd-eval

# Run in Nix environment
nix develop --command uv run pytest
```

## Key Files

- **pyproject.toml** - Project metadata and dependency specifications
- **uv.lock** - Locked dependency versions (commit this file)
- **.python-version** - Python version specification for uv
- **flake.nix** - Nix integration with uv2nix

## Why uv?

- ⚡ **Fast**: 10-100x faster than pip
- 🔒 **Reliable**: Lock file ensures reproducible installs
- 🎯 **Simple**: Single tool for package management
- 🔄 **Compatible**: Works with existing pyproject.toml
- 🦀 **Modern**: Written in Rust for performance

## Common Tasks

### Adding a New Dependency
```bash
# Add runtime dependency
uv add pydantic-ai

# Add dev dependency
uv add --dev pytest

# Update lock file
uv lock
```

### Running Tests
```bash
# All tests
uv run pytest

# Specific test file
uv run pytest tests/test_models.py -v

# With coverage
uv run pytest --cov=src/tdd_eval tests/
```

### Code Quality
```bash
# Format code
uv run ruff format .

# Check linting
uv run ruff check .

# Auto-fix linting issues
uv run ruff check --fix .
```

## Troubleshooting

### Lock File Out of Sync
If you see errors about the lock file being out of sync:
```bash
uv lock --upgrade
```

### Python Version Issues
Ensure you have Python 3.11+ installed:
```bash
python --version
# or via Nix
nix develop --command python --version
```

### Clean Install
To do a fresh install:
```bash
rm -rf .venv
uv sync --all-extras
```

## References

- [uv Documentation](https://github.com/astral-sh/uv)
- [uv2nix GitHub](https://github.com/adisbladis/uv2nix)
- [PEP 621 - pyproject.toml](https://peps.python.org/pep-0621/)
