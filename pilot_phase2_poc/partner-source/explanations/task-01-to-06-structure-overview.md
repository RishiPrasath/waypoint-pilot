# Tasks 01 To 06 Structure Overview

This note explains what we built from task 1 through task 6 and how the code structure is starting to fit together.

The short version:

```text
Task 01 gives us a Spring Boot app.
Task 02 proves tests can run in CI.
Task 03 creates the package map.
Task 04 adds the first order domain rule.
Task 05 adds the first assignment domain rule.
Task 06 adds seed data and in-memory repositories.
```

At this point, we are not building HTTP endpoints yet. We are building the inside of the app first.

## Big Picture

The project is a fake logistics partner API.

Waypoint will eventually call this API to ask things like:

```text
What is the status of order ORD-1001?
Who is driver DRV-2001?
Which assignments does DRV-2001 have?
Can this driver update this order?
Can this order move from OUT_FOR_DELIVERY to DELIVERED?
```

Before we expose HTTP endpoints, we need the internal model:

```text
domain rules
seed data
repositories
tests
```

That is what tasks 1 through 6 are setting up.

## Mental Model

Think of the app in layers:

```text
API layer       future controllers and DTOs
Service layer   future business workflows
Repository      read/write access to seed data
Seed layer      fake deterministic data
Domain layer    core business concepts and rules
```

So far we mostly built the lower layers:

```text
Domain layer
Seed layer
Repository layer
```

The API and service layers come later.

## Task 01 - Project Setup

Task 1 created the Spring Boot module itself.

Important files:

```text
partner-source-springboot/pom.xml
partner-source-springboot/mvnw
partner-source-springboot/mvnw.cmd
partner-source-springboot/src/main/java/com/waypoint/partnersource/PartnerSourceApplication.java
partner-source-springboot/src/test/java/com/waypoint/partnersource/PartnerSourceApplicationTests.java
partner-source-springboot/src/main/resources/application.properties
```

What this means:

```text
pom.xml              Maven project configuration
mvnw / mvnw.cmd      Maven wrapper so everyone runs the same Maven
PartnerSourceApplication.java  Spring Boot entrypoint
application.properties         app configuration file
PartnerSourceApplicationTests  first smoke test
```

The test in task 1 does not test business behavior.

It only asks:

```text
Can Spring Boot start the application context?
```

That is why the test is called:

```java
contextLoads()
```

## Task 02 - CI Pipeline

Task 2 created the GitHub Actions workflow.

Important file:

```text
.github/workflows/partner-source-springboot-ci.yml
```

This is not application code. It is automation.

The purpose is:

```text
When code is pushed or opened in a PR, GitHub should run the Spring Boot tests.
```

So task 2 connects the local project to CI proof.

The important idea:

```text
Local test passing is good.
CI test passing is stronger proof.
```

## Task 03 - Package Layout

Task 3 created the folder structure before adding behavior.

The package root is:

```text
com.waypoint.partnersource
```

Under that root, we created feature-based packages:

```text
order
driver
assignment
shared
```

This is important. We are not organizing by generic technical buckets first. We are organizing mostly by business feature.

## Main Package Families

### order

Order code lives here:

```text
src/main/java/com/waypoint/partnersource/order/
```

Current and future subfolders:

```text
order/domain
order/repository
order/service
order/api
order/api/dto
```

What `order` is about:

```text
Delivery orders
Order status
Order status timeline
Order status changes
```

Current files include:

```text
order/domain/OrderStatus.java
order/domain/StatusTransitionPolicy.java
order/domain/ActorType.java
order/domain/DeliveryOrder.java
order/domain/OrderStatusEvent.java
order/repository/InMemoryOrderRepository.java
order/repository/InMemoryStatusEventRepository.java
```

### driver

Driver code lives here:

```text
src/main/java/com/waypoint/partnersource/driver/
```

What `driver` is about:

```text
Driver profile
Driver availability
Eventually driver API responses
```

Current files include:

```text
driver/domain/DeliveryDriver.java
driver/domain/DriverAvailabilityStatus.java
driver/repository/InMemoryDriverRepository.java
```

### assignment

Assignment code lives here:

```text
src/main/java/com/waypoint/partnersource/assignment/
```

What `assignment` is about:

```text
Which driver is assigned to which order
Whether a driver may update an order
Assignment status
```

Current files include:

```text
assignment/domain/AssignmentStatus.java
assignment/domain/DeliveryAssignment.java
assignment/domain/AssignmentAuthorizationPolicy.java
assignment/repository/InMemoryAssignmentRepository.java
```

### shared

Shared code lives here:

```text
src/main/java/com/waypoint/partnersource/shared/
```

What `shared` is about:

```text
Cross-feature support code
Seed data
Error handling later
Health/readiness later
```

Current files include:

```text
shared/seed/SeedDataStore.java
shared/seed/SeedDataLoader.java
shared/seed/SeedDataConfig.java
```

## What Domain Means

The `domain` package holds the business language and business rules.

Domain code should not care about:

```text
HTTP
JSON
controllers
databases
Spring annotations
```

Domain code answers business questions.

Examples:

```java
policy.canTransition(OrderStatus.OUT_FOR_DELIVERY, OrderStatus.DELIVERED)
```

This asks:

```text
Is this order status move allowed?
```

Another example:

```java
policy.canDriverUpdateOrder("DRV-2001", "ORD-1001", assignments)
```

This asks:

```text
Is this driver allowed to create a status event for this order?
```

That is domain logic.

## Task 04 - Status Transition Policy

Task 4 added the first real business rule.

Files:

```text
order/domain/OrderStatus.java
order/domain/StatusTransitionPolicy.java
order/domain/StatusTransitionPolicyTest.java
```

`OrderStatus` is an enum.

That means it defines the allowed status values:

```text
CREATED
CONFIRMED
PICKED_UP
IN_TRANSIT
OUT_FOR_DELIVERY
DELIVERY_ATTEMPTED
DELIVERED
CANCELLED
```

`StatusTransitionPolicy` answers:

```text
Can an order move from this current status to this next status?
```

Example:

```text
OUT_FOR_DELIVERY -> DELIVERED is allowed
DELIVERED -> OUT_FOR_DELIVERY is not allowed
```

Why this matters:

Later, when the API receives a request to create a status event, the service will call this policy before accepting the update.

The test proves the rule without needing HTTP or a database.

## Task 05 - Assignment Authorization Policy

Task 5 added the second business rule.

Files:

```text
assignment/domain/AssignmentStatus.java
assignment/domain/DeliveryAssignment.java
assignment/domain/AssignmentAuthorizationPolicy.java
assignment/domain/AssignmentAuthorizationPolicyTest.java
```

`DeliveryAssignment` connects:

```text
assignmentId
orderId
driverId
status
```

Example:

```text
ASN-3001 connects DRV-2001 to ORD-1001
```

`AssignmentAuthorizationPolicy` answers:

```text
Can this driver update this order?
```

It checks the assignments it is given.

The important statuses:

```text
ASSIGNED    authorizes the driver
ACCEPTED    authorizes the driver
COMPLETED   authorizes the driver for the delivered-order invalid-transition path
CANCELLED   does not authorize the driver
```

The completed assignment rule can feel strange at first.

Why `COMPLETED` can authorize:

```text
ORD-1003 is already DELIVERED.
DRV-2001 had completed assignment ASN-3003 for ORD-1003.
If DRV-2001 tries to move ORD-1003 back to OUT_FOR_DELIVERY, we want the failure to be:
409 INVALID_STATUS_TRANSITION
not:
403 ORDER_NOT_ASSIGNED_TO_DRIVER
```

So the assignment policy lets the request reach the status transition policy.

That is why task 5 and task 4 work together.

## Task 06 - Seed Store And Repositories

Task 6 turned the agreed fake data into Java objects.

This is where the project starts feeling more like an app.

Files:

```text
driver/domain/DeliveryDriver.java
driver/domain/DriverAvailabilityStatus.java
order/domain/ActorType.java
order/domain/DeliveryOrder.java
order/domain/OrderStatusEvent.java
shared/seed/SeedDataStore.java
shared/seed/SeedDataLoader.java
shared/seed/SeedDataConfig.java
order/repository/InMemoryOrderRepository.java
driver/repository/InMemoryDriverRepository.java
assignment/repository/InMemoryAssignmentRepository.java
order/repository/InMemoryStatusEventRepository.java
```

Tests:

```text
order/repository/InMemoryOrderRepositoryTest.java
driver/repository/InMemoryDriverRepositoryTest.java
assignment/repository/InMemoryAssignmentRepositoryTest.java
order/repository/InMemoryStatusEventRepositoryTest.java
```

## What Seed Means

Seed data is fake data that always exists when the app starts.

For this project, we are not using a database yet.

So instead of this:

```text
API -> service -> database
```

we are doing this:

```text
API -> service -> repository -> SeedDataStore
```

The seed data includes:

```text
orders
drivers
assignments
status events
```

The main seed class is:

```text
SeedDataLoader
```

Its job:

```text
Build the fake dataset.
Return a SeedDataStore.
```

## What SeedDataStore Does

`SeedDataStore` holds maps.

Conceptually:

```text
orders                  Map orderId -> DeliveryOrder
drivers                 Map driverId -> DeliveryDriver
assignments             Map assignmentId -> DeliveryAssignment
statusEventsByOrderId   Map orderId -> list of OrderStatusEvent
```

So when code asks for `ORD-1001`, the order repository can look it up by key.

Example:

```java
store.orders().get("ORD-1001")
```

That returns the seeded order object.

## What Repositories Mean

Repositories are classes that hide how data is stored.

Right now, data is stored in memory.

Later, if this became a database-backed app, the service code should not need to know all the storage details.

Instead of service code doing this:

```java
store.orders().get(orderId)
```

it will do this:

```java
orderRepository.findById(orderId)
```

That is cleaner because the repository owns the lookup logic.

## Current Repositories

### InMemoryOrderRepository

Purpose:

```text
Find and save orders.
```

Important methods:

```java
findById(String orderId)
save(DeliveryOrder order)
```

Returns:

```text
Optional<DeliveryOrder>
```

That means:

```text
Order found     -> Optional containing the order
Order missing   -> Optional.empty()
```

### InMemoryDriverRepository

Purpose:

```text
Find drivers.
```

Important method:

```java
findById(String driverId)
```

### InMemoryAssignmentRepository

Purpose:

```text
Find assignments by assignment ID, driver ID, or order ID.
```

Important methods:

```java
findById(String assignmentId)
findActiveByDriverId(String driverId)
findByOrderId(String orderId)
findAll()
```

Important rule:

```text
findActiveByDriverId("DRV-2001") returns only ASN-3001 and ASN-3002.
```

This is a big project-specific detail.

`ASN-3004` exists in seed data, but it is reserved for Slice 2.

So even though `ASN-3004` has status `ASSIGNED`, it must not appear as active Slice 1 driver work.

That is why the repository has:

```java
ACTIVE_SLICE_1_ASSIGNMENT_IDS = Set.of("ASN-3001", "ASN-3002")
```

### InMemoryStatusEventRepository

Purpose:

```text
Find and append timeline events.
```

Important methods:

```java
findByOrderId(String orderId)
append(OrderStatusEvent event)
```

The timeline is sorted chronologically before returning.

That means callers get events in time order.

## What Resources Means In Spring Boot

In Spring Boot, `src/main/resources` is for files loaded by the application, not Java classes.

Current important resource file:

```text
src/main/resources/application.properties
```

This is where app configuration goes.

Examples later might include:

```text
server port
logging
feature flags
```

But for Slice 1, we are keeping it simple.

Do not confuse:

```text
resources
```

with:

```text
repositories
```

They sound similar, but they are different.

```text
resources      configuration/static files
repositories   Java classes that access data
```

## How Tests Are Organized

The test tree mirrors the main code tree.

Main code:

```text
src/main/java/com/waypoint/partnersource/order/domain/StatusTransitionPolicy.java
```

Test code:

```text
src/test/java/com/waypoint/partnersource/order/domain/StatusTransitionPolicyTest.java
```

Main code:

```text
src/main/java/com/waypoint/partnersource/assignment/repository/InMemoryAssignmentRepository.java
```

Test code:

```text
src/test/java/com/waypoint/partnersource/assignment/repository/InMemoryAssignmentRepositoryTest.java
```

This makes it easy to find the matching test for a class.

## Why We Write Tests First

For tasks 4, 5, and 6, the tests define the expected behavior before implementation.

The flow is:

```text
write test
run test
test fails because code does not exist or behavior is wrong
write implementation
run test again
test passes
```

This is the red-green loop.

For example, task 6 started with tests that referenced:

```text
SeedDataLoader
InMemoryOrderRepository
InMemoryDriverRepository
InMemoryAssignmentRepository
InMemoryStatusEventRepository
```

Those classes did not exist yet, so the first failure was expected.

Then we created the production classes, and the tests passed.

## How Tasks 04, 05, And 06 Connect

Task 4 gives us:

```text
Can this status transition happen?
```

Task 5 gives us:

```text
Can this driver update this order?
```

Task 6 gives us:

```text
Where do we get orders, drivers, assignments, and events from?
```

Together they support the future status-event workflow:

```text
1. Find order by orderId.
2. Find driver by driverId.
3. Find assignments for that order/driver.
4. Check assignment authorization.
5. Check status transition.
6. Append status event.
7. Update order current status.
```

We have not built that full workflow yet.

But tasks 4 through 6 are preparing the pieces for it.

## Current Shape After Task 06

Current production structure:

```text
src/main/java/com/waypoint/partnersource/
  PartnerSourceApplication.java
  assignment/
    domain/
      AssignmentAuthorizationPolicy.java
      AssignmentStatus.java
      DeliveryAssignment.java
    repository/
      InMemoryAssignmentRepository.java
  driver/
    domain/
      DeliveryDriver.java
      DriverAvailabilityStatus.java
    repository/
      InMemoryDriverRepository.java
  order/
    domain/
      ActorType.java
      DeliveryOrder.java
      OrderStatus.java
      OrderStatusEvent.java
      StatusTransitionPolicy.java
    repository/
      InMemoryOrderRepository.java
      InMemoryStatusEventRepository.java
  shared/
    seed/
      SeedDataConfig.java
      SeedDataLoader.java
      SeedDataStore.java
```

Current test structure:

```text
src/test/java/com/waypoint/partnersource/
  PartnerSourceApplicationTests.java
  assignment/
    domain/
      AssignmentAuthorizationPolicyTest.java
    repository/
      InMemoryAssignmentRepositoryTest.java
  driver/
    repository/
      InMemoryDriverRepositoryTest.java
  order/
    domain/
      StatusTransitionPolicyTest.java
    repository/
      InMemoryOrderRepositoryTest.java
      InMemoryStatusEventRepositoryTest.java
```

## Common Confusions

### Domain vs Repository

Domain is about rules and business meaning.

Repository is about getting data.

Example:

```text
StatusTransitionPolicy   domain
InMemoryOrderRepository  repository
```

### Seed vs Repository

Seed is the actual fake data.

Repository is how code reads the fake data.

Example:

```text
SeedDataLoader creates ORD-1001.
InMemoryOrderRepository finds ORD-1001.
```

### Resources vs Repositories

Resources are files under:

```text
src/main/resources
```

Repositories are Java classes under:

```text
src/main/java/.../repository
```

### Test Package vs Main Package

Tests mirror the main package so each behavior has a nearby proof.

Example:

```text
main: src/main/java/.../order/domain/StatusTransitionPolicy.java
test: src/test/java/.../order/domain/StatusTransitionPolicyTest.java
```

## What Comes Next

After task 6, the project has data and rules.

Next tasks can start exposing behavior through Spring Boot:

```text
health endpoint
readiness endpoint
order status lookup
timeline lookup
driver profile
driver assignments
create status event
```

The future pattern will usually be:

```text
Controller receives HTTP request.
Service coordinates the workflow.
Repository fetches data.
Domain policy validates business rules.
DTO shapes the response.
```

That is the structure we are slowly building toward.

## Verification Commands

Focused task 6 tests:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-springboot
.\mvnw.cmd "-Dtest=InMemoryOrderRepositoryTest,InMemoryDriverRepositoryTest,InMemoryAssignmentRepositoryTest,InMemoryStatusEventRepositoryTest" test
```

Full Spring Boot tests:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-springboot
.\mvnw.cmd test
```
