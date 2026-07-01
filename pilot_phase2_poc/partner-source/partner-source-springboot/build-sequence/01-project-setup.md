# 01 - Project Setup

## Status

- Status: Done
- Last Updated: 2026-07-02

## Purpose

Create the Spring Boot reference module with Java 21, Maven, and one tiny passing test.

## Source Docs To Read

- `../../AGREED_SPEC.md`
- `../../docs/active/springboot-implementation-handoff.md`
- `../../docs/support/implementation-schematic-and-task-sequence.md`

## Tests To Write First

Spring Initializr will generate the first scaffold test:

```text
src/test/java/com/waypoint/partnersource/PartnerSourceApplicationTests.java
```

Expected behavior:

- The application context loads.
- No Partner Source behavior is implemented yet.

## Code To Implement

Create or generate:

```text
pom.xml
mvnw
mvnw.cmd
.mvn/wrapper/
src/main/java/com/waypoint/partnersource/PartnerSourceApplication.java
src/test/java/com/waypoint/partnersource/PartnerSourceApplicationTests.java
```

Use:

| Setting | Value |
|---|---|
| Java | 21 |
| Build | Maven |
| Group | `com.waypoint` |
| Artifact | `partner-source-springboot` |
| Package | `com.waypoint.partnersource` |
| Dependencies | Spring Web, Spring Validation, Spring Boot Test |

## Commands To Run

### 1. Open The Module Folder

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-springboot
Get-ChildItem -Force
```

Expected before scaffold:

```text
README.md
build-sequence
```

### 2. Check Tools

```powershell
java -version
git --version
```

Expected:

- Java reports version `21`.
- Git is available.

Maven does not need to be installed globally if the Spring Initializr scaffold includes Maven Wrapper.

### 3. Generate The Spring Boot Project

Run this from `partner-source-springboot`.

This downloads a Spring Initializr project into a temp folder, then copies the generated project files into the current folder without deleting the existing `README.md` or `build-sequence/`.

```powershell
$ErrorActionPreference = "Stop"

cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-springboot

$starterZip = Join-Path $env:TEMP "partner-source-springboot-starter.zip"
$extractDir = Join-Path $env:TEMP "partner-source-springboot-starter"

if (Test-Path $starterZip) {
  Remove-Item -LiteralPath $starterZip -Force
}

if (Test-Path $extractDir) {
  Remove-Item -LiteralPath $extractDir -Recurse -Force
}

$query = @(
  "type=maven-project"
  "language=java"
  "baseDir=partner-source-springboot"
  "groupId=com.waypoint"
  "artifactId=partner-source-springboot"
  "name=partner-source-springboot"
  "description=Waypoint%20Partner%20Source%20Spring%20Boot%20reference%20implementation"
  "packageName=com.waypoint.partnersource"
  "packaging=jar"
  "javaVersion=21"
  "dependencies=web,validation"
) -join "&"

Invoke-WebRequest "https://start.spring.io/starter.zip?$query" -OutFile $starterZip
Expand-Archive -Path $starterZip -DestinationPath $extractDir

Copy-Item -Path (Join-Path $extractDir "partner-source-springboot\*") -Destination . -Recurse -Force
```

Expected generated files:

```text
pom.xml
mvnw
mvnw.cmd
.mvn/wrapper/
src/main/java/com/waypoint/partnersource/PartnerSourceSpringbootApplication.java
src/test/java/com/waypoint/partnersource/PartnerSourceSpringbootApplicationTests.java
```

### 4. Normalize The Application Class Name

Spring Initializr may generate `PartnerSourceSpringbootApplication`. Rename it to the agreed class name:

```powershell
$src = "src\main\java\com\waypoint\partnersource\PartnerSourceSpringbootApplication.java"
$dst = "src\main\java\com\waypoint\partnersource\PartnerSourceApplication.java"

if (Test-Path $src) {
  Move-Item -LiteralPath $src -Destination $dst -Force
  (Get-Content $dst) `
    -replace "PartnerSourceSpringbootApplication", "PartnerSourceApplication" |
    Set-Content -Path $dst -Encoding UTF8
}

$testSrc = "src\test\java\com\waypoint\partnersource\PartnerSourceSpringbootApplicationTests.java"
$testDst = "src\test\java\com\waypoint\partnersource\PartnerSourceApplicationTests.java"

if (Test-Path $testSrc) {
  Move-Item -LiteralPath $testSrc -Destination $testDst -Force
  (Get-Content $testDst) `
    -replace "PartnerSourceSpringbootApplicationTests", "PartnerSourceApplicationTests" |
    Set-Content -Path $testDst -Encoding UTF8
}
```

Expected files after rename:

```text
src/main/java/com/waypoint/partnersource/PartnerSourceApplication.java
src/test/java/com/waypoint/partnersource/PartnerSourceApplicationTests.java
```

### 5. Run The Scaffold Test

```powershell
.\mvnw.cmd test
```

If `mvnw.cmd` is missing, the scaffold did not generate correctly. Stop and fix the scaffold before continuing.

If Maven Wrapper exists but fails because of execution or download issues, try:

```powershell
mvn test
```

## Expected Output

```text
BUILD SUCCESS
```

## Done Criteria

- [x] `.\mvnw.cmd test` passes.
- [x] Package is `com.waypoint.partnersource`.
- [x] `pom.xml`, `mvnw`, `mvnw.cmd`, `.mvn/wrapper/`, `src/main/`, and `src/test/` exist.
- [x] No domain code or endpoints were added yet.

## Change Notes

- Spring Initializr generated the scaffold, but the first Java file picked up a hidden UTF-8 BOM from PowerShell.
- The application and test classes were rewritten cleanly to remove the encoding issue.
- The resulting setup is still the same intended scaffold: a minimal Spring Boot app with one passing context-load test.

## Stop / Do Not Add

- Do not add JPA, Actuator, Security, database drivers, Docker, or OpenAPI generation.
- Do not implement `/health` yet.
