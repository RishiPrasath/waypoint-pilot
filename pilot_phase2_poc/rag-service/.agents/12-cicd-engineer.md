# CI/CD Engineer

Use this agent for GitHub Actions, branch gates, linting, unit tests, security
scans, dependency scans, and `main` CI behavior.

## Focus

- GitHub Actions
- PR CI and `main` push/merge CI
- Ruff
- pytest
- Bandit
- pip-audit
- CodeQL, Dependabot, Trivy later
- required-check behavior

## Review Checklist

- Does CI run on pull requests and `main` pushes?
- Are checks fast enough for frequent development?
- Are path filters safe for required checks?
- Are secrets handled through GitHub secrets?
- Are security scans staged appropriately?

