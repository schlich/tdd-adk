#!/usr/bin/env python3
"""Example of programmatic usage of the TDD evaluation framework.

This demonstrates how to use the evaluation framework in your own code
without using the CLI.
"""

import asyncio
import os

from tdd_eval import TDDCycle, TestResult
from tdd_eval.evaluators import evaluate_full_cycle, evaluate_red_phase


async def example_full_cycle_evaluation():
    """Demonstrate evaluating a complete TDD cycle."""
    print("=" * 80)
    print("EXAMPLE: Full TDD Cycle Evaluation")
    print("=" * 80)

    # Define a TDD cycle
    cycle = TDDCycle(
        feature_description="Add a function to multiply two numbers",
        red_test_code="""def test_multiply_two_numbers():
    \"\"\"Test that multiply function works correctly.\"\"\"
    result = multiply(3, 4)
    assert result == 12""",
        red_test_result=TestResult(
            test_name="test_multiply_two_numbers",
            passed=False,
            failure_reason="NameError: name 'multiply' is not defined",
        ),
        green_implementation="""def multiply(a, b):
    \"\"\"Multiply two numbers.\"\"\"
    return a * b""",
        green_test_result=TestResult(test_name="test_multiply_two_numbers", passed=True),
        refactor_changes=["Add type hints", "Add docstring example"],
        refactor_test_results=[
            TestResult(test_name="test_multiply_two_numbers", passed=True),
            TestResult(test_name="test_multiply_two_numbers", passed=True),
        ],
    )

    # Check if OpenAI API key is available
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not set. Skipping actual evaluation.")
        print("Set OPENAI_API_KEY environment variable to run actual evaluation.\n")
        return

    # Evaluate the cycle
    print("\nEvaluating TDD cycle...")
    evaluation = await evaluate_full_cycle(cycle)

    print(f"\n✅ Overall score: {evaluation.overall_score:.2f}")
    print(f"✅ Passed TDD discipline: {evaluation.passed_tdd_discipline}")
    print(f"\nSummary: {evaluation.summary}")

    print(f"\nRED Phase Feedback: {evaluation.red_evaluation.feedback}")
    print(f"GREEN Phase Feedback: {evaluation.green_evaluation.feedback}")
    if evaluation.refactor_evaluation:
        print(f"REFACTOR Phase Feedback: {evaluation.refactor_evaluation.feedback}")


async def example_red_phase_only():
    """Demonstrate evaluating just the RED phase."""
    print("\n" + "=" * 80)
    print("EXAMPLE: RED Phase Only Evaluation")
    print("=" * 80)

    cycle = TDDCycle(
        feature_description="Add a function to divide two numbers",
        red_test_code="""def test_divide_two_numbers():
    \"\"\"Test that divide function works correctly.\"\"\"
    result = divide(10, 2)
    assert result == 5""",
        red_test_result=TestResult(
            test_name="test_divide_two_numbers",
            passed=False,
            failure_reason="NameError: name 'divide' is not defined",
        ),
        green_implementation="# Not yet implemented",
        green_test_result=TestResult(
            test_name="test_divide_two_numbers",
            passed=False,
            failure_reason="NameError: name 'divide' is not defined",
        ),
    )

    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not set. Skipping actual evaluation.")
        print("Set OPENAI_API_KEY environment variable to run actual evaluation.\n")
        return

    print("\nEvaluating RED phase only...")
    red_eval = await evaluate_red_phase(cycle)

    print(f"\n✅ RED Phase Score: {red_eval.score:.2f}")
    print(f"   - Test fails correctly: {red_eval.test_fails_correctly}")
    print(f"   - Test is focused: {red_eval.test_is_focused}")
    print(f"   - Test name descriptive: {red_eval.test_name_descriptive}")
    print(f"   - Failure message clear: {red_eval.failure_message_clear}")
    print(f"\nFeedback: {red_eval.feedback}")


async def main():
    """Run all examples."""
    await example_full_cycle_evaluation()
    await example_red_phase_only()

    print("\n" + "=" * 80)
    print("Examples complete!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
