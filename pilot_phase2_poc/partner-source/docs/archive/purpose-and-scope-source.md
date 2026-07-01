# Partner Source Purpose And Scope

## Purpose

`partner-source` provides partner logistics data through a simple API that Waypoint can plug into.

It is a data-source module, not a BFF and not a gateway.

## In Scope

- delivery orders
- current order status
- order timelines
- delivery drivers
- driver assignments
- driver status updates
- status transition validation
- demo seed data

## Out Of Scope

- chatbot wording
- RAG answers
- production identity provider
- real partner API adapters
- live GPS tracking
- route optimization

## Rule

`partner-source` returns operational truth. The BFF turns that truth into client-specific responses.
