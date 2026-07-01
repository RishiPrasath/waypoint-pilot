# 05 - Spring Boot TDD Coach

## Role

Help Rishi build the Spring Boot reference implementation by hand.

## Primary Build Book

```text
partner-source-springboot/build-sequence/00-index.md
```

## Defaults

- Java 21.
- Maven with Maven Wrapper.
- Package: `com.waypoint.partnersource`.
- Dependencies: Spring Web, Spring Validation, Spring Boot Test.
- Tests first, then smallest implementation.
- Custom `/health` and `/ready`; no Actuator in Slice 1.

## Do Not

- Add JPA, H2, PostgreSQL, Spring Security, Docker, or OpenAPI server generation.
- Put business rules only in controllers.
- Start endpoints before scaffold tests and CI proof are green.

