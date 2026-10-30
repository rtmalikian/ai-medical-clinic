# open.epic MCP: Epic Documentation Lookup for This Project

This project documents an optional integration with Epic's **open.epic MCP
server** — a documentation/spec-lookup tool for developers building FHIR
integrations. It is **documentation only**: no patient data flows through it,
ever.

## What the server is — and is not

**It is:**

- A remote Model Context Protocol (MCP) server published by Epic under the
  open.epic programme.
- A way for an AI client (or a developer) to retrieve Epic's own integration
  documentation while building or reviewing a FHIR integration: API
  specifications, interface summaries, additional documentation such as
  data-sharing playbooks and tutorials, and FAQs — including Epic on FHIR
  content.

**It is not:**

- A patient-data or FHIR-resource server. It does not query `Patient`,
  `Observation`, `Encounter`, or any other FHIR resource.
- A SMART on FHIR / OAuth endpoint, and it requires no credentials.
- A replacement for this project's FHIR work. Patient data in a real
  deployment continues to flow **only** through a proper FHIR R4 client with
  SMART on FHIR authorisation — never through this MCP server.

Verified live on 2026-10-30: the server identifies itself as
**"open.epic MCP", version 4.0.9**.

## Server details

| Item | Value |
|---|---|
| URL | `https://mcp.open.epic.com` |
| Transport | Streamable HTTP |
| Protocol | MCP (JSON-RPC 2.0), `protocolVersion` `2025-03-26` accepted |
| Authentication | None documented |

### Content categories

- API specifications (Epic on FHIR APIs, with an R4 preference)
- Interface summaries
- Additional documentation: data-sharing playbooks, tutorials
- FAQs

### Live tools (discovered via MCP `tools/list`, 2026-10-30)

| Tool | Arguments | What it does |
|---|---|---|
| `search_documents` | `query` (string, ≤ 500 chars) | Keyword/phrase search across Epic documentation; returns documents with id, url, title, and snippet. |
| `get_document` | `document_id` (e.g. `api:x`, `tutorial:x`, `faq:x`, `interface:x:x`); optional `offset` (int) | Returns the full contents of one document; paginate with `offset` / `next_offset` in 20,000-character pages when a document is large. |

Typical flow: `search_documents` first, then `get_document` with a returned
document id for the full text.

## The no-PHI rule (read this before connecting anything)

Epic states that this server is **not designated to handle protected health
information (PHI) or confidential information**, and that the user is
responsible for anything they transmit to it. Use is subject to the open.epic
Terms of Use.

In substance, for this project that means:

- **Never** send patient identifiers, MRNs, SSNs, dates of birth, clinical
  notes, FHIR resource JSON for a real patient, or `Patient/<id>` references
  in a query.
- Only send documentation-style queries: API names, resource *type* names
  (e.g. `MedicationRequest`), and spec topics.
- When in doubt, do not send it. Look the topic up with generic terms instead.

## AI-client setup

An example client config is checked in at the repo root:
[`epic-mcp.mcp.json.example`](epic-mcp.mcp.json.example)

```json
{
  "mcpServers": {
    "open-epic-mcp": {
      "url": "https://mcp.open.epic.com",
      "transport": "streamable-http"
    }
  }
}
```

It is an example to copy, not a forced config. Which filename each client
reads:

| Client | Filename to copy it to |
|---|---|
| Claude Code | `.mcp.json` (project root) |
| VS Code | `.vscode/mcp.json` |
| Cursor | `.cursor/mcp.json` (project) or the global MCP config in Cursor settings |

## Env-style usage notes

This repo is docs/config only for this integration — no code in this project
calls the server today. If/when a client module is added, follow the shared
rollout convention so behaviour is consistent across projects:

```bash
EPIC_MCP_URL="https://mcp.open.epic.com"   # default; override only for testing
EPIC_MCP_ENABLED="true"                    # docs lookup is optional, never required
```

Rules that go with those settings:

- The app must work fully with the server disabled or unreachable — graceful
  degradation, with a short timeout (15s in the shared pattern).
- Any future `tools/call` path must screen query text for PHI-like content
  and refuse the call (logged, never silently sent) before anything leaves
  the machine.
- Nothing about this integration changes this project's existing demo /
  no-PHI safety boundary.

## How this project would use it

Alongside — never instead of — the FHIR work described in
`docs/ehr-fhir-implementation.md`:

- While implementing or reviewing a workflow module, look up the current Epic
  API specification for the FHIR resource types that module touches (for
  example `MedicationRequest` / `MedicationDispense` for refill and prior-auth
  work, `DocumentReference` for referrals and records requests, `Claim` /
  `Coverage` for eligibility and billing-denial work).
- Check interface summaries, playbooks, and FAQs when mapping a workflow's
  EHR touchpoints to what Epic actually exposes, before writing integration
  assumptions into a skill or module.
- Record which spec was consulted when an integration decision depends on
  Epic-specific behaviour, so the decision can be re-checked when the spec
  changes.

## Source

- Epic open.epic MCP documentation:
  https://fhir.epic.com/documentation?docid=mcp
