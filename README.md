# TDD Evaluation Framework

A Python-based evaluation framework for Test-Driven Development (TDD) cycles using [pydantic-ai](https://ai.pydantic.dev/).

## Overview

This framework evaluates TDD cycles across the three classic phases:
- **RED**: Writing a failing test
- **GREEN**: Implementing minimal code to pass the test
- **REFACTOR**: Improving code quality without changing behavior

The evaluation uses pydantic-ai agents to assess whether TDD discipline was followed and provide constructive feedback.

## Features

- 📊 **Structured Evaluation**: Uses Pydantic models for type-safe, validated evaluation results
- 🤖 **AI-Powered Analysis**: Leverages pydantic-ai with OpenAI GPT-4o-mini for intelligent TDD assessment
- 🎯 **Phase-Specific Agents**: Specialized evaluators for RED, GREEN, and REFACTOR phases
- 📝 **Detailed Feedback**: Provides actionable insights on TDD discipline adherence
- 🔍 **Granular or Full-Cycle**: Evaluate individual phases or complete TDD cycles
- 🧪 **Well-Tested**: Comprehensive test suite with 100% passing tests

## Installation

```bash
# Clone the repository
git clone https://github.com/schlich/tdd-adk.git
cd tdd-adk

# Install dependencies
pip install -e .

# Install development dependencies (for testing)
pip install -e ".[dev]"
```

## Configuration

Set your OpenAI API key:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Usage

### CLI Evaluation

Evaluate a complete TDD cycle from a JSON file:

```bash
python -m tdd_eval.cli examples/simple_tdd_cycle.json
```

Evaluate and save results:

```bash
python -m tdd_eval.cli examples/validation_tdd_cycle.json -o results.json
```

### Programmatic Usage

See `examples/programmatic_usage.py` for complete examples. Here's a quick start:

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

### Evaluating Individual Phases

You can also evaluate just a single phase:

```python
from tdd_eval.evaluators import evaluate_red_phase, evaluate_green_phase

# Evaluate only the RED phase
red_evaluation = await evaluate_red_phase(cycle)
print(f"RED phase score: {red_evaluation.score}")

# Evaluate only the GREEN phase
green_evaluation = await evaluate_green_phase(cycle)
print(f"GREEN phase score: {green_evaluation.score}")
```

## Examples

The `examples/` directory contains several sample TDD cycles:

1. **simple_tdd_cycle.json** - Basic addition function with RED→GREEN→REFACTOR
2. **validation_tdd_cycle.json** - Input validation with comprehensive refactoring
3. **red_phase_only.json** - Example of evaluating just the RED phase
4. **programmatic_usage.py** - Python script demonstrating API usage

Run any example:

```bash
# CLI evaluation
python -m tdd_eval.cli examples/simple_tdd_cycle.json

# Programmatic example
python examples/programmatic_usage.py
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

# Fix linting issues automatically
ruff check --fix .
```

## Architecture

The framework uses pydantic-ai to create specialized evaluation agents:

- `get_red_phase_agent()`: Returns agent for evaluating RED phase quality
- `get_green_phase_agent()`: Returns agent for evaluating GREEN phase quality  
- `get_refactor_phase_agent()`: Returns agent for evaluating REFACTOR phase quality

Each agent:
- Uses OpenAI GPT-4o-mini for intelligent analysis
- Returns structured output via Pydantic models
- Has a specialized system prompt tailored to its phase
- Is lazily initialized to avoid requiring API keys at import time

### Key Components

- **Models** (`src/tdd_eval/models.py`): Pydantic models for TDD cycles and evaluations
- **Evaluators** (`src/tdd_eval/evaluators.py`): AI-powered evaluation logic
- **CLI** (`src/tdd_eval/cli.py`): Command-line interface for evaluations

## Use Cases

This evaluation framework can be used for:

1. **Training**: Help developers learn TDD discipline by evaluating their practice cycles
2. **Code Review**: Automated assessment of whether PRs follow TDD methodology
3. **Research**: Collect data on TDD effectiveness and common anti-patterns
4. **CI/CD**: Integrate TDD quality checks into development workflows
5. **LLM Evaluation**: Assess how well AI coding agents follow TDD practices

## Related

This evaluation framework is part of the TDD-ADK (Test-Driven Development Agent Development Kit) project, which implements TDFlow methodology:

- [TDFlow Research Paper](https://arxiv.org/abs/2510.23761)
- [TDD Copilot Instructions](.github/copilot-instructions.md)
- [TDD Agents](.github/agents/)

## License

[Add your license here]
