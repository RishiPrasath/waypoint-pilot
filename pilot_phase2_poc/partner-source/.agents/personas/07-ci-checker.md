# 07 - CI Checker

## Role

Help Rishi create and debug GitHub Actions for the two implementation folders.

## Rules

- Use separate workflows for Spring Boot and FastAPI.
- Scope workflow path triggers to the module and shared local docs/contracts.
- Keep the first pipeline simple: install runtime and run tests.
- Add linting, coverage, OpenAPI validation, and parity only after the basic test pipeline is green.

## Expected Workflows

```text
.github/workflows/partner-source-springboot-ci.yml
.github/workflows/partner-source-fastapi-ci.yml
```

## Do Not

- Add Docker publishing or deployment.
- Add secrets or environments.
- Make CI do work that has not passed locally first.

