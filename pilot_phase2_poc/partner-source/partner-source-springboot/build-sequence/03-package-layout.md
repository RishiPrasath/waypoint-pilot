# 03 - Package Layout

## Purpose

Prepare the feature-based package structure before adding real behavior.

## Source Docs To Read

- `../../docs/support/implementation-schematic-and-task-sequence.md`
- `../../docs/active/implementation-mapping.md`

## Tests To Write First

No behavior test. This is folder preparation after the scaffold test and CI proof are green.

## Code To Implement

Create this package layout under:

```text
src/main/java/com/waypoint/partnersource/
```

```text
order/api/dto
order/domain
order/repository
order/service
driver/api/dto
driver/domain
driver/repository
driver/service
assignment/domain
assignment/repository
shared/error
shared/health
shared/seed
```

Create matching test folders under:

```text
src/test/java/com/waypoint/partnersource/
```

```text
order/domain
order/repository
order/service
order/api
driver/repository
driver/service
driver/api
assignment/domain
shared/health
shared/error
integration
```

## Commands To Run

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-springboot
New-Item -ItemType Directory -Force -Path `
  src\main\java\com\waypoint\partnersource\order\api\dto,`
  src\main\java\com\waypoint\partnersource\order\domain,`
  src\main\java\com\waypoint\partnersource\order\repository,`
  src\main\java\com\waypoint\partnersource\order\service,`
  src\main\java\com\waypoint\partnersource\driver\api\dto,`
  src\main\java\com\waypoint\partnersource\driver\domain,`
  src\main\java\com\waypoint\partnersource\driver\repository,`
  src\main\java\com\waypoint\partnersource\driver\service,`
  src\main\java\com\waypoint\partnersource\assignment\domain,`
  src\main\java\com\waypoint\partnersource\assignment\repository,`
  src\main\java\com\waypoint\partnersource\shared\error,`
  src\main\java\com\waypoint\partnersource\shared\health,`
  src\main\java\com\waypoint\partnersource\shared\seed
```

Then run:

```powershell
.\mvnw.cmd test
```

## Done Criteria

- [ ] Folder structure exists.
- [ ] Scaffold test still passes.
- [ ] No placeholder behavior classes were added just to fill folders.

## Stop / Do Not Add

- Do not add controllers before domain policies.
- Do not add repository implementations before seed data tests.
