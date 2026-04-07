# Compliance Presets

The `full` tier writes a `.claude/rules/domain-compliance.md` file pre-populated with rules for one of these compliance domains. Selected via Q3 in `/init-workflow`.

## `none` (default)

No compliance rules. The file is created with just placeholders for the user to fill in if their domain has specific requirements.

## `govt` — Government / Public Sector

Triggered by: `Q3=2` (政府/公共部门)

Rules injected:

```markdown
## Government Compliance

**Why**: Public sector projects subject to government data laws, audit requirements,
and citizen privacy protection.

### Required Controls

1. **Audit log on every write operation**
   - All create/update/delete must log: who, when, what, before/after snapshot
   - No silent backend mutations

2. **Data isolation by org/department**
   - All list/detail endpoints must enforce permission filters
   - Multi-tenant by default

3. **Sensitive field encryption at rest**
   - ID numbers (citizen ID, passport, SSN equivalents)
   - Phone numbers, bank cards, addresses
   - Use field-level encryption annotations, not just disk encryption

4. **State machines for all workflows**
   - No direct status field writes
   - Approval workflows must use proper workflow engine, not status field flipping

5. **Approval workflows**
   - Any "approval" semantic must go through a workflow engine (BPMN / similar)
   - No "status: approved" without an approval record
```

## `fintech` — Financial / Payment

Triggered by: `Q3=3`

Rules injected:

```markdown
## Financial Compliance

**Why**: Payment, settlement, and financial data require regulatory compliance
(PCI-DSS, local payment regulations, anti-money-laundering rules).

### Required Controls

1. **Idempotency keys on all payment operations**
   - All charge/refund/transfer must accept and enforce idempotency key
   - Duplicate-detection window ≥24h

2. **Audit log with immutable storage**
   - Financial operations log to append-only store
   - Logs must include user, operation, amount, before/after balance

3. **Money values use Decimal (not float)**
   - No float arithmetic on monetary values, ever
   - Use BigDecimal / Decimal128 / similar

4. **PII encryption + tokenization**
   - Card numbers tokenized via PCI-compliant vault
   - Bank account numbers encrypted at rest

5. **Daily reconciliation**
   - Must have an automated reconciliation job comparing internal ledger
     vs payment provider ledger

6. **Two-person review on critical workflows**
   - Refunds above threshold require approval
   - Configuration changes to payment routing require dual approval
```

## `healthcare` — Healthcare / Medical

Triggered by: `Q3=4`

Rules injected:

```markdown
## Healthcare Compliance

**Why**: Medical data subject to HIPAA (US), GDPR Article 9 (EU), and equivalent
local regulations. Patient safety is paramount.

### Required Controls

1. **PHI (Protected Health Information) encryption**
   - All patient identifiers, diagnoses, treatments encrypted at rest
   - Encryption keys rotated quarterly

2. **Access logging**
   - Every read of patient data must log who accessed what when
   - Logs retained per regulatory minimum (typically 6+ years)

3. **Consent management**
   - Patient consent for data sharing must be tracked per recipient
   - No data export without recorded consent

4. **De-identification for analytics**
   - Analytics queries must operate on de-identified datasets
   - Re-identification requires explicit audit-logged action

5. **Break-glass emergency access**
   - Emergency override path for life-threatening scenarios
   - Triggers immediate audit alert + post-hoc review

6. **Backup retention + immutability**
   - Backups must be immutable for legal hold compliance
```

## `privacy` — Personal Information Protection

Triggered by: `Q3=5`

Rules injected:

```markdown
## Privacy Compliance (GDPR / CCPA / PIPL equivalent)

**Why**: Consumer-facing apps with personal data must comply with global
privacy regulations.

### Required Controls

1. **Data minimization**
   - Only collect fields you actively use
   - Periodic review to delete unused fields from schemas

2. **Right to access (subject access request)**
   - User-facing endpoint to export all their data in machine-readable format
   - Must complete within regulatory window (typically 30 days)

3. **Right to deletion (right to be forgotten)**
   - User-facing endpoint to delete account + all associated data
   - Cascading deletes verified across all data stores

4. **Consent records**
   - Every consent (marketing, cookies, data sharing) tracked with timestamp
   - Withdrawals must be respected immediately, not at next batch run

5. **Cross-border data transfer**
   - Track where data is stored and processed
   - Document legal basis for international transfers

6. **Data Processing Agreements (DPA) with vendors**
   - All third-party processors must sign DPA
   - Maintain vendor inventory in repo
```

## How to Add a New Preset

1. Add a new branch in `scripts/init.sh` to handle the new compliance value
2. Add the rule block to this file
3. Update `templates/full/rules/domain-compliance.md.template` to reference the injection point
4. Document the new preset value in `init-workflow` Q3 options
