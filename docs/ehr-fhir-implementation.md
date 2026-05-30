# EHR/FHIR Implementation Plan

## Standards

- FHIR R4 / 4.0.1 baseline
- SMART App Launch OAuth2/OIDC with PKCE
- US Core profiles where available
- Bulk Data only for population/export workflows
- X12/clearinghouse integrations may still be required for real-time eligibility and revenue cycle workflows

## Vendor notes

- Epic: use open.epic and Epic on FHIR sandbox; production requires app/customer enablement.
- Oracle Health/Cerner: tenant-specific R4 endpoints; feature-detect write support from CapabilityStatement.
- athenahealth: many FHIR resources are read/search; scheduling and billing may require proprietary APIs.
- eClinicalWorks: public details are more gated; rely on SMART discovery and tenant metadata.
- NextGen: distinguish Enterprise, Office, Patient Access, and partner APIs.

## Integration ladder

1. Synthetic fixture mode.
2. Read-only FHIR sandbox.
3. SMART launch with least-privilege scopes.
4. Read-only production pilot.
5. Human-approved writeback.
6. Backend/Bulk jobs only after security review.

## Practical first workflows

Start with read-only or dry-run workflows:

- Pre-Visit Chart Prep
- Patient Message Drafting
- Referral Tracking
- Prior Authorization packet checklist

Avoid early autonomous writeback for scheduling, medication changes, orders, or clinical tasks.
