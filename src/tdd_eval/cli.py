"""CLI runner for TDD cycle evaluation."""

import asyncio
import json
from pathlib import Path

from .evaluators import evaluate_full_cycle
from .models import EvaluationResult, TDDCycle


async def run_evaluation(cycle_data: dict) -> EvaluationResult:
    """Run evaluation on a TDD cycle.

    Args:
        cycle_data: Dictionary containing TDD cycle data

    Returns:
        Evaluation result
    """
    cycle = TDDCycle(**cycle_data)
    evaluation = await evaluate_full_cycle(cycle)
    return EvaluationResult(cycle=cycle, evaluation=evaluation)


def print_evaluation(result: EvaluationResult) -> None:
    """Print evaluation results in a human-readable format.

    Args:
        result: Evaluation result to print
    """
    print("\n" + "=" * 80)
    print("TDD CYCLE EVALUATION REPORT")
    print("=" * 80)
    print(f"\nFeature: {result.cycle.feature_description}")
    print(f"\nOverall Score: {result.evaluation.overall_score:.2f}")
    print(f"TDD Discipline: {'✅ PASSED' if result.evaluation.passed_tdd_discipline else '❌ NEEDS IMPROVEMENT'}")
    print(f"\n{result.evaluation.summary}")

    # RED phase
    print("\n" + "-" * 80)
    print("RED PHASE EVALUATION")
    print("-" * 80)
    red = result.evaluation.red_evaluation
    print(f"Score: {red.score:.2f}")
    print(f"✓ Test fails correctly: {red.test_fails_correctly}")
    print(f"✓ Test is focused: {red.test_is_focused}")
    print(f"✓ Test name descriptive: {red.test_name_descriptive}")
    print(f"✓ Failure message clear: {red.failure_message_clear}")
    print(f"\nFeedback: {red.feedback}")

    # GREEN phase
    print("\n" + "-" * 80)
    print("GREEN PHASE EVALUATION")
    print("-" * 80)
    green = result.evaluation.green_evaluation
    print(f"Score: {green.score:.2f}")
    print(f"✓ Test passes: {green.test_passes}")
    print(f"✓ Implementation minimal: {green.implementation_minimal}")
    print(f"✓ No test hacking: {green.no_test_hacking}")
    print(f"✓ No regressions: {green.no_regressions}")
    print(f"\nFeedback: {green.feedback}")

    # REFACTOR phase (if present)
    if result.evaluation.refactor_evaluation:
        print("\n" + "-" * 80)
        print("REFACTOR PHASE EVALUATION")
        print("-" * 80)
        refactor = result.evaluation.refactor_evaluation
        print(f"Score: {refactor.score:.2f}")
        print(f"✓ Tests still pass: {refactor.tests_still_pass}")
        print(f"✓ Behavior unchanged: {refactor.behavior_unchanged}")
        print(f"✓ Code quality improved: {refactor.code_quality_improved}")
        print(f"✓ Changes atomic: {refactor.changes_atomic}")
        print(f"✓ Appropriate stopping point: {refactor.appropriate_stopping_point}")
        print(f"\nFeedback: {refactor.feedback}")

    print("\n" + "=" * 80)


async def main():
    """Main entry point for the CLI."""
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate TDD cycles")
    parser.add_argument(
        "input_file",
        type=Path,
        help="JSON file containing TDD cycle data",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output file for evaluation results (JSON)",
    )

    args = parser.parse_args()

    # Load cycle data
    with open(args.input_file) as f:
        cycle_data = json.load(f)

    # Run evaluation
    print(f"Evaluating TDD cycle from {args.input_file}...")
    result = await run_evaluation(cycle_data)

    # Print results
    print_evaluation(result)

    # Save to file if requested
    if args.output:
        with open(args.output, "w") as f:
            json.dump(result.model_dump(), f, indent=2)
        print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    asyncio.run(main())
