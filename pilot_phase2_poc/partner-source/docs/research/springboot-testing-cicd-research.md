# Spring Boot, Testing, And CI/CD Research Hub

## 1. Purpose

This page is the research hub for the beginner learning material behind the `partner-source` implementation.

The detailed research has been split into three focused documents:

| Area | Document | Purpose |
|---|---|---|
| Spring Boot API basics | [../support/springboot-api-fundamentals.md](../support/springboot-api-fundamentals.md) | Explains what Spring Boot is, how APIs are structured, and what classes/concepts are needed. |
| Testing | [../support/springboot-testing-playbook.md](../support/springboot-testing-playbook.md) | Explains unit, controller, repository, integration, and TDD testing for the API. |
| CI/CD | [../support/cicd-pipeline-guide.md](../support/cicd-pipeline-guide.md) | Explains CI/CD, compares GitHub Actions and CircleCI, and proposes a beginner pipeline. |

This hub exists so the research remains easy to navigate instead of being buried inside one giant page.

## 2. Executive Recommendation

For `partner-source`, use this project direction:

```text
Spring Boot REST API
-> contract-first with OpenAPI
-> feature-based package structure
-> DTOs separate from database entities
-> service layer coordinates use cases
-> domain policies enforce lifecycle rules
-> repositories handle persistence
-> scenario-driven seed data
-> JUnit 5 + Mockito + MockMvc testing
-> GitHub Actions CI first
```

## 3. Recommended Learning Order

1. Learn what Spring Boot is.
2. Learn REST controllers and API endpoints.
3. Learn DTOs, validation, and error handling.
4. Learn services and domain policies.
5. Learn repositories, JPA, and database configuration.
6. Learn seed data.
7. Learn JUnit 5 testing basics.
8. Learn Mockito and MockMvc.
9. Learn repository and integration testing.
10. Learn GitHub Actions CI.
11. Add OpenAPI validation to CI later.

## 4. Current Project Decision

The research supports this implementation sequence:

```text
design contract
-> define seed scenarios
-> write tests
-> implement Spring Boot API
-> add GitHub Actions CI
-> expand later to database realism and deployment
```

## 5. Source Families

The detailed documents rely mostly on official documentation:

- Spring Boot documentation
- Spring Framework documentation
- Spring Data JPA documentation
- Hibernate documentation
- JUnit 5 documentation
- Mockito documentation
- GitHub Actions documentation
- CircleCI documentation
- Maven documentation
