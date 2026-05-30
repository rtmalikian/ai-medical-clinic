# Safety and Compliance Notes

This is not legal advice or a HIPAA compliance certification.

## Demo rules

- Do not enter PHI.
- Use synthetic patients and synthetic workflows.
- Keep EHR writeback disabled.
- Require human review for every output.
- Treat all AI output as a draft.

## Production prerequisites

- BAA and security review where PHI is involved.
- Tenant-specific EHR approval.
- Access controls and user identity.
- Audit logging and retention policy.
- PHI-safe logging and observability.
- Incident response and deletion/export process.
- Clinical governance for any clinical-risk routing.
