"""Tests for TDD evaluators (unit tests without API calls)."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from tdd_eval.evaluators import evaluate_full_cycle, evaluate_green_phase, evaluate_red_phase
from tdd_eval.models import (
    GreenPhaseEvaluation,
    RedPhaseEvaluation,
    TDDCycle,
    TestResult,
)


@pytest.fixture
def sample_cycle():
    """Create a sample TDD cycle for testing."""
    return TDDCycle(
        feature_description="Add a sum function",
        red_test_code="def test_sum(): assert sum_numbers(2, 3) == 5",
        red_test_result=TestResult(
            test_name="test_sum",
            passed=False,
            failure_reason="NameError: sum_numbers not defined",
        ),
        green_implementation="def sum_numbers(a, b): return a + b",
        green_test_result=TestResult(test_name="test_sum", passed=True),
    )


@pytest.mark.asyncio
async def test_evaluate_red_phase_structure(sample_cycle):
    """Test that RED phase evaluation returns correct structure."""
    mock_result = RedPhaseEvaluation(
        test_fails_correctly=True,
        test_is_focused=True,
        test_name_descriptive=True,
        failure_message_clear=True,
        score=0.9,
        feedback="Good RED phase",
    )

    mock_agent = MagicMock()
    mock_agent.run = AsyncMock(return_value=MagicMock(data=mock_result))

    with patch("tdd_eval.evaluators.get_red_phase_agent", return_value=mock_agent):
        result = await evaluate_red_phase(sample_cycle)

        assert isinstance(result, RedPhaseEvaluation)
        assert result.score == 0.9
        assert result.test_fails_correctly is True


@pytest.mark.asyncio
async def test_evaluate_green_phase_structure(sample_cycle):
    """Test that GREEN phase evaluation returns correct structure."""
    mock_result = GreenPhaseEvaluation(
        test_passes=True,
        implementation_minimal=True,
        no_test_hacking=True,
        no_regressions=True,
        score=0.95,
        feedback="Good GREEN phase",
    )

    mock_agent = MagicMock()
    mock_agent.run = AsyncMock(return_value=MagicMock(data=mock_result))

    with patch("tdd_eval.evaluators.get_green_phase_agent", return_value=mock_agent):
        result = await evaluate_green_phase(sample_cycle)

        assert isinstance(result, GreenPhaseEvaluation)
        assert result.score == 0.95
        assert result.test_passes is True


@pytest.mark.asyncio
async def test_evaluate_full_cycle_without_refactor(sample_cycle):
    """Test full cycle evaluation without REFACTOR phase."""
    mock_red = RedPhaseEvaluation(
        test_fails_correctly=True,
        test_is_focused=True,
        test_name_descriptive=True,
        failure_message_clear=True,
        score=0.9,
        feedback="Good RED phase",
    )
    mock_green = GreenPhaseEvaluation(
        test_passes=True,
        implementation_minimal=True,
        no_test_hacking=True,
        no_regressions=True,
        score=0.95,
        feedback="Good GREEN phase",
    )

    mock_red_agent = MagicMock()
    mock_red_agent.run = AsyncMock(return_value=MagicMock(data=mock_red))
    mock_green_agent = MagicMock()
    mock_green_agent.run = AsyncMock(return_value=MagicMock(data=mock_green))

    with patch("tdd_eval.evaluators.get_red_phase_agent", return_value=mock_red_agent), patch(
        "tdd_eval.evaluators.get_green_phase_agent", return_value=mock_green_agent
    ):
        result = await evaluate_full_cycle(sample_cycle)

        assert result.red_evaluation.score == 0.9
        assert result.green_evaluation.score == 0.95
        assert result.refactor_evaluation is None
        assert result.overall_score == pytest.approx((0.9 + 0.95) / 2)
        assert result.passed_tdd_discipline is True


@pytest.mark.asyncio
async def test_evaluate_full_cycle_with_refactor(sample_cycle):
    """Test full cycle evaluation with REFACTOR phase."""
    from tdd_eval.models import RefactorPhaseEvaluation

    # Add refactor changes to cycle
    sample_cycle.refactor_changes = ["Add type hints"]
    sample_cycle.refactor_test_results = [
        TestResult(test_name="test_sum", passed=True),
    ]

    mock_red = RedPhaseEvaluation(
        test_fails_correctly=True,
        test_is_focused=True,
        test_name_descriptive=True,
        failure_message_clear=True,
        score=0.9,
        feedback="Good RED phase",
    )
    mock_green = GreenPhaseEvaluation(
        test_passes=True,
        implementation_minimal=True,
        no_test_hacking=True,
        no_regressions=True,
        score=0.95,
        feedback="Good GREEN phase",
    )
    mock_refactor = RefactorPhaseEvaluation(
        tests_still_pass=True,
        behavior_unchanged=True,
        code_quality_improved=True,
        changes_atomic=True,
        appropriate_stopping_point=True,
        score=0.85,
        feedback="Good REFACTOR phase",
    )

    mock_red_agent = MagicMock()
    mock_red_agent.run = AsyncMock(return_value=MagicMock(data=mock_red))
    mock_green_agent = MagicMock()
    mock_green_agent.run = AsyncMock(return_value=MagicMock(data=mock_green))
    mock_refactor_agent = MagicMock()
    mock_refactor_agent.run = AsyncMock(return_value=MagicMock(data=mock_refactor))

    with patch(
        "tdd_eval.evaluators.get_red_phase_agent", return_value=mock_red_agent
    ), patch("tdd_eval.evaluators.get_green_phase_agent", return_value=mock_green_agent), patch(
        "tdd_eval.evaluators.get_refactor_phase_agent", return_value=mock_refactor_agent
    ):
        result = await evaluate_full_cycle(sample_cycle)

        assert result.red_evaluation.score == 0.9
        assert result.green_evaluation.score == 0.95
        assert result.refactor_evaluation.score == 0.85
        assert result.overall_score == pytest.approx((0.9 + 0.95 + 0.85) / 3)
        assert result.passed_tdd_discipline is True
