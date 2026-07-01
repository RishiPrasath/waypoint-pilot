# 02 - CI Pipeline

## Purpose

Create a simple GitHub Actions workflow that proves the Spring Boot module tests run in CI.

## Source Docs To Read

- `../../docs/support/cicd-pipeline-guide.md`
- `../../docs/active/test-and-acceptance-handoff.md`
- `01-project-setup.md`

## Tests To Write First

No new behavior test. The scaffold test from step 01 is the CI proof.

## Code To Implement

Create from the repository root:

```text
.github/workflows/partner-source-springboot-ci.yml
```

Use this workflow:

```yaml
name: Partner Source Spring Boot CI

on:
  pull_request:
    paths:
      - "pilot_phase2_poc/partner-source/partner-source-springboot/**"
      - "pilot_phase2_poc/partner-source/docs/**"
      - "pilot_phase2_poc/partner-source/AGREED_SPEC.md"
      - ".github/workflows/partner-source-springboot-ci.yml"
  push:
    branches: [main]
    paths:
      - "pilot_phase2_poc/partner-source/partner-source-springboot/**"
      - "pilot_phase2_poc/partner-source/docs/**"
      - "pilot_phase2_poc/partner-source/AGREED_SPEC.md"
      - ".github/workflows/partner-source-springboot-ci.yml"

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: pilot_phase2_poc/partner-source/partner-source-springboot
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: "21"
          cache: maven
      - run: chmod +x ./mvnw
      - run: ./mvnw test
```

## Commands To Run

Before pushing:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-springboot
.\mvnw.cmd test
```

Check Git from repo root:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot
git status --short
```

## Expected Output

- Local test: `BUILD SUCCESS`.
- GitHub Actions: workflow completes green.

## Done Criteria

- [ ] Workflow file exists at repo root.
- [ ] Workflow uses Java 21.
- [ ] Workflow runs `./mvnw test`.
- [ ] Workflow path filters include this module and local docs/contracts.
- [ ] CI is green after push or PR.

## Stop / Do Not Add

- Do not add deployment.
- Do not add Docker publishing.
- Do not add coverage or linting until the basic test pipeline is green.

