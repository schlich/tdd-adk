"""TDD cycle evaluators using pydantic-ai."""


from pydantic_ai import Agent

from tdd_eval.models import (
    FullCycleEvaluation,
    GreenPhaseEvaluation,
    RedPhaseEvaluation,
    RefactorPhaseEvaluation,
    TDDCycle,
)

# Lazily initialized agents
_red_phase_agent: Agent | None = None
_green_phase_agent: Agent | None = None
_refactor_phase_agent: Agent | None = None


def get_red_phase_agent() -> Agent:
    """Get or create RED phase evaluator agent."""
    global _red_phase_agent
    if _red_phase_agent is None:
        _red_phase_agent = Agent(
            "openai:gpt-4o-mini",
            result_type=RedPhaseEvaluation,
            system_prompt="""You are an expert TDD practitioner evaluating the RED phase of a TDD cycle.

Assess the following criteria:
1. Test fails correctly (not due to syntax errors or import issues)
2. Test is focused (ONE clear assertion)
3. Test name describes expected behavior
4. Failure message is clear and helpful

Provide honest, constructive feedback. The RED phase should establish a clear failing test.""",
        )
    return _red_phase_agent


def get_green_phase_agent() -> Agent:
    """Get or create GREEN phase evaluator agent."""
    global _green_phase_agent
    if _green_phase_agent is None:
        _green_phase_agent = Agent(
            "openai:gpt-4o-mini",
            result_type=GreenPhaseEvaluation,
            system_prompt="""You are an expert TDD practitioner evaluating the GREEN phase of a TDD cycle.

Assess the following criteria:
1. Test now passes
2. Implementation is minimal (no over-engineering, just enough to pass)
3. No test hacking (test code was NOT modified to make it pass)
4. No regressions (other tests still pass)

Provide honest, constructive feedback. The GREEN phase should be the simplest solution.""",
        )
    return _green_phase_agent


def get_refactor_phase_agent() -> Agent:
    """Get or create REFACTOR phase evaluator agent."""
    global _refactor_phase_agent
    if _refactor_phase_agent is None:
        _refactor_phase_agent = Agent(
            "openai:gpt-4o-mini",
            result_type=RefactorPhaseEvaluation,
            system_prompt="""You are an expert TDD practitioner evaluating the REFACTOR phase of a TDD cycle.

Assess the following criteria:
1. All tests still pass after refactoring
2. Behavior is unchanged
3. Code quality improved (readability, maintainability, removal of duplication)
4. Changes were atomic (one improvement at a time)
5. Refactoring stopped at appropriate point (no premature optimization)

Provide honest, constructive feedback. The REFACTOR phase should improve quality without changing behavior.""",
        )
    return _refactor_phase_agent


async def evaluate_red_phase(cycle: TDDCycle) -> RedPhaseEvaluation:
    """Evaluate the RED phase of a TDD cycle.

    Args:
        cycle: The TDD cycle to evaluate

    Returns:
        Evaluation of the RED phase
    """
    prompt = f"""Evaluate this RED phase:

Feature: {cycle.feature_description}

Test Code:
```
{cycle.red_test_code}
```

Test Result:
- Test Name: {cycle.red_test_result.test_name}
- Passed: {cycle.red_test_result.passed}
- Failure Reason: {cycle.red_test_result.failure_reason or 'N/A'}

Provide your evaluation."""

    agent = get_red_phase_agent()
    result = await agent.run(prompt)
    return result.data


async def evaluate_green_phase(cycle: TDDCycle) -> GreenPhaseEvaluation:
    """Evaluate the GREEN phase of a TDD cycle.

    Args:
        cycle: The TDD cycle to evaluate

    Returns:
        Evaluation of the GREEN phase
    """
    prompt = f"""Evaluate this GREEN phase:

Feature: {cycle.feature_description}

Original RED Test Code:
```
{cycle.red_test_code}
```

GREEN Implementation:
```
{cycle.green_implementation}
```

Test Result After Implementation:
- Test Name: {cycle.green_test_result.test_name}
- Passed: {cycle.green_test_result.passed}
- Failure Reason: {cycle.green_test_result.failure_reason or 'N/A'}

Provide your evaluation."""

    agent = get_green_phase_agent()
    result = await agent.run(prompt)
    return result.data


async def evaluate_refactor_phase(cycle: TDDCycle) -> RefactorPhaseEvaluation:
    """Evaluate the REFACTOR phase of a TDD cycle.

    Args:
        cycle: The TDD cycle to evaluate

    Returns:
        Evaluation of the REFACTOR phase
    """
    refactor_summary = "\n".join(
        f"{i+1}. {change}" for i, change in enumerate(cycle.refactor_changes)
    )

    test_results_summary = "\n".join(
        f"After change {i+1}: {result.test_name} - {'PASSED' if result.passed else 'FAILED'}"
        for i, result in enumerate(cycle.refactor_test_results)
    )

    prompt = f"""Evaluate this REFACTOR phase:

Feature: {cycle.feature_description}

Refactoring Changes Made:
{refactor_summary}

Test Results After Each Change:
{test_results_summary}

Original GREEN Implementation:
```
{cycle.green_implementation}
```

Provide your evaluation."""

    agent = get_refactor_phase_agent()
    result = await agent.run(prompt)
    return result.data


async def evaluate_full_cycle(cycle: TDDCycle) -> FullCycleEvaluation:
    """Evaluate a complete TDD cycle.

    Args:
        cycle: The TDD cycle to evaluate

    Returns:
        Full cycle evaluation
    """
    # Evaluate each phase
    red_eval = await evaluate_red_phase(cycle)
    green_eval = await evaluate_green_phase(cycle)

    # REFACTOR is optional
    refactor_eval = None
    if cycle.refactor_changes:
        refactor_eval = await evaluate_refactor_phase(cycle)

    # Calculate overall score
    scores = [red_eval.score, green_eval.score]
    if refactor_eval:
        scores.append(refactor_eval.score)
    overall_score = sum(scores) / len(scores)

    # Check if TDD discipline was followed
    passed_tdd_discipline = (
        red_eval.test_fails_correctly
        and green_eval.test_passes
        and green_eval.no_test_hacking
        and (refactor_eval is None or refactor_eval.tests_still_pass)
    )

    # Generate summary
    summary_parts = [
        f"RED phase: {'✅' if red_eval.score >= 0.8 else '⚠️'} (score: {red_eval.score:.2f})",
        f"GREEN phase: {'✅' if green_eval.score >= 0.8 else '⚠️'} (score: {green_eval.score:.2f})",
    ]
    if refactor_eval:
        summary_parts.append(
            f"REFACTOR phase: {'✅' if refactor_eval.score >= 0.8 else '⚠️'} "
            f"(score: {refactor_eval.score:.2f})"
        )
    summary_parts.append(f"Overall: {'PASSED' if passed_tdd_discipline else 'NEEDS IMPROVEMENT'}")
    summary = " | ".join(summary_parts)

    return FullCycleEvaluation(
        red_evaluation=red_eval,
        green_evaluation=green_eval,
        refactor_evaluation=refactor_eval,
        overall_score=overall_score,
        passed_tdd_discipline=passed_tdd_discipline,
        summary=summary,
    )
