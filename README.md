# AI Medical Clinic: Agentic Medical Office Workflow Automation with EHR/FHIR and OpenAI-Compatible API Integration

**AI Medical Clinic** is a modular, human-in-the-loop healthcare administration automation starter for medical offices, clinics, and healthcare AI builders. It turns the atomic workflow skill library from [`medical-clinic-ai-workflow-skills`](https://github.com/rtmalikian/medical-clinic-ai-workflow-skills) into working API submodules for patient intake, appointment scheduling, eligibility checks, prior authorization, referral tracking, chart prep, patient messaging, lab follow-up, refill routing, recall outreach, records requests, and billing denial support.

> SEO keywords: medical office AI automation, AI clinic workflow software, healthcare AI agents, EHR integration, FHIR integration, SMART on FHIR, OpenAI compatible healthcare AI, prior authorization automation, patient intake automation, referral tracking automation, medical office workflow automation.

## What this repo includes

- **12 workflow submodules** mapped from atomic medical office skills.
- **FastAPI backend** with interactive Swagger docs at `/docs`.
- **OpenAI-compatible AI integration** using `OPENAI_BASE_URL`, `OPENAI_API_KEY`, and `OPENAI_MODEL`.
- **Local OpenAI-compatible `/v1/chat/completions` endpoint** for demo agents and workflow-router integrations.
- **Deterministic rules-first engine** before any LLM drafting.
- **Human approval queue** for every generated workflow artifact.
- **Append-only audit event model** with artifact hashing.
- **FHIR utilities** for Bundle normalization and CapabilityStatement discovery.
- **No-PHI demo mode** with safe fallback drafting when no AI key is configured.
- **Pytest coverage** for workflows, FHIR utilities, and AI fallback behavior.

## Safety boundary

This is a **demo/starter** for administrative workflow automation. It is not medical advice, clinical decision support, diagnosis, treatment, emergency triage, autonomous patient messaging, or a production HIPAA-compliant system. Do not enter real PHI into a public or unapproved environment.

Every workflow follows this rule:

> Rules first → AI drafts second → human approves final action.

## Workflow modules

| Module | Problem solved | FHIR/EHR touchpoints |
|---|---|---|
| Patient Intake Triage | Converts messy calls/forms into structured tasks | Patient, Appointment, QuestionnaireResponse, Communication, Task |
| Appointment Scheduling | Suggests next scheduling step and required checks | Appointment, Schedule, Slot, Location, Practitioner |
| Insurance Eligibility | Creates verification checklist and missing-info tasks | Coverage, Patient, Account, ClaimResponse |
| Referral Tracking | Tracks missing docs, stale referrals, follow-ups | ServiceRequest, DocumentReference, Task |
| Prior Authorization | Builds auth packet checklist and status tracker | MedicationRequest, ServiceRequest, Coverage, DocumentReference |
| Pre-Visit Chart Prep | Summarizes chart context and open loops | Patient, Encounter, Observation, Condition |
| Patient Message Drafting | Classifies admin vs clinical escalation messages | Communication, CommunicationRequest, Task |
| Lab & Imaging Follow-Up | Routes pending/missing/normal/abnormal result work | Observation, DiagnosticReport, ServiceRequest |
| Medication Refill Routing | Applies refill checklist and routes exceptions | MedicationRequest, Observation, Encounter |
| No-Show & Recall Follow-Up | Builds recall/outreach queues | Appointment, Communication, CarePlan |
| Medical Records Requests | Creates ROI checklist and deadline tracker | DocumentReference, Consent, Provenance |
| Billing Denial Support | Summarizes denials and drafts appeal checklist | Claim, ClaimResponse, EOB, DocumentReference |

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn app.main:app --reload
```

Then open:

- API docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health
- Workflow list: http://127.0.0.1:8000/api/workflows

Run tests:

```bash
pytest -q
```

## OpenAI-compatible integration

The app can call any provider exposing an OpenAI-compatible `/chat/completions` endpoint.

```bash
cp .env.example .env
export OPENAI_BASE_URL="https://api.openai.com/v1"
export OPENAI_API_KEY="your-key-here"
export OPENAI_MODEL="gpt-4o-mini"
```

Compatible patterns include OpenAI, LiteLLM gateways, vLLM OpenAI-compatible servers, local model servers, OpenRouter-style gateways, and enterprise AI gateways.

If no API key is configured, the app uses a deterministic safe fallback so demos still work without paid AI calls.

## Main API endpoints

```text
GET  /api/workflows
GET  /api/workflows/{workflow_id}
POST /api/workflows/{workflow_id}/run
POST /api/ai/draft
GET  /api/review-tasks
POST /api/review-tasks/{task_id}/approve
POST /api/review-tasks/{task_id}/reject
GET  /api/audit-events
POST /api/fhir/normalize-bundle
GET  /api/fhir/capability?base_url=https://hapi.fhir.org/baseR4
POST /v1/chat/completions        # local OpenAI-compatible demo response shape
```

Example workflow run:

```bash
curl -X POST http://127.0.0.1:8000/api/workflows/patient-intake-triage/run   -H 'Content-Type: application/json'   -d '{
    "source": "portal",
    "patient_ref": "Patient/example",
    "request_text": "I need a routine follow-up appointment next week.",
    "use_ai": false
  }'
```

## EHR/FHIR implementation strategy

Research-backed integration ladder:

1. Synthetic/no-PHI fixtures.
2. Read-only FHIR sandbox using SMART Health IT, HAPI FHIR, Epic, Oracle Health/Cerner, or athenahealth sandboxes.
3. SMART on FHIR OAuth2/OIDC launch with PKCE and least-privilege scopes.
4. Read-only production pilot after customer approval and security review.
5. Human-approved writeback only after audit logging, idempotency, rollback planning, and EHR vendor approval.

See `docs/ehr-fhir-implementation.md`.

## open.epic MCP documentation lookup

This project also documents an optional integration with Epic's
**open.epic MCP server** (`https://mcp.open.epic.com`, Streamable HTTP) for
looking up Epic API specifications and integration guidance while building
the FHIR work above. It is **documentation only — not patient data**: Epic
states the server is not designated for PHI, and patient data never flows
through it. See [`EPIC_MCP.md`](EPIC_MCP.md) for what the server is/isn't,
its live tools (`search_documents`, `get_document`), the no-PHI rule, and
AI-client setup, and [`epic-mcp.mcp.json.example`](epic-mcp.mcp.json.example)
for an example MCP client config.

## Research sources used

- HL7 FHIR R4: https://hl7.org/fhir/R4/
- SMART App Launch: https://hl7.org/fhir/smart-app-launch/
- SMART Backend Services: https://hl7.org/fhir/smart-app-launch/backend-services.html
- US Core: https://hl7.org/fhir/us/core/
- Bulk Data: https://hl7.org/fhir/uv/bulkdata/
- SMART Health IT Launcher: https://launch.smarthealthit.org/
- Epic on FHIR: https://fhir.epic.com/
- Oracle Health/Cerner FHIR: https://fhir.cerner.com/millennium/r4/
- athenahealth FHIR: https://docs.athenahealth.com/api/guides/fhir
- LiteLLM OpenAI-compatible providers: https://docs.litellm.ai/docs/providers/openai_compatible
- vLLM OpenAI-compatible server: https://docs.vllm.ai/en/latest/serving/openai_compatible_server/
- FastAPI: https://fastapi.tiangolo.com/
- Pydantic: https://docs.pydantic.dev/
- OWASP LLM Top 10: https://owasp.org/www-project-top-10-for-large-language-model-applications/

## License

Commercial Evaluation License. See `LICENSE`.

## Contact

Raphael T. Malikian, MBBS, BSc  
Email: rtmalikian@gmail.com  
LinkedIn: http://www.linkedin.com/in/raphael-t-malikian-mbbs-bsc-hons-71075436a  
GitHub: https://github.com/rtmalikian
