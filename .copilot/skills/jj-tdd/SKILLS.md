---
name: jj-tdd-workflow
description: Integrates Test-Driven Development (TDD) with Jujutsu (jj) version control. Use when practicing TDD to create atomic, well-documented commits that capture the Red-Green-Refactor cycle. Each TDD phase becomes a distinct revision with meaningful descriptions.
version_target: "0.36.x"
---

# JJ-TDD: Test-Driven Development with Jujutsu

## Philosophy

TDD and jj are natural partners:

- **TDD phases map to jj revisions** - Each RED/GREEN/REFACTOR step is a distinct, atomic change
- **jj's edit-friendly model** supports iterative refinement
- **Operations log** provides safety net for experimental TDD cycles
- **No staging area** means focus stays on tests and code, not version control mechanics

## TDD Phase Conventions

### Commit Description Format

```
[RED] Add failing test for <feature>

- Test: <test name/description>
- Expected: <expected behavior>
- Actual: Test fails (feature not implemented)
```

```
[GREEN] Implement <feature> to pass test

- Minimal implementation to satisfy test
- Test now passes: <test name>
```

```
[REFACTOR] Clean up <feature> implementation

- Changes: <what was improved>
- All tests still pass
```

## Core Workflow Commands

### Starting a TDD Cycle

```bash
# Create RED phase revision
jj new -m "[RED] Add failing test for user authentication"

# Write your failing test, then verify it fails
# jj auto-snapshots your changes

# Move to GREEN phase
jj new -m "[GREEN] Implement basic user authentication"

# Write minimal code to pass, verify tests pass

# Move to REFACTOR phase
jj new -m "[REFACTOR] Extract authentication logic to separate module"

# Clean up code, ensure tests still pass
```

### Parallel TDD Cycles

When working on independent features simultaneously:

```bash
# Start from common base
jj new --no-edit main -m "[RED] Add failing test for feature A"
jj new --no-edit main -m "[RED] Add failing test for feature B"

# Work on feature A
jj edit <feature-a-change-id>
# ... write test, then continue cycle
```

### Amending TDD Phases

If you need to adjust a phase (jj makes this trivial):

```bash
# Edit any revision in the cycle
jj edit <change-id>

# Make changes (auto-snapshots)
# Or explicitly describe what changed
jj desc -m "[RED] Add failing test for user auth (updated assertions)"
```

## TDD-Specific Revsets

### Find TDD Phases

```bash
# All RED phases (failing tests)
jj log -r 'description(substring-i:"[RED]")'

# All GREEN phases (implementations)
jj log -r 'description(substring-i:"[GREEN]")'

# All REFACTOR phases
jj log -r 'description(substring-i:"[REFACTOR]")'

# Your recent TDD work
jj log -r 'mine() & description(substring-i:"[RED]") | description(substring-i:"[GREEN]") | description(substring-i:"[REFACTOR]")'

# Incomplete TDD cycles (RED without following GREEN)
jj log -r 'description(substring-i:"[RED]") & ~parents(description(substring-i:"[GREEN]"))'
```

### Navigate TDD History

```bash
# Show the full TDD cycle for a feature
jj log -r '::@ & description(substring-i:"authentication")'

# View evolution of a TDD phase
jj evolog -r <red-phase-change-id> -p
```

## TDD Cycle Management

### Squash Completed Cycles

After a successful TDD cycle, optionally squash into a single feature commit:

```bash
# Squash RED+GREEN+REFACTOR into one commit
jj squash --from <red-change-id> --into <refactor-change-id>
jj desc -r <refactor-change-id> -m "feat: Add user authentication

TDD cycle complete:
- Added comprehensive auth tests
- Implemented JWT-based authentication
- Refactored into AuthService module"
```

### Split Oversized Phases

If a phase grew too large:

```bash
# Split a GREEN phase that implemented too much
jj split -r <green-change-id> src/auth.rs -m "[GREEN] Implement password validation"
# Remaining changes stay in original with updated description
```

### Abandon Failed Experiments

```bash
# Abandon a TDD cycle that didn't work out
jj abandon <red-change-id>::<refactor-change-id>

# Or restore to before the experiment
jj op log
jj op restore <op-id-before-experiment>
```

## Integration with Test Runners

### Verify TDD Phases

```bash
# After RED phase - tests SHOULD fail
cargo test 2>&1 | grep -q "FAILED" && echo "✓ RED phase valid"

# After GREEN phase - tests SHOULD pass
cargo test && echo "✓ GREEN phase valid"

# After REFACTOR - tests MUST still pass
cargo test && echo "✓ REFACTOR phase valid"
```

### Bisect for Test Regressions

```bash
# Find which TDD phase broke tests
jj bisect run -- cargo test --lib
```

## Templates for TDD Logging

### Compact TDD Log

```bash
jj log -r 'mine()' -T '
  separate(" ",
    change_id.shortest(8),
    if(description.first_line().starts_with("[RED]"), "🔴",
      if(description.first_line().starts_with("[GREEN]"), "🟢",
        if(description.first_line().starts_with("[REFACTOR]"), "🔵", "⚪")
      )
    ),
    description.first_line().substr(0, 60),
  ) ++ "\n"
'
```

### TDD Phase Summary

```bash
jj log -r '@::' -T '
  if(description.first_line().starts_with("[RED]") ||
     description.first_line().starts_with("[GREEN]") ||
     description.first_line().starts_with("[REFACTOR]"),
    separate(" | ",
      change_id.shortest(6),
      description.first_line(),
      if(conflict, "⚠️ CONFLICT", ""),
    ) ++ "\n",
    ""
  )
'
```

## Best Practices

### 1. One Test Per RED Phase

```bash
# ✅ Focused RED phase
jj new -m "[RED] Add test for email validation format"

# ❌ Too broad
jj new -m "[RED] Add tests for user validation"
```

### 2. Minimal GREEN Implementations

```bash
# ✅ Just enough to pass
jj new -m "[GREEN] Return hardcoded valid response for email check"

# ❌ Over-engineering in GREEN
jj new -m "[GREEN] Implement full RFC 5322 email parser with extensions"
```

### 3. Meaningful REFACTOR Descriptions

```bash
# ✅ Specific refactoring
jj new -m "[REFACTOR] Extract email regex to constants module"

# ❌ Vague
jj new -m "[REFACTOR] Clean up code"
```

### 4. Use Bookmarks for Feature Branches

```bash
# Create bookmark for TDD feature work
jj bookmark create auth-feature -r @

# Push completed TDD cycle
jj git push -b auth-feature
```

### 5. Checkpoint Before Complex Refactors

```bash
# Record current state before risky refactor
jj op log -l 1  # Note the operation ID

# If refactor breaks tests
jj op restore <safe-op-id>
```

## Recovery Scenarios

### Tests Broke During Refactor

```bash
# Option 1: Undo the refactor changes
jj undo

# Option 2: Restore specific files from GREEN phase
jj restore --from <green-change-id> src/auth.rs

# Option 3: Full operation restore
jj op restore <op-before-refactor>
```

### Wrong Phase Committed

```bash
# Realized GREEN work went into RED phase
jj split -r <red-change-id> src/auth.rs -m "[GREEN] Implement auth"
# Original RED phase keeps only test files
```

### Need to Insert Missing Phase

```bash
# Insert GREEN between existing RED and REFACTOR
jj new -A <red-change-id> -m "[GREEN] Implement feature"
# This inserts after RED, rebasing REFACTOR on top
```

## Quick Reference

| Action             | Command                                      |
| ------------------ | -------------------------------------------- | --------- | -------------- |
| Start RED          | `jj new -m "[RED] Add failing test for X"`   |
| Start GREEN        | `jj new -m "[GREEN] Implement X"`            |
| Start REFACTOR     | `jj new -m "[REFACTOR] Clean up X"`          |
| View TDD phases    | `jj log -r 'description(substring-i:"[RED]\\ | [GREEN]\\ | [REFACTOR]")'` |
| Amend phase        | `jj edit <id>` then make changes             |
| Squash cycle       | `jj squash --from <red> --into <refactor>`   |
| Undo last action   | `jj undo`                                    |
| Verify test status | `cargo test` / `pytest` / `npm test`         |

## See Also

- `working-with-jj` skill for comprehensive jj reference
- `jj help -k revsets` for revset syntax
- TDD dataflow diagram in `tdd-dataflow.d2`
