# 01 - Project Setup

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Create the Spring Boot reference module with Java 21, Maven Wrapper, and one tiny passing context-load test.

## Source Docs To Read

- `../../AGREED_SPEC.md`
- `../../docs/active/springboot-implementation-handoff.md`
- `../../docs/support/implementation-schematic-and-task-sequence.md`

## Prereqs

- Java 21 is installed and active.
- Work inside `partner-source-springboot`.
- Keep existing `README.md` and `build-sequence/` files.

## Tests To Write First

Create:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `src/test/java/com/waypoint/partnersource/PartnerSourceApplicationTests.java`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
src/test/java/com/waypoint/partnersource/PartnerSourceApplicationTests.java
```

Use this exact scaffold test:

**Test Block Explanation**

- What this block does: Shows the test code to write first for Use this exact scaffold test.
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

Expected behavior: the application context loads and no Partner Source behavior exists yet.
## File Map

Create or generate:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for Create or generate.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
pom.xml
mvnw
mvnw.cmd
.mvn/wrapper/
src/main/java/com/waypoint/partnersource/PartnerSourceApplication.java
src/test/java/com/waypoint/partnersource/PartnerSourceApplicationTests.java
src/main/resources/application.properties

```

## Exact Code

`pom.xml` must target Java 21:

**Code Block Explanation**

- What this block does: Shows the exact XML code for `pom.xml`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read it top-down and keep the names, paths, and casing exactly as shown.

```xml
<properties>
    <java.version>21</java.version>
</properties>
```

Create `PartnerSourceApplication.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `PartnerSourceApplication.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class PartnerSourceApplication {
    public static void main(String[] args) {
        SpringApplication.run(PartnerSourceApplication.class, args);
    }
}

```

Create `PartnerSourceApplicationTests.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `PartnerSourceApplicationTests.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

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

If Initializr creates `PartnerSourceSpringbootApplication`, rename it to `PartnerSourceApplication` and rename the test class too.

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-springboot
java -version
.\mvnw.cmd test
```

## Done Criteria

- [x] `pom.xml`, `mvnw`, `mvnw.cmd`, `.mvn/wrapper/`, `src/main/`, and `src/test/` exist.
- [x] Package is `com.waypoint.partnersource`.
- [x] Context-load test passes.
- [x] No domain code or endpoints were added in this task.

## Common Mistakes

- Running with Java 17 and hitting `release version 21 not supported`.
- Leaving the generated class name as `PartnerSourceSpringbootApplication`.
- Adding `/health` or domain classes during scaffold setup.

## Stop / Do Not Add

- Do not add JPA, Actuator, Security, database drivers, Docker, or OpenAPI generation.
- Do not implement `/health` yet.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized to the shared build-task format.
- Existing scaffold is complete.
