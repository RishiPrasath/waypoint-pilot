from __future__ import annotations

from scripts.json_path import MISSING, values_at
from scripts.models import Mismatch, ResponseSnapshot, Scenario, ScenarioResult


def compare_scenario(
    scenario: Scenario,
    spring: ResponseSnapshot,
    fastapi: ResponseSnapshot,
) -> ScenarioResult:
    mismatches: list[Mismatch] = []

    _compare_status(scenario, spring, fastapi, mismatches)
    _compare_required_paths(scenario, spring, fastapi, mismatches)
    _compare_expected_values(scenario, spring, fastapi, mismatches)
    _compare_contains_values(scenario, spring, fastapi, mismatches)
    _compare_all_values(scenario, spring, fastapi, mismatches)
    _compare_peer_values(scenario, spring, fastapi, mismatches)

    return ScenarioResult(scenario=scenario, spring=spring, fastapi=fastapi, mismatches=mismatches)


def _compare_status(
    scenario: Scenario,
    spring: ResponseSnapshot,
    fastapi: ResponseSnapshot,
    mismatches: list[Mismatch],
) -> None:
    if spring.status_code != scenario.expected_status or fastapi.status_code != scenario.expected_status:
        mismatches.append(
            Mismatch(
                field="HTTP status",
                expected=scenario.expected_status,
                spring=spring.status_code,
                fastapi=fastapi.status_code,
                message="HTTP status did not match expected value.",
            )
        )


def _compare_required_paths(
    scenario: Scenario,
    spring: ResponseSnapshot,
    fastapi: ResponseSnapshot,
    mismatches: list[Mismatch],
) -> None:
    for path in scenario.required_paths:
        spring_value = values_at(spring.body, path)
        fastapi_value = values_at(fastapi.body, path)
        if spring_value is MISSING or fastapi_value is MISSING:
            mismatches.append(
                Mismatch(
                    field=path,
                    expected="present",
                    spring=_display_value(spring_value),
                    fastapi=_display_value(fastapi_value),
                    message="Required field was missing.",
                )
            )


def _compare_expected_values(
    scenario: Scenario,
    spring: ResponseSnapshot,
    fastapi: ResponseSnapshot,
    mismatches: list[Mismatch],
) -> None:
    for expectation in scenario.expected_values:
        spring_value = values_at(spring.body, expectation.path)
        fastapi_value = values_at(fastapi.body, expectation.path)
        if spring_value != expectation.expected or fastapi_value != expectation.expected:
            mismatches.append(
                Mismatch(
                    field=expectation.path,
                    expected=expectation.expected,
                    spring=_display_value(spring_value),
                    fastapi=_display_value(fastapi_value),
                    message="Field did not match expected value.",
                )
            )


def _compare_contains_values(
    scenario: Scenario,
    spring: ResponseSnapshot,
    fastapi: ResponseSnapshot,
    mismatches: list[Mismatch],
) -> None:
    for expectation in scenario.contains_values:
        expected_values = tuple(expectation.expected)
        spring_value = values_at(spring.body, expectation.path)
        fastapi_value = values_at(fastapi.body, expectation.path)
        spring_missing = _missing_contains(spring_value, expected_values)
        fastapi_missing = _missing_contains(fastapi_value, expected_values)
        if spring_missing or fastapi_missing:
            mismatches.append(
                Mismatch(
                    field=expectation.path,
                    expected=f"contains {expected_values}",
                    spring=_display_value(spring_value),
                    fastapi=_display_value(fastapi_value),
                    message=f"Expected values missing. Spring missing={spring_missing}; FastAPI missing={fastapi_missing}.",
                )
            )


def _compare_all_values(
    scenario: Scenario,
    spring: ResponseSnapshot,
    fastapi: ResponseSnapshot,
    mismatches: list[Mismatch],
) -> None:
    for expectation in scenario.all_values:
        spring_value = values_at(spring.body, expectation.path)
        fastapi_value = values_at(fastapi.body, expectation.path)
        spring_bad = _non_matching_values(spring_value, expectation.expected)
        fastapi_bad = _non_matching_values(fastapi_value, expectation.expected)
        if spring_bad or fastapi_bad:
            mismatches.append(
                Mismatch(
                    field=expectation.path,
                    expected=f"all values equal {expectation.expected}",
                    spring=_display_value(spring_value),
                    fastapi=_display_value(fastapi_value),
                    message=f"Unexpected values found. Spring={spring_bad}; FastAPI={fastapi_bad}.",
                )
            )


def _compare_peer_values(
    scenario: Scenario,
    spring: ResponseSnapshot,
    fastapi: ResponseSnapshot,
    mismatches: list[Mismatch],
) -> None:
    for path in scenario.compare_paths:
        spring_value = values_at(spring.body, path)
        fastapi_value = values_at(fastapi.body, path)
        if spring_value != fastapi_value:
            mismatches.append(
                Mismatch(
                    field=path,
                    expected="Spring Boot and FastAPI values match",
                    spring=_display_value(spring_value),
                    fastapi=_display_value(fastapi_value),
                    message="Spring Boot and FastAPI returned different values.",
                )
            )


def _missing_contains(actual: object, expected_values: tuple[object, ...]) -> tuple[object, ...]:
    if not isinstance(actual, list):
        return expected_values
    return tuple(value for value in expected_values if value not in actual)


def _non_matching_values(actual: object, expected: object) -> tuple[object, ...]:
    if not isinstance(actual, list):
        return (actual,)
    return tuple(value for value in actual if value != expected)


def _display_value(value: object) -> object:
    if value is MISSING:
        return "<missing>"
    return value
