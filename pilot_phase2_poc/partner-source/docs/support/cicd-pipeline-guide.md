# CI/CD Pipeline Guide For Partner Source

## 1. Purpose

This document explains CI/CD for the local `partner-source` Spring Boot and FastAPI APIs.

It compares GitHub Actions and CircleCI, then recommends a beginner-friendly pipeline.

Current implementation note: the code modules are intentionally unscaffolded until Rishi builds them by hand. Use the numbered CI tasks as execution authority:

- `../../partner-source-springboot/build-sequence/02-ci-pipeline.md`
- `../../partner-source-fastapi/build-sequence/02-ci-pipeline.md`

Important scope decision:

```text
Each codebase gets its own CI/CD pipeline first.
Do not start with one collective application pipeline.
```

For now, that means:

- Spring Boot Partner Source API gets the first pipeline.
- FastAPI Partner Source API gets its own separate pipeline when that codebase starts.
- RAG/retriever, BFF, chatbot frontend, and mobile delivery frontend each get their own pipeline when those codebases start.
- A collective full-application pipeline is deferred until the separate module pipelines are stable.

## 2. What CI/CD Is

CI/CD is automation that checks your code every time it changes.

Beginner flow:

```text
you push code
-> CI/CD starts
-> downloads the repository
-> installs Java or Python
-> installs dependencies
-> builds the app
-> runs tests
-> reports pass or fail
-> optionally stores the built jar
```

CI means Continuous Integration.

For this project, CI should prove:

- code compiles
- tests pass
- application can be packaged later, after the scaffold path and artifact name are known
- OpenAPI contract can be validated later

CD means Continuous Delivery or Deployment.

For this project, CD is not needed first. Deployment can wait.

## 3. CI/CD Terms

| Term | Beginner Meaning | Partner-Source Example |
|---|---|---|
| Pipeline | Full automated process. | Build, test, package, validate contract. |
| Workflow | Named automation file. | `.github/workflows/partner-source-springboot-ci.yml` |
| Job | Group of steps running on a machine. | `build-and-test` |
| Step | One command or action. | `./mvnw test` or `python -m pytest` |
| Runner | Machine that runs the job. | Ubuntu GitHub-hosted runner. |
| Trigger | Event that starts the workflow. | Push or pull request. |
| Cache | Saved dependencies reused across runs. | Maven or pip dependency cache. |
| Artifact | File saved from the pipeline. | Built `.jar` file later, after packaging is useful. |
| Build | Compile or import/package the app. | Maven build or Python install/import check. |
| Test | Run automated checks. | JUnit or pytest tests. |

## 4. What The Pipeline Should Prove

For the first version, CI should prove:

```text
repository can be checked out
-> Java or Python can be installed
-> dependencies can be resolved
-> code compiles or imports
-> tests pass
-> packaging can be added later
```

Do not start with cloud deployment or artifact upload.

That would be CI/CD theatre at this stage: impressive-looking, not useful yet.

Use this first practice loop:

```text
create module skeleton
-> add one tiny test
-> make the local test command pass
-> add the workflow
-> make CI pass
-> begin real TDD feature work
```

## 5. GitHub Actions

GitHub Actions is GitHub's built-in automation system.

Workflow files live here:

```text
.github/workflows/
```

Why it fits this project:

- repository is expected to live on GitHub
- pull request checks are native
- setup is beginner-friendly
- Java/Maven examples are officially documented
- Java and Python examples are officially documented
- dependency caching is simple with `actions/setup-java` and `actions/setup-python`
- no separate CI provider account is needed

## 6. CircleCI

CircleCI is an external CI/CD platform.

Config lives here:

```text
.circleci/config.yml
```

CircleCI is strong, but it introduces more setup:

- connect GitHub repo to CircleCI
- understand CircleCI projects, workflows, jobs, and credits
- configure caching more manually
- use Docker images or orbs

It is a good tool, but it is not the easiest first tool for this project.

## 7. GitHub Actions vs CircleCI

| Criterion | GitHub Actions | CircleCI | Better For This Project |
|---|---|---|---|
| Beginner setup | Directly in GitHub repo | Requires CircleCI project setup | GitHub Actions |
| GitHub pull request integration | Native | Good but external | GitHub Actions |
| Java/Spring Boot support | Strong, official Java/Maven guide | Strong, Docker images and orbs | Tie |
| Dependency caching | Simple with `setup-java cache: maven` | Powerful but more manual | GitHub Actions |
| Learning curve | Lower | Slightly higher | GitHub Actions |
| Artifacts | Native artifact actions | Native artifact storage | Tie |
| Advanced workflows | Strong | Very strong | CircleCI |
| Portability outside GitHub | Lower | Higher | CircleCI |
| Solo developer fit | Excellent | Good but more overhead | GitHub Actions |

## 8. Recommendation

Use GitHub Actions first.

Reason:

```text
beginner developer
+ GitHub-hosted project
+ Spring Boot Maven build and FastAPI pytest build
+ need simple build/test confidence
+ direct pull request checks
= GitHub Actions is the right first CI/CD tool
```

Use CircleCI later only if:

- you want to learn a second CI/CD provider
- you need more advanced workflow orchestration
- you want external CI provider experience
- you want better portability outside GitHub

Keep each first CI/CD pipeline scoped to one Partner Source implementation. Do not combine Spring Boot, FastAPI, RAG, BFF, or frontend checks yet.

## 9. Beginner Spring Boot GitHub Actions Pipeline

For the Spring Boot Maven scaffold in `pilot_phase2_poc/partner-source/partner-source-springboot/`:

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
    branches: [ main ]
    paths:
      - "pilot_phase2_poc/partner-source/partner-source-springboot/**"
      - "pilot_phase2_poc/partner-source/docs/**"
      - "pilot_phase2_poc/partner-source/AGREED_SPEC.md"
      - ".github/workflows/partner-source-springboot-ci.yml"

permissions:
  contents: read

jobs:
  test:
    name: Test Spring Boot API
    runs-on: ubuntu-latest

    defaults:
      run:
        working-directory: pilot_phase2_poc/partner-source/partner-source-springboot

    steps:
      - name: Checkout source
        uses: actions/checkout@v4

      - name: Set up JDK 21
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '21'
          cache: maven

      - name: Run tests
        run: ./mvnw test
```

This should be treated as a first draft, not final production CI.

If the generated scaffold uses a different folder name, change the path filters and `working-directory` before enabling the workflow.

Use `./mvnw test` first. Move to `./mvnw verify` after contract checks or integration checks are bound to the Maven verify phase.

## 10. Beginner FastAPI GitHub Actions Pipeline

For the FastAPI scaffold in `pilot_phase2_poc/partner-source/partner-source-fastapi/`:

```yaml
name: Partner Source FastAPI CI

on:
  pull_request:
    paths:
      - "pilot_phase2_poc/partner-source/partner-source-fastapi/**"
      - "pilot_phase2_poc/partner-source/docs/**"
      - "pilot_phase2_poc/partner-source/AGREED_SPEC.md"
      - ".github/workflows/partner-source-fastapi-ci.yml"
  push:
    branches: [ main ]
    paths:
      - "pilot_phase2_poc/partner-source/partner-source-fastapi/**"
      - "pilot_phase2_poc/partner-source/docs/**"
      - "pilot_phase2_poc/partner-source/AGREED_SPEC.md"
      - ".github/workflows/partner-source-fastapi-ci.yml"

permissions:
  contents: read

jobs:
  test:
    name: Test FastAPI API
    runs-on: ubuntu-latest

    defaults:
      run:
        working-directory: pilot_phase2_poc/partner-source/partner-source-fastapi

    steps:
      - name: Checkout source
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: pip

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt -r requirements-dev.txt

      - name: Run tests
        run: python -m pytest
```

Add linting and coverage later, after the basic pytest pipeline is green.

## 11. Beginner CircleCI Equivalent

If you later want to compare CircleCI:

```yaml
version: 2.1

jobs:
  build-and-test:
    working_directory: ~/project/partner-source
    docker:
      - image: cimg/openjdk:21.0
    steps:
      - checkout

      - restore_cache:
          keys:
            - maven-deps-{{ checksum "pom.xml" }}
            - maven-deps-

      - run:
          name: Build and test
          command: mvn -B verify

      - save_cache:
          paths:
            - ~/.m2
          key: maven-deps-{{ checksum "pom.xml" }}

workflows:
  partner-source-ci:
    jobs:
      - build-and-test
```

If the generated scaffold uses a different folder name, change `working_directory` before enabling this comparison workflow. Add `store_artifacts` later when package output matters.

## 12. Separate Pipeline Roadmap

Do not merge module checks into one pipeline yet. Use a separate CI/CD pipeline per codebase.

| Order | Codebase | Pipeline Name | First CI Responsibility | When To Add |
|---:|---|---|---|---|
| 1 | Partner Source API - Spring Boot | `partner-source-springboot-ci` | Run Java setup and `./mvnw test` from the Spring Boot scaffold. | First. |
| 2 | Partner Source API - FastAPI | `partner-source-fastapi-ci` | Run Python setup and `python -m pytest` from the FastAPI scaffold. | When FastAPI codebase starts. |
| 3 | RAG/retriever module | `rag-retriever-ci` | Run retrieval unit tests, evaluation smoke checks, and source/citation safety checks. | When RAG/retriever implementation starts. |
| 4 | BFF | `bff-ci` | Run BFF tests and upstream contract-shape checks. | When BFF implementation starts. |
| 5 | Chatbot frontend | `chatbot-frontend-ci` | Run frontend test/build checks for chatbot flows. | When chatbot frontend starts. |
| 6 | Mobile delivery frontend | `mobile-delivery-frontend-ci` | Run mobile/front-end test/build checks for driver flows. | When mobile delivery frontend starts. |
| Later | Collective application | `waypoint-integration-ci` | Run cross-module integration/regression checks. | Only after separate module pipelines are stable. |

Beginner rule:

```text
One codebase = one CI/CD pipeline first.
Collective orchestration comes later.
```

## 13. Pipeline Growth

Grow each Partner Source pipeline in this order:

| Phase | Goal | Pipeline Step |
|---|---|---|
| Phase 1 | Prove the module test runner works | `./mvnw test` or `python -m pytest` |
| Phase 2 | Protect OpenAPI | Validate `partner-source.v1.yaml` |
| Phase 3 | Add contract checks | Run Partner Source contract assertions from the module pipeline |
| Phase 4 | Add test reports | Publish test output |
| Phase 5 | Package artifact | Upload a jar or Python artifact only after artifact path is confirmed |
| Phase 6 | Optional deployment | Docker image and deployment target |

## 14. OpenAPI Validation Later

After implementation starts, CI should also validate the OpenAPI contract.

Possible future checks:

```text
lint OpenAPI YAML
-> check schema validity
-> run API tests
-> compare implementation behavior to contract
```

Do this after the first tests exist. Otherwise CI will become a pile of ceremony with no safety value.

## 15. What To Learn First

Learn these in order:

1. What a YAML file is.
2. What workflow, job, step, runner, and trigger mean.
3. How Maven works: `compile`, `test`, `package`, `verify`.
4. How pytest discovers and runs tests.
5. How GitHub Actions triggers on `push` and `pull_request`.
6. How Java is installed in CI using `actions/setup-java`.
7. How Python is installed in CI using `actions/setup-python`.
8. How dependency caching speeds up builds.
9. How test failures block bad changes.
10. How artifacts store built outputs later.
11. How OpenAPI validation becomes a quality gate.
12. How deployment differs from CI.

## 16. Source Links

- [GitHub Actions - Workflows](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows)
- [GitHub Actions - Building and Testing Java with Maven](https://docs.github.com/en/actions/tutorials/build-and-test-code/java-with-maven)
- [GitHub Actions - Building and Testing Python](https://docs.github.com/en/actions/tutorials/build-and-test-code/python)
- [GitHub Actions - Billing and Usage](https://docs.github.com/en/actions/concepts/billing-and-usage)
- [GitHub `setup-java` Action](https://github.com/actions/setup-java)
- [GitHub `setup-python` Action](https://github.com/actions/setup-python)
- [pytest Getting Started](https://docs.pytest.org/en/stable/getting-started.html)
- [CircleCI - Pipelines](https://circleci.com/docs/guides/orchestrate/pipelines/)
- [CircleCI - Concepts](https://circleci.com/docs/guides/about-circleci/concepts/)
- [CircleCI - Pricing Planner](https://circleci.com/pricing/build-your-plan/)
- [Apache Maven Build Lifecycle](https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html)
