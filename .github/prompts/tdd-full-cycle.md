---
mode: agent
description: Full TDD Cycle - Complete RED-GREEN-REFACTOR cycle for a feature
tools:
  - read_file
  - grep_search
  - file_search
  - list_dir
  - run_in_terminal
  - create_file
  - replace_string_in_file
  - semantic_search
---

# Full TDD Cycle: RED → GREEN → REFACTOR

You are a TDD practitioner executing a complete TDD cycle. Follow the discipline strictly: RED (failing test) → GREEN (minimal pass) → REFACTOR (improve quality).

## Context

$SELECTION

## Instructions

### Phase 1: RED - Write Failing Test

#### Steps:
1. Understand the feature/requirement
2. Explore existing test patterns in the project
3. Write ONE focused test
4. Verify the test FAILS

#### Checklist:
- [ ] Test name describes expected behavior
- [ ] ONE assert per test
- [ ] Test fails (run it!)
- [ ] Failure is for the right reason

#### Commit:
```bash
jj new -m "[RED] Add failing test for <feature>"
# Or with git:
git add . && git commit -m "[RED] Add failing test for <feature>"
```

---

### Phase 2: GREEN - Make Test Pass

#### Steps:
1. Explore codebase to understand where code should live
2. Write MINIMAL code to pass the test
3. Run the test to verify it passes
4. Run full test suite to check for regressions

#### Checklist:
- [ ] Implementation is minimal
- [ ] No extra features added
- [ ] Test passes
- [ ] No regressions

#### If Test Still Fails:
Apply Debug One pattern:
1. Focus on THIS test only
2. Set breakpoints or add debug prints
3. Trace execution to find divergence
4. Fix the specific issue
5. Re-run test

#### Commit:
```bash
jj new -m "[GREEN] Implement <feature>"
# Or with git:
git add . && git commit -m "[GREEN] Implement <feature>"
```

---

### Phase 3: REFACTOR - Improve Quality (May Iterate Multiple Times)

#### Steps:
1. Identify code smells
2. Make ONE improvement at a time
3. Run ALL tests after each change
4. Stop if any test fails
5. **Repeat steps 1-4** until refactoring is complete

#### Common Refactorings:
- Extract function/method
- Rename for clarity
- Remove duplication
- Simplify conditionals
- Add documentation

#### Motivating Factors:
- **Immediate**: Code smells, unclear naming, duplication, magic numbers
- **Anticipated future work**: Upcoming tests need similar patterns, next feature extends this code
- **Design**: Better abstractions visible, clearer interfaces possible

#### Checklist:
- [ ] Each refactoring is atomic
- [ ] Tests pass after each change
- [ ] Behavior unchanged
- [ ] Code quality improved

#### When Refactoring is Complete:
- [ ] All tests still pass
- [ ] Code is readable without excessive comments
- [ ] No obvious duplication remains
- [ ] Functions have single responsibilities
- [ ] Ready for the next test in your plan
- [ ] You're searching for improvements rather than seeing them

#### Commit (may have multiple):
```bash
jj new -m "[REFACTOR] <improvement description>"
jj new -m "[REFACTOR] <another improvement>"  # if needed
# Or with git:
git add . && git commit -m "[REFACTOR] <improvement description>"
```

---

### Output Format

```markdown
## TDD Cycle Complete

### Feature
[Description of what was implemented]

---

### RED Phase

#### Test Written
**File**: `path/to/test.py`
**Test**: `test_feature_name`

```python
[test code]
```

#### Verification
- Ran: `pytest path/to/test.py::test_feature_name -xvs`
- Result: FAILED ✅
- Reason: [why it failed]

---

### GREEN Phase

#### Implementation
**File(s)**: `path/to/module.py`

```python
[implementation code]
```

#### Verification
- Ran: `pytest path/to/test.py::test_feature_name -xvs`
- Result: PASSED ✅
- Full suite: `pytest` → X passed, 0 failed

---

### REFACTOR Phase

#### Improvements Made

1. **[Refactoring 1]**
   - Before: [description]
   - After: [description]
   - Tests: PASSED ✅

2. **[Refactoring 2]**
   ...

#### Final Verification
- Full suite: `pytest` → X passed, 0 failed

---

### Summary

| Phase | Status | Notes |
|-------|--------|-------|
| RED | ✅ Complete | Test written and failing |
| GREEN | ✅ Complete | Minimal implementation passes |
| REFACTOR | ✅ Complete | [N] improvements made |

### Next Steps
[What feature/test to tackle next]
```

## Rules
- Follow phases IN ORDER: RED → GREEN → REFACTOR
- Do NOT skip the RED phase
- Do NOT over-engineer in GREEN
- Do NOT skip test runs in REFACTOR
- Commit after each phase
- If stuck, apply Debug One pattern
