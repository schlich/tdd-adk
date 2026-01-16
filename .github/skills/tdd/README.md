# TDD Copilot Customization

GitHub Copilot customization for Test-Driven Development based on [TDFlow research](https://arxiv.org/abs/2510.23761).

## Quick Start

### Use TDD Prompts

In Copilot Chat, use these prompts:

| Prompt                | Description                            |
| --------------------- | -------------------------------------- |
| `/tdd-red-phase`      | Write a failing test                   |
| `/tdd-green-phase`    | Implement minimal code to pass         |
| `/tdd-refactor-phase` | Improve code without changing behavior |
| `/tdd-debug-one`      | Deep-dive into a single failing test   |
| `/tdd-explore-files`  | Navigate codebase and propose patches  |
| `/tdd-generate-tests` | Create reproduction tests              |
| `/tdd-full-cycle`     | Complete RED→GREEN→REFACTOR            |

### Key Principles

1. **Tests drive development** - Solve existing tests, don't generate arbitrary code
2. **One test at a time** - Debug and fix focused, atomic changes
3. **No test hacking** - Never modify tests to make them pass
4. **Minimal implementations** - Just enough code to pass tests

## File Structure

```
.github/
├── copilot-instructions.md    # Global TDD instructions
├── chat-participant.json      # Prompt registry
├── prompts/                   # Individual prompts
│   ├── tdd-red-phase.md
│   ├── tdd-green-phase.md
│   ├── tdd-refactor-phase.md
│   ├── tdd-debug-one.md
│   ├── tdd-explore-files.md
│   ├── tdd-generate-tests.md
│   ├── tdd-revise-patch.md
│   └── tdd-full-cycle.md
├── agents/                    # Agent configurations
│   ├── explore-files.md
│   ├── debug-one.md
│   ├── generate-tests.md
│   └── revise-patch.md
└── skills/
    └── tdd/
        ├── SKILLS.md          # Main TDFlow skill
        ├── anti-test-hacking.md
        └── tdflow-prompts.md
```

## TDFlow Architecture

See [tdflow-architecture.d2](../tdflow-architecture.d2) for the visual workflow.

### Four Sub-Agents

| Agent              | Role                           | Tools                  |
| ------------------ | ------------------------------ | ---------------------- |
| **Explore Files**  | Navigate code, propose patches | Read, search (no edit) |
| **Debug One**      | Analyze single failing test    | Debugger, read         |
| **Generate Tests** | Create reproduction tests      | Read, create, run      |
| **Revise Patch**   | Fix malformed patches          | Read, search           |

### Algorithm

```
REPEAT:
  1. Run tests → collect errors
  2. Explore Files → propose patch
  3. If patch fails → Revise Patch
  4. Apply patch, run tests
  5. For each failure → Debug One
  6. Feed debug reports back
UNTIL all tests pass
```

## Key Research Insights

From the TDFlow paper:

- **94.3%** success rate with human-written tests
- **68%** success rate with LLM-generated tests
- **Bottleneck**: Test generation, not test resolution
- **Solution**: Humans write tests, AI implements

## Anti-Patterns (Test Hacking)

Never do these:

- ❌ Modify test assertions
- ❌ Skip or disable tests
- ❌ Weaken assertions
- ❌ Hardcode expected values
- ❌ Add test-only code paths

## References

- [TDFlow Paper](https://arxiv.org/abs/2510.23761) - Han et al., 2025
- [SWE-Bench](https://www.swebench.com/) - Evaluation benchmark
- [jj-tdd Skill](.github/skills/jj-tdd/SKILLS.md) - Integration with Jujutsu
