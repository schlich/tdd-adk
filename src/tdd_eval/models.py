"""Data models for TDD cycle evaluation."""

from enum import Enum

from pydantic import BaseModel, Field


class TDDPhase(str, Enum):
    """TDD cycle phases."""

    RED = "RED"
    GREEN = "GREEN"
    REFACTOR = "REFACTOR"


class TestResult(BaseModel):
    """Result of running a test."""

    test_name: str = Field(description="Name of the test")
    passed: bool = Field(description="Whether the test passed")
    failure_reason: str | None = Field(
        default=None, description="Reason for failure if test failed"
    )
    execution_time_ms: float | None = Field(
        default=None, description="Test execution time in milliseconds"
    )


class TDDCycle(BaseModel):
    """A complete TDD cycle with RED, GREEN, and REFACTOR phases."""

    feature_description: str = Field(description="Description of the feature being developed")

    # RED phase
    red_test_code: str = Field(description="Test code written in RED phase")
    red_test_result: TestResult = Field(description="Result of running the RED phase test")

    # GREEN phase
    green_implementation: str = Field(description="Implementation code in GREEN phase")
    green_test_result: TestResult = Field(description="Result after GREEN implementation")

    # REFACTOR phase (optional, can have multiple iterations)
    refactor_changes: list[str] = Field(
        default_factory=list, description="List of refactoring changes made"
    )
    refactor_test_results: list[TestResult] = Field(
        default_factory=list, description="Test results after each refactoring"
    )


class RedPhaseEvaluation(BaseModel):
    """Evaluation of the RED phase."""

    test_fails_correctly: bool = Field(
        description="Test fails for the right reason (not syntax error, etc.)"
    )
    test_is_focused: bool = Field(description="Test has ONE clear assertion")
    test_name_descriptive: bool = Field(
        description="Test name describes expected behavior"
    )
    failure_message_clear: bool = Field(description="Failure message is clear and helpful")
    score: float = Field(ge=0.0, le=1.0, description="Overall RED phase score (0-1)")
    feedback: str = Field(description="Detailed feedback on RED phase")


class GreenPhaseEvaluation(BaseModel):
    """Evaluation of the GREEN phase."""

    test_passes: bool = Field(description="Test now passes")
    implementation_minimal: bool = Field(
        description="Implementation is minimal (no over-engineering)"
    )
    no_test_hacking: bool = Field(
        description="No test code was modified to make test pass"
    )
    no_regressions: bool = Field(description="All other tests still pass")
    score: float = Field(ge=0.0, le=1.0, description="Overall GREEN phase score (0-1)")
    feedback: str = Field(description="Detailed feedback on GREEN phase")


class RefactorPhaseEvaluation(BaseModel):
    """Evaluation of the REFACTOR phase."""

    tests_still_pass: bool = Field(description="All tests still pass after refactoring")
    behavior_unchanged: bool = Field(description="Behavior is unchanged")
    code_quality_improved: bool = Field(
        description="Code quality improved (readability, maintainability)"
    )
    changes_atomic: bool = Field(description="Each refactoring change was atomic")
    appropriate_stopping_point: bool = Field(
        description="Refactoring stopped at appropriate point"
    )
    score: float = Field(ge=0.0, le=1.0, description="Overall REFACTOR phase score (0-1)")
    feedback: str = Field(description="Detailed feedback on REFACTOR phase")


class FullCycleEvaluation(BaseModel):
    """Complete evaluation of a TDD cycle."""

    red_evaluation: RedPhaseEvaluation
    green_evaluation: GreenPhaseEvaluation
    refactor_evaluation: RefactorPhaseEvaluation | None = Field(
        default=None, description="REFACTOR phase evaluation (if applicable)"
    )
    overall_score: float = Field(
        ge=0.0, le=1.0, description="Overall TDD cycle score (0-1)"
    )
    passed_tdd_discipline: bool = Field(
        description="Whether the cycle followed TDD discipline"
    )
    summary: str = Field(description="Summary of the evaluation")


class EvaluationResult(BaseModel):
    """Result of evaluating a TDD cycle."""

    cycle: TDDCycle
    evaluation: FullCycleEvaluation
