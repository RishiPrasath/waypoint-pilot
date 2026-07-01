# 02 - Slice 1 No Scope Creep

Do not add these unless the plan changes deliberately:

- [ ] Database persistence.
- [ ] JPA, H2, PostgreSQL, SQLAlchemy, or Alembic.
- [ ] Authentication or authorization systems beyond assignment authorization policy.
- [ ] Docker, deployment, cloud config, or secrets.
- [ ] Spring Boot Actuator.
- [ ] OpenAPI server-code generation.
- [ ] New endpoints.
- [ ] New enum values.
- [ ] New seed records outside the agreed scenarios.
- [ ] Delivery-attempt behavior for `DELIVERY_ATTEMPTED`.

Slice 1 is contract behavior, deterministic seed data, tests, and CI.

