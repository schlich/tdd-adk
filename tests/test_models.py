"""Tests for TDD evaluation models."""

import pytest

from tdd_eval.models import (
    FullCycleEvaluation,
    GreenPhaseEvaluation,
    RedPhaseEvaluation,
    RefactorPhaseEvaluation,
    TDDCycle,
    TDDPhase,
    TestResult,
)


def test_tdd_phase_enum():
    """Test TDDPhase enum values."""
    assert TDDPhase.RED == "RED"
    assert TDDPhase.GREEN == "GREEN"
    assert TDDPhase.REFACTOR == "REFACTOR"


def test_test_result_model():
    """Test TestResult model."""
    result = TestResult(
        test_name="test_example",
        passed=False,
        failure_reason="AssertionError: expected 5, got 3",
        execution_time_ms=1.5,
    )
    assert result.test_name == "test_example"
    assert result.passed is False
    assert "AssertionError" in result.failure_reason
    assert result.execution_time_ms == 1.5


def test_tdd_cycle_model():
    """Test TDDCycle model."""
    cycle = TDDCycle(
        feature_description="Test feature",
        red_test_code="def test_example(): assert False",
        red_test_result=TestResult(
            test_name="test_example",
            passed=False,
            failure_reason="AssertionError",
        ),
        green_implementation="def example(): return True",
        green_test_result=TestResult(test_name="test_example", passed=True),
    )
    assert cycle.feature_description == "Test feature"
    assert cycle.red_test_result.passed is False
    assert cycle.green_test_result.passed is True


def test_red_phase_evaluation_model():
    """Test RedPhaseEvaluation model."""
    eval_result = RedPhaseEvaluation(
        test_fails_correctly=True,
        test_is_focused=True,
        test_name_descriptive=True,
        failure_message_clear=True,
        score=1.0,
        feedback="Excellent RED phase",
    )
    assert eval_result.test_fails_correctly is True
    assert eval_result.score == 1.0


def test_green_phase_evaluation_model():
    """Test GreenPhaseEvaluation model."""
    eval_result = GreenPhaseEvaluation(
        test_passes=True,
        implementation_minimal=True,
        no_test_hacking=True,
        no_regressions=True,
        score=1.0,
        feedback="Excellent GREEN phase",
    )
    assert eval_result.test_passes is True
    assert eval_result.score == 1.0


def test_refactor_phase_evaluation_model():
    """Test RefactorPhaseEvaluation model."""
    eval_result = RefactorPhaseEvaluation(
        tests_still_pass=True,
        behavior_unchanged=True,
        code_quality_improved=True,
        changes_atomic=True,
        appropriate_stopping_point=True,
        score=1.0,
        feedback="Excellent REFACTOR phase",
    )
    assert eval_result.tests_still_pass is True
    assert eval_result.score == 1.0


def test_full_cycle_evaluation_model():
    """Test FullCycleEvaluation model."""
    red_eval = RedPhaseEvaluation(
        test_fails_correctly=True,
        test_is_focused=True,
        test_name_descriptive=True,
        failure_message_clear=True,
        score=1.0,
        feedback="Good RED phase",
    )
    green_eval = GreenPhaseEvaluation(
        test_passes=True,
        implementation_minimal=True,
        no_test_hacking=True,
        no_regressions=True,
        score=1.0,
        feedback="Good GREEN phase",
    )
    full_eval = FullCycleEvaluation(
        red_evaluation=red_eval,
        green_evaluation=green_eval,
        overall_score=1.0,
        passed_tdd_discipline=True,
        summary="Excellent TDD cycle",
    )
    assert full_eval.overall_score == 1.0
    assert full_eval.passed_tdd_discipline is True


def test_score_validation():
    """Test that scores are validated to be between 0 and 1."""
    with pytest.raises(ValueError):
        RedPhaseEvaluation(
            test_fails_correctly=True,
            test_is_focused=True,
            test_name_descriptive=True,
            failure_message_clear=True,
            score=1.5,  # Invalid: > 1.0
            feedback="Test",
        )

    with pytest.raises(ValueError):
        GreenPhaseEvaluation(
            test_passes=True,
            implementation_minimal=True,
            no_test_hacking=True,
            no_regressions=True,
            score=-0.5,  # Invalid: < 0.0
            feedback="Test",
        )
