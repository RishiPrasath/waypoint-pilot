from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


JsonValue = dict[str, Any] | list[Any] | str | int | float | bool | None


@dataclass(frozen=True)
class FieldExpectation:
    path: str
    expected: Any


@dataclass(frozen=True)
class Scenario:
    id: str
    use_case: str
    actor: str
    intent: str
    resource: str
    method: str
    path: str
    expected_status: int
    body: JsonValue = None
    expected_values: tuple[FieldExpectation, ...] = ()
    required_paths: tuple[str, ...] = ()
    compare_paths: tuple[str, ...] = ()
    contains_values: tuple[FieldExpectation, ...] = ()
    all_values: tuple[FieldExpectation, ...] = ()
    state_changing: bool = False


@dataclass(frozen=True)
class ResponseSnapshot:
    status_code: int
    body: JsonValue
    content_type: str = ""
    error: str | None = None


@dataclass(frozen=True)
class Mismatch:
    field: str
    expected: Any
    spring: Any
    fastapi: Any
    message: str


@dataclass
class ScenarioResult:
    scenario: Scenario
    spring: ResponseSnapshot
    fastapi: ResponseSnapshot
    mismatches: list[Mismatch] = field(default_factory=list)

    @property
    def status(self) -> str:
        return "PASS" if not self.mismatches else "FAIL"
