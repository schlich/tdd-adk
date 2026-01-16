---
mode: agent
description: Run prek pre-commit hooks to validate code quality, formatting, and catch issues before committing
tools:
  - run_in_terminal
  - read_file
  - list_dir
---

# Prek Quality Check

Run pre-commit hooks using prek to validate code quality.

## Context

$SELECTION

## Instructions

### Quick Check (Staged Files)

Run basic hooks on currently modified files:

```bash
prek run
```

### Full Check (All Files)

Run all hooks on the entire codebase:

```bash
prek run --all-files
```

### Manual Stage (Including Tests)

Run hooks including those in the manual stage:

```bash
prek run --hook-stage manual
```

### Check Output

When hooks run:
- ✅ **Passed**: Hook completed successfully
- ❌ **Failed**: Hook found issues
- ⚠️ **Skipped**: Hook didn't apply to any files

### Common Fixes

**Trailing whitespace / End of file:**
```bash
# Auto-fixed by the hook, just re-run
prek run
```

**YAML/TOML/JSON syntax errors:**
```bash
# Check the file for syntax issues
cat problematic-file.yaml
```

**D2 diagram validation:**
```bash
# Check D2 syntax manually
d2 fmt file.d2
d2 file.d2 /dev/null
```

### Skipping Hooks Temporarily

```bash
# Skip specific hooks
PREK_SKIP=trailing-whitespace prek run

# Skip via CLI
prek run --skip nix-fmt
```

## Output Format

Report results in this format:

### Prek Quality Check Results

**Command Run:** `prek run [options]`

**Results:**

| Hook | Status | Notes |
|------|--------|-------|
| trailing-whitespace | ✅ Passed | |
| end-of-file-fixer | ✅ Passed | |
| check-yaml | ✅ Passed | |

**Issues Found:** [List any failed hooks and what to fix]

**Summary:** Total: X, Passed: X, Failed: X, Skipped: X

## Rules
- Always report hook output
- For failures, suggest specific fixes
- Note if hooks auto-fixed any issues
