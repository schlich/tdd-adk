# TDD Evaluation Framework

A Python-based evaluation framework for Test-Driven Development (TDD) cycles using [pydantic-ai](https://ai.pydantic.dev/).

## Overview

This framework evaluates TDD cycles across the three classic phases:
- **RED**: Writing a failing test
- **GREEN**: Implementing minimal code to pass the test
- **REFACTOR**: Improving code quality without changing behavior

The evaluation uses pydantic-ai agents to assess whether TDD discipline was followed and provide constructive feedback.

## Installation

```bash
# Install dependencies
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

## Usage

### CLI Evaluation

Evaluate a TDD cycle from a JSON file:

```bash
python -m tdd_eval.cli examples/simple_tdd_cycle.json
```

Save evaluation results to a file:

```bash
python -m tdd_eval.cli examples/simple_tdd_cycle.json -o results.json
```

### Programmatic Usage

```python
import asyncio
from tdd_eval import TDDCycle, TestResult
from tdd_eval.evaluators import evaluate_full_cycle

async def main():
    # Define a TDD cycle
    cycle = TDDCycle(
        feature_description="Add a sum function",
        red_test_code="def test_sum(): assert sum_numbers(2, 3) == 5",
        red_test_result=TestResult(
            test_name="test_sum",
            passed=False,
            failure_reason="NameError: sum_numbers not defined"
        ),
        green_implementation="def sum_numbers(a, b): return a + b",
        green_test_result=TestResult(
            test_name="test_sum",
            passed=True
        )
    )
    
    # Evaluate the cycle
    evaluation = await evaluate_full_cycle(cycle)
    print(f"Overall score: {evaluation.overall_score}")
    print(f"Passed TDD discipline: {evaluation.passed_tdd_discipline}")

asyncio.run(main())
```

## Input Format

The evaluation expects a JSON file with the following structure:

```json
{
  "feature_description": "Description of the feature being developed",
  "red_test_code": "Test code written in RED phase",
  "red_test_result": {
    "test_name": "test_name",
    "passed": false,
    "failure_reason": "Why the test failed",
    "execution_time_ms": 2.5
  },
  "green_implementation": "Implementation code in GREEN phase",
  "green_test_result": {
    "test_name": "test_name",
    "passed": true,
    "execution_time_ms": 1.2
  },
  "refactor_changes": [
    "Description of refactoring change 1",
    "Description of refactoring change 2"
  ],
  "refactor_test_results": [
    {
      "test_name": "test_name",
      "passed": true,
      "execution_time_ms": 1.3
    }
  ]
}
```

See `examples/simple_tdd_cycle.json` for a complete example.

## Evaluation Criteria

### RED Phase
- ✅ Test fails for the right reason (not syntax errors)
- ✅ Test has ONE clear assertion
- ✅ Test name describes expected behavior
- ✅ Failure message is clear and helpful

### GREEN Phase
- ✅ Test now passes
- ✅ Implementation is minimal (no over-engineering)
- ✅ No test hacking (test wasn't modified)
- ✅ No regressions (other tests still pass)

### REFACTOR Phase (Optional)
- ✅ All tests still pass
- ✅ Behavior is unchanged
- ✅ Code quality improved
- ✅ Changes were atomic
- ✅ Refactoring stopped at appropriate point

## Development

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check .
```

## Architecture

The framework uses pydantic-ai to create specialized evaluation agents:

- `red_phase_agent`: Evaluates RED phase quality
- `green_phase_agent`: Evaluates GREEN phase quality
- `refactor_phase_agent`: Evaluates REFACTOR phase quality

Each agent uses structured output (Pydantic models) to ensure consistent evaluation format.

## Related

This evaluation framework is part of the TDD-ADK (Test-Driven Development Agent Development Kit) project, which implements TDFlow methodology:

- [TDFlow Research Paper](https://arxiv.org/abs/2510.23761)
- [TDD Copilot Instructions](.github/copilot-instructions.md)
- [TDD Agents](.github/agents/)

## License

[Add your license here]
