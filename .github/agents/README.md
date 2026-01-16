# TDD Agents Configuration

This directory contains agent configurations for TDFlow-style Test-Driven Development.

## Workflow Order

For new features/apps, use agents in this order:

1. **Plan Tests** → Create test map (ALWAYS START HERE for new features)
2. **Generate Tests** → Write ONE test from the plan
3. **Explore Files** → Understand codebase for implementation
4. **Debug One** → If test fails unexpectedly
5. **Revise Patch** → If patch doesn't apply cleanly

## Available Agents

### 0. Plan Tests Agent (`plan-tests.md`) ⭐ START HERE
- **Role**: Map out ALL tests before writing any (London-style TDD)
- **Tools**: Read files, search (read-only)
- **Output**: Comprehensive test plan with layers (acceptance → integration → unit)
- **When**: FIRST step for any new feature or app request

### 1. Explore Files Agent (`explore-files.md`)
- **Role**: Navigate codebase, analyze tests, propose patches
- **Tools**: Read files, search, list directories
- **Cannot**: Create/edit files

### 2. Debug One Agent (`debug-one.md`)
- **Role**: Deep-dive into a single failing test
- **Tools**: Debugger, file reading, search
- **Output**: Detailed debugging report

### 3. Revise Patch Agent (`revise-patch.md`)
- **Role**: Fix patches that fail to apply
- **Tools**: Read files, search (context only)
- **Output**: Corrected patch

### 4. Generate Tests Agent (`generate-tests.md`)
- **Role**: Create ONE reproduction test from the test plan
- **Tools**: Read files, create files, run tests
- **Output**: Single failing test
- **Rule**: ONE test per TDD cycle only

## Usage

Reference these agents in prompts or invoke directly:

```
@workspace /tdd-plan Plan tests for the user authentication feature
@workspace /tdd-explore Analyze the failing tests and propose a fix
@workspace /tdd-debug Debug test_authentication_failure
@workspace /tdd-generate Write the next test from the plan
```

## London-Style TDD (Top-Down)

This workflow favors **London-style (outside-in) TDD**:

```
┌─────────────────────────────────────┐
│   Acceptance Tests (Start Here)     │  ← User-facing behavior
│  ┌───────────────────────────────┐  │
│  │    Integration Tests          │  │  ← Component contracts
│  │  ┌─────────────────────────┐  │  │
│  │  │    Unit Tests           │  │  │  ← Implementation details
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

**Key Principles:**
- Plan all tests first, write one at a time
- Start from user behavior, work inward
- Mock dependencies not yet implemented
- Let tests drive architecture discovery

## Agent Philosophy

From TDFlow research:
- **Forced decoupling** reduces cognitive load
- **Specialized tools** per agent improve results
- **Minimum context** prevents hallucination
- **Iterative refinement** with debug feedback
