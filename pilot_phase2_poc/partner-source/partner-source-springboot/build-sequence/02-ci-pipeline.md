# 02 - CI Pipeline

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Create a simple GitHub Actions workflow that proves the Spring Boot module tests run in CI.

## Source Docs To Read

- `../../docs/support/cicd-pipeline-guide.md`
- `../../docs/active/test-and-acceptance-handoff.md`
- `01-project-setup.md`

## Prereqs

- Task 01 is complete.
- `mvnw` and `mvnw.cmd` exist.
- Local `.\mvnw.cmd test` passes before pushing.

## Tests To Write First

No new behavior test for this task.

The CI task proves that this existing scaffold test runs in GitHub Actions:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for The CI task proves that this existing scaffold test runs in GitHub Actions.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
src/test/java/com/waypoint/partnersource/PartnerSourceApplicationTests.java
```

Expected content:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `package com.waypoint.partnersource;`, `import org.junit.jupiter.api.Test;`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```java
package com.waypoint.partnersource;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class PartnerSourceApplicationTests {

    @Test
    void contextLoads() {
    }
}

```

The workflow is done when CI runs `./mvnw test` against the module.
## File Map

Create from repository root:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for Create from repository root.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
.github/workflows/partner-source-springboot-ci.yml
```

## Exact Code

Create `.github/workflows/partner-source-springboot-ci.yml`:

**Code Block Explanation**

- What this block does: Shows the exact YAML configuration for `.github/workflows/partner-source-springboot-ci.yml`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read indentation carefully: top-level keys define the workflow, nested keys define jobs and steps.

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
      - uses: actions/checkout@v5
      - uses: actions/setup-java@v5
        with:
          distribution: temurin
          java-version: "21"
          cache: maven
      - run: chmod +x ./mvnw
      - run: ./mvnw test

```

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-springboot
.\mvnw.cmd test

```

From repo root:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for From repo root.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot
git status --short

```

## Done Criteria

- [x] Workflow file exists at repo root.
- [x] Workflow uses Java 21.
- [x] Workflow runs `./mvnw test`.
- [x] Workflow path filters include this module and local docs/contracts.
- [x] CI is green after push or PR.

## Common Mistakes

- Putting the workflow under `partner-source-springboot/.github` instead of repo root `.github`.
- Using Java 17 in CI while Maven compiles with release 21.
- Adding deployment or Docker publishing here.

## Stop / Do Not Add

- Do not add deployment.
- Do not add Docker publishing.
- Do not add coverage or linting until the basic test pipeline is green.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized to the shared build-task format.
- CI remains a simple Java 21 Maven test gate.
