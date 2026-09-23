# Architecture Notes

## Boundary design

External channels feed one normalized intake contract. This keeps Telegram, website chat, CRM, or another provider from leaking channel-specific logic through the whole system.

## Reliability

- Validate at ingress
- Create idempotency keys before external writes
- Retry transient failures with bounded exponential backoff
- Send permanent failures to a review queue
- Expose a health endpoint
- Keep secrets in environment variables, never source control

## Production extension points

A client deployment can add:
- CRM adapters
- Google Sheets logging
- email notifications
- LLM classification
- human approval gates
- scheduled follow-ups
- metrics and alerting
