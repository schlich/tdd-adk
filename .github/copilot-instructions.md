# GitHub Copilot Custom Instructions for TDD

## Core Philosophy: Test-Driven Flow (TDFlow)

This project follows an agentic TDD workflow inspired by TDFlow research. The key principle is that **tests drive development** - LLMs solve human-written tests rather than generating arbitrary implementations.

## TDD Workflow Rules

### 1. Test Planning First (For New Features)

When given a request for a new app or feature:

1. **ALWAYS plan tests first** before writing any code or tests
2. Create a comprehensive test map listing ALL necessary tests
3. Use **London-style (top-down/outside-in) TDD**:
   - Start with acceptance tests (user-facing behavior)
   - Work inward to integration tests
   - Discover unit tests as you implement
4. **Generate only ONE test per TDD cycle**

#### London-Style TDD Approach

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

**Why London-style?**
- Tests drive architecture discovery
- Mock dependencies not yet implemented
- Validates behavior before implementation details
- Natural fit for iterative development

### 2. Test Resolution Focus

- Always prioritize solving existing tests over writing new code
- When tests exist, analyze them to understand the expected behavior
- Never modify test code to make tests pass (anti-pattern: "test hacking")

### 3. The Five TDFlow Sub-Agent Roles

When working on code, mentally adopt these focused roles:

#### Plan Tests Agent (NEW - Use First for Features)

- Map out ALL tests needed for a feature before writing any
- Organize tests in layers: acceptance → integration → unit
- Identify dependencies to mock
- Prioritize test execution order
- Output: A test map, NOT actual test code

#### Explore Files Agent

- Navigate the codebase to understand context
- Propose repository-level patches based on failing tests
- Access: file viewing, keyword search, folder hierarchy only
- NO file creation or editing during exploration

#### Debug One Agent

- Focus on ONE failing test at a time
- Use debugging to understand why the test fails
- Generate detailed reports on failure causes
- Identify specific code locations that need changes

#### Revise Patch Agent

- Fix malformed or incorrect patches
- Ensure patches apply cleanly to the codebase
- Verify context lines match actual file content

#### Generate Tests Agent (when no tests exist)

- Write reproduction tests that capture the issue
- Each test should have ONE assert statement
- Tests should FAIL before implementation (RED phase)
- Validate tests actually fail using test runner

### 4. Structured Output Format

When proposing changes, always structure as:

```
## Analysis
- Failing test(s): [list]
- Root cause: [explanation]
- Files affected: [paths]

## Proposed Patch
[minimal change to pass tests]

## Verification
- Expected: All tests pass
- Side effects: None / [list any]
```

### 5. Anti-Patterns to Avoid (Test Hacking)

NEVER do these:

- Modify test source code to avoid assertions
- Skip or disable tests
- Weaken assertions
- Hardcode outputs to match test expectations
- Add test-only logic paths
- Modify test fixtures/data to avoid failures

### 6. TDD Phase Discipline

**RED Phase**: Write ONE failing test

- Test must fail for the right reason
- Test captures expected behavior

**GREEN Phase**: Minimal implementation

- Write just enough code to pass
- Resist over-engineering
- Run test to verify it passes

**REFACTOR Phase**: Improve without changing behavior (may iterate multiple times)

- All tests must still pass
- Clean up code smells
- Extract abstractions
- **Multiple refactoring passes are encouraged** within a single cycle

#### When to Refactor (Motivating Factors)

- **Code smells**: Duplication, long methods, unclear naming, magic numbers
- **Anticipated future work**: If upcoming tests/features will need similar patterns, extract them now
- **Readability**: If the GREEN implementation is hard to understand
- **Design improvement**: Better abstractions, clearer interfaces, improved cohesion
- **Technical debt prevention**: Address shortcuts taken during GREEN phase

#### When Refactoring is Complete

Stop refactoring when:
- All tests still pass
- Code is readable and intention-revealing
- Duplication is minimized (DRY)
- Functions/methods have single responsibilities
- No obvious improvements remain for the **current scope**
- The codebase is prepared for the **next planned test** in your test map

**Rule of thumb**: If you can articulate a specific improvement, do it. If you're searching for something to change, you're done.

### 7. Context Management

To reduce cognitive load:

- Keep each sub-task focused and narrow
- Don't try to fix everything at once
- Debug one test at a time
- Make small, atomic commits

### 8. Iteration Strategy

When a patch doesn't work:

1. Run tests to collect error messages
2. Debug each failing test individually
3. Aggregate debugging reports
4. Propose revised patch with new context
5. Repeat until all tests pass

## Language-Specific Testing

### Python

```bash
pytest -xvs path/to/test.py::TestClass::test_method
```

### JavaScript/TypeScript

```bash
npm test -- --testPathPattern="test-name"
```

### Rust

```bash
cargo test test_name -- --nocapture
```

### Go

```bash
go test -v -run TestName ./...
```

## Integration with Jujutsu (jj)

This project uses jj for version control. TDD phases map to jj revisions:

- `[RED]` commits: Failing tests
- `[GREEN]` commits: Minimal implementations
- `[REFACTOR]` commits: Code improvements

See `.github/skills/jj-tdd/SKILLS.md` for detailed jj+TDD workflow.

## Code Quality with Prek

This project uses [prek](https://prek.j178.dev/) (Rust-based pre-commit) for code quality checks.

### Quick Commands

```bash
prek run                    # Check modified files
prek run --all-files        # Check entire codebase
prek run --hook-stage manual # Run manual hooks (tests, etc.)
```

### Integration with jj

Since jj auto-snapshots (no staging area), run prek manually before pushing:

```bash
prek run --all-files && jj git push
```

### TDD Integration

- **Before GREEN phase**: `prek run` to catch formatting issues
- **After REFACTOR phase**: `prek run --all-files` for full validation
- **Before push**: Always run full checks

See `.github/skills/prek/SKILLS.md` for detailed prek configuration and usage.

## References

- TDFlow Paper: https://arxiv.org/abs/2510.23761
- Key insight: 94.3% success rate when solving human-written tests
- The bottleneck is test generation, not test resolution
