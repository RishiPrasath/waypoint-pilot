from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_contract_sources_exist() -> None:
    required_paths = [
        ROOT / "AGREED_SPEC.md",
        ROOT / "docs" / "research" / "use-cases.md",
        ROOT / "docs" / "research" / "use-case-resource-map.md",
        ROOT / "docs" / "contracts" / "openapi" / "partner-source.v1.yaml",
        ROOT / "docs" / "contracts" / "openapi" / "http" / "partner-source-slice1.http",
        ROOT / "docs" / "contracts" / "shared-error-contract.md",
    ]

    missing = [str(path) for path in required_paths if not path.exists()]

    assert missing == []
