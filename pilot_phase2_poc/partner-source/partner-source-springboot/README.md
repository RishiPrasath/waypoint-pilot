# Partner Source Spring Boot

Fresh Spring Boot reference implementation folder for Waypoint Phase 2 Partner Source.

This folder is intentionally not scaffolded yet. Build it from scratch by hand when you are ready.

## Role

Spring Boot is the first reference implementation.

It should prove the contract behavior before FastAPI parity work becomes meaningful.

## Starting Choices

| Area | Choice |
|---|---|
| Java | 21 |
| Build | Maven with Maven Wrapper |
| Package | `com.waypoint.partnersource` |
| Dependencies | Spring Web, Spring Validation, Spring Boot Test |
| Persistence | In-memory repositories only |
| Health | Custom `/health` and `/ready` |

Do not add JPA, H2, PostgreSQL, Spring Security, Actuator, Docker, deployment config, or OpenAPI server generation for Slice 1.

## First Manual Setup Target

Create a Spring Boot project here with:

```text
pom.xml
mvnw
mvnw.cmd
.mvn/wrapper/
src/main/java/com/waypoint/partnersource/PartnerSourceApplication.java
src/test/java/com/waypoint/partnersource/
```

First validation command:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-springboot
.\mvnw.cmd test
```

## First Real TDD Target

After the tiny scaffold test passes locally and in CI:

```text
StatusTransitionPolicyTest
```

Then:

```text
AssignmentAuthorizationPolicyTest
```

Follow the root checklist:

```text
..\MANUAL_BUILD_SEQUENCE.md
```

Use the numbered human build sequence for all instructions:

```text
build-sequence\00-index.md
```

For agreed behavior, use:

```text
..\AGREED_SPEC.md
```

Older long-form manuals are archived under `..\docs\archive\manuals\` for history only.
