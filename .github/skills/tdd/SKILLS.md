---
name: tdflow-tdd
description: TDFlow-inspired Test-Driven Development workflow. Use when implementing features test-first, debugging failing tests, or resolving issues with existing test suites. Applies agentic decomposition to separate exploration, debugging, and patching concerns.
---

# TDFlow: Agentic Test-Driven Development

## Overview

TDFlow is a test-driven agentic workflow that frames software engineering as a **test-resolution task**. Instead of generating code from vague descriptions, TDFlow focuses on solving concrete, executable tests.

## Core Principle

> "The primary bottleneck to human-level software engineering performance lies within writing tests rather than solving them."

When provided with well-written tests, AI achieves 94%+ success rates. Focus your effort on writing good tests; let AI handle the implementation.

## London-Style TDD (Top-Down)

This workflow uses **London-style (outside-in) TDD**:

```
Outside-In Order:
┌─────────────────────────────────────┐
│     Acceptance Tests (Start Here)   │  ← User behavior
│  ┌───────────────────────────────┐  │
│  │    Integration Tests          │  │  ← Component contracts
│  │  ┌─────────────────────────┐  │  │
│  │  │    Unit Tests           │  │  │  ← Implementation details
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

**Key Workflow:**
1. **Plan first**: Map ALL tests before writing any
2. **One test per cycle**: Generate → Fail → Implement → Pass → Refactor → Next
3. **Outside-in**: Start with acceptance tests, work inward

## The Five Sub-Agents

### 0. Plan Tests Agent (NEW - Use First)

**Purpose**: Map out all tests before writing any

**Process**:
1. Analyze feature request
2. Create layered test map (acceptance → integration → unit)
3. Identify dependencies to mock
4. Prioritize test order (outside-in)

**Output**: A comprehensive test plan, NOT actual test code

### 1. Explore Files Agent

**Purpose**: Navigate codebase and propose patches

**Allowed Actions**:
- View file contents
- Search for keywords/patterns
- Browse folder structure
- Analyze test error messages

**Forbidden Actions**:
- Create files
- Edit files
- Run bash commands
- Modify tests

**Output**: A proposed repository-level patch (diff format)

**Prompt Pattern**:
```
Given these failing tests and error messages:
[test source code]
[error output]

Explore the repository to understand:
1. Where the relevant code lives
2. What the expected behavior should be
3. Why the current implementation fails

Propose a minimal patch to fix the issue.
```

### 2. Debug One Agent

**Purpose**: Deep-dive into ONE failing test

**Allowed Actions**:
- Set breakpoints
- Step through code
- Inspect variables
- View call stack
- Read related files

**Output**: A debugging report explaining:
- What the test expects
- What actually happens
- Where the code diverges
- Suggested fix location

**Prompt Pattern**:
```
Test: [test name]
Source: [test code]
Error: [error message]
Patch tried: [previous patch]

Debug this single test to understand:
1. The execution flow
2. Where behavior diverges from expected
3. What specific change would fix it

Write a detailed report.
```

### 3. Revise Patch Agent

**Purpose**: Fix patches that fail to apply

**Allowed Actions**:
- View files to get correct context
- Search for correct line numbers
- Compare patch expectations vs reality

**Output**: A corrected patch with accurate context lines

**Prompt Pattern**:
```
This patch failed to apply:
[malformed patch]

Error: [patch application error]

Find the correct file context and produce a valid patch.
Do NOT modify the intended code changes, only fix the context.
```

### 4. Generate Tests Agent

**Purpose**: Create ONE reproduction test from the plan

**Rules**:
- ONE test per TDD cycle only
- ONE assert per test
- Test must FAIL before implementation
- Reference the test plan for order
- Validate test actually fails

**Prompt Pattern**:
```
Test Plan: [reference to test plan]
Next Test: [which test to write]

Write this ONE reproduction test that:
1. Captures the expected behavior
2. Currently FAILs (feature not implemented)
3. Is specific and focused

After writing, run test to confirm it fails.
Then proceed to GREEN phase.
```

## TDFlow Algorithm

### For New Features (Start Here)

```
Input: Feature request from user
Output: Working implementation with tests

1. PLAN_TESTS(feature_request) → test_map
   - Acceptance tests (outermost)
   - Integration tests
   - Unit tests (innermost)

2. FOR each test in test_map (outside-in order):
   a. RED: Write ONE failing test
   b. GREEN: Minimal implementation to pass
   c. REFACTOR: Improve code quality
   d. COMMIT each phase

3. DONE when all tests in plan are passing
```

### For Existing Tests (Bug Fixes)

```
Input: Failing tests {f₁, ..., fₙ}
Output: Patch that passes all tests

REPEAT until all tests pass OR max iterations:
  1. RUN tests → collect errors {e₁, ..., eₙ}
  2. EXPLORE_FILES(tests, errors) → proposed_patch
  3. IF patch fails to apply:
       REVISE_PATCH(patch, error) → fixed_patch
  4. APPLY patch to repository
  5. RUN tests again
  6. FOR each failing test fᵢ:
       DEBUG_ONE(fᵢ, patch) → report_i
  7. AGGREGATE reports
  8. Feed reports back to EXPLORE_FILES
```

## Practical Workflow

### Starting a New Feature (London-Style TDD)

```bash
# 1. Plan all tests first
# Use Plan Tests agent to create test map

# 2. Write FIRST test (acceptance level)
pytest path/to/test.py::test_feature_happy_path -xvs
# Should FAIL

# 3. Implement minimal code to pass
# GREEN phase

# 4. Refactor (may iterate multiple times)
# REFACTOR phase - continue until code is clean
# and prepared for the next test

# 5. Commit the cycle (may have multiple REFACTOR commits)
jj new -m "[RED] test_feature_happy_path"
jj new -m "[GREEN] implement feature happy path"
jj new -m "[REFACTOR] extract helper function"
jj new -m "[REFACTOR] improve naming"  # additional pass if needed

# 6. Return to test plan, pick NEXT test
# Repeat 2-5 until all tests pass
```

### Starting with Existing Tests (Bug Fixes)

```bash
# 1. Run tests to identify failures
pytest -x 2>&1 | head -100

# 2. Focus on ONE failing test
pytest path/to/test.py::test_specific -xvs

# 3. Explore relevant code
# (use grep, find, read files)

# 4. Propose minimal fix

# 5. Verify fix
pytest path/to/test.py::test_specific -xvs

# 6. Run full suite to check for regressions
pytest
```

### Starting Without a Test Plan (Quick Fix)

```bash
# 1. Understand the issue/feature

# 2. Write ONE failing test
# - ONE assert per test
# - Specific behavior

# 3. Verify test fails
pytest path/to/test.py -xvs
# Should see FAILED

# 4. Implement to pass (GREEN)

# 5. Refactor

# 6. Repeat with next test
```

## Anti-Patterns (Test Hacking)

### Never Do These:

| Anti-Pattern | Example |
|--------------|---------|
| Modify tests | Change assertions to match buggy behavior |
| Skip tests | `@pytest.mark.skip`, `test.skip()` |
| Weaken assertions | `assertEqual` → `assertTrue(x is not None)` |
| Hardcode values | `return 42  # matches test expectation` |
| Test-only branches | `if testing: return expected_value` |
| Disable checks | `SKIP_VALIDATION=true` in test env |

### Detection Signals:

- Patch touches test files
- Assertions removed or weakened
- Magic constants from tests appear in code
- Environment variable checks in production code

## Context Engineering

### Minimum Context for Explore Files:
- Failing test source code
- Test error messages
- Previous patches and their results
- Debugging reports from failed attempts

### Minimum Context for Debug One:
- Single test source code
- Single error message
- The proposed patch
- Access to debugger

### Why Separate Contexts?
- Reduces long-context burden on each agent
- Focuses attention on specific sub-task
- Allows specialized prompting per role
- Enables parallel debugging of multiple tests

## Iteration Patterns

### Pattern: Incremental Fix
```
Iteration 1: Fix test_basic (3 tests still failing)
Iteration 2: Fix test_edge_case (2 tests still failing)
Iteration 3: Fix test_error_handling (1 test still failing)
Iteration 4: Fix test_integration (all tests pass!)
```

### Pattern: Root Cause Discovery
```
Iteration 1: Surface-level fix (breaks other tests)
Iteration 2: Debug reveals deeper issue
Iteration 3: Fix root cause (all related tests pass)
```

### Pattern: Patch Revision
```
Attempt 1: Patch has wrong context lines
→ Revise patch with correct file state
Attempt 2: Patch applies, tests still fail
→ Debug to understand why
Attempt 3: Corrected logic, all tests pass
```

## Integration with Version Control

### TDD Commits with jj

```bash
# RED: Write failing test
jj new -m "[RED] Add test for feature X"
# Write test, verify it fails
jj describe -m "[RED] Add test for feature X

Test: test_feature_x_basic
Expected: X should return Y
Status: FAILING (not implemented)"

# GREEN: Implement to pass
jj new -m "[GREEN] Implement feature X"
# Minimal implementation
jj describe -m "[GREEN] Implement feature X

Minimal implementation to pass test_feature_x_basic
All tests now pass"

# REFACTOR: Clean up (may have multiple commits)
jj new -m "[REFACTOR] Extract feature X helpers"
# Clean up code
jj describe -m "[REFACTOR] Extract feature X helpers

- Moved validation to separate function
- Added docstrings
- All tests still pass"

# Additional REFACTOR pass if needed
jj new -m "[REFACTOR] Prepare for next test"
jj describe -m "[REFACTOR] Prepare for next test

- Extracted shared constants for upcoming tests
- Simplified interface for extensibility
- All tests still pass"
```

### When to Stop Refactoring

**Stop when:**
- All tests pass
- No obvious code smells remain
- The codebase is ready for the next planned test
- You're searching for improvements rather than seeing them

**Continue if:**
- You can name a specific improvement
- The next test will be easier after this refactoring
- Anticipated future work motivates current cleanup

## Metrics for Success

| Metric | Target |
|--------|--------|
| Test pass rate | 100% |
| Regression rate | 0% |
| Test hacking instances | 0 |
| Patches per issue | < 5 iterations |
| Time to resolution | Decreasing |

## Quick Reference

```
┌─────────────────────────────────────────────────────────┐
│                    TDFlow Quick Start                    │
├─────────────────────────────────────────────────────────┤
│ NEW FEATURE?                                             │
│ 1. PLAN_TESTS first → create test map                   │
│ 2. Write ONE test (acceptance first, outside-in)        │
│ 3. RED → GREEN → REFACTOR                               │
│ 4. Return to plan, pick NEXT test                       │
│ 5. Repeat until all tests pass                          │
├─────────────────────────────────────────────────────────┤
│ EXISTING TESTS FAILING?                                  │
│ 1. Run EXPLORE_FILES                                    │
│ 2. Patch won't apply? → Run REVISE_PATCH                │
│ 3. Tests still fail? → Run DEBUG_ONE per test           │
│ 4. Repeat until all tests pass                          │
├─────────────────────────────────────────────────────────┤
│ Key Rules:                                               │
│ • Plan tests BEFORE writing any                         │
│ • ONE test per TDD cycle                                │
│ • Outside-in: Acceptance → Integration → Unit           │
│ • NEVER modify tests to make them pass                  │
│ • Minimal patches only                                  │
└─────────────────────────────────────────────────────────┘
```

## References

- TDFlow Paper: arxiv.org/abs/2510.23761
- 88.8% success on SWE-Bench Lite with human-written tests
- 94.3% success on SWE-Bench Verified with human-written tests
- Key insight: Decoupling exploration, debugging, and patching improves results
