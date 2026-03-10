# UK Property Management & Block Management Software

## Project Overview

Internal tooling for UK residential property management and block management companies. The focus is on practical, lightweight tools that reduce manual admin for property managers, RMCs (Resident Management Companies), and leaseholders.

---

## Core Modules

- **Tenant Repair Portal** — leaseholders and tenants submit maintenance requests; contractors receive and update jobs
- **Service Charge Calculator** — apportion costs across units by floor area, equal share, or lease-defined ratios
- **Contractor Job Tracker** — raise works orders, track status, store quotes and completion certificates
- **Lease Extension Calculator** — calculate premium estimates using the Deverell Smith / tribunal methodology (marriage value, ground rent capitalisation, reversion)
- **Document Automation** — generate Section 20 notices, service charge demands, AGM packs, and lease summaries from templates

---

## Tech Stack Preferences

- **Backend:** Python (FastAPI or Django) or Node.js (Express/Fastify)
- **Frontend:** Plain HTML + HTMX for simple internal tools, or React where interactivity demands it
- **Database:** PostgreSQL — use proper relational schemas; avoid document stores for structured property data
- **PDF generation:** WeasyPrint (Python) or Puppeteer (Node) for statutory notices and demands
- **Auth:** Simple session-based auth or JWT; no OAuth complexity unless required
- **Hosting:** Single VPS or Railway/Render for MVP; containerise with Docker

---

## Coding Rules

### General

- Keep it simple. Internal tools do not need microservices, event queues, or GraphQL.
- Prefer explicit over clever. Property managers are the end users, not developers.
- All monetary values stored as integers (pence/minor currency unit). Never use floats for money.
- Dates stored as ISO 8601 strings (`YYYY-MM-DD`) or proper `DATE` columns in Postgres.
- All calculations must be auditable — store inputs alongside outputs so results can be reproduced.

### UK-Specific Rules

- Ground rent, service charges, and lease premiums must follow current UK leasehold law:
  - Leasehold Reform (Ground Rent) Act 2022 — zero ground rent for new leases
  - Landlord and Tenant Act 1985 — Section 20 consultation thresholds (currently £250 per unit or £100 per unit per year for qualifying works)
  - RICS guidance for service charge accounting
- VAT handling: clearly distinguish VATable and exempt service charge items. Default VAT rate is 20%.
- Companies House numbers and UTRs should be validated to UK formats before storage.
- Postcodes must be validated against the standard UK postcode regex and normalised to uppercase with a space before the inward code.

### Database

- Every table must have `created_at` and `updated_at` timestamps.
- Use UUIDs as primary keys for externally referenced records (leases, units, jobs).
- Use integer surrogate keys for internal lookup tables (cost categories, job statuses, etc.).
- Never delete records — use `deleted_at` (soft delete) or an `is_archived` flag.
- Service charge periods are always explicit `period_start` and `period_end` date columns, never implied by year.

### API Design

- REST endpoints named after resources: `/api/units/`, `/api/jobs/`, `/api/demands/`
- Return standardised error shapes: `{ "error": "message", "code": "SNAKE_CASE_CODE" }`
- Paginate all list endpoints using `limit` / `offset` query params with a default limit of 50.
- Never expose internal database IDs in URLs for leaseholder-facing routes — use UUIDs.

### Frontend

- Forms must show inline validation errors, not just alert boxes.
- All currency inputs display as pounds (£) with two decimal places; store as pence on submit.
- Date pickers must default to UK date format (DD/MM/YYYY) in the UI.
- Repair portal submissions must confirm receipt with a reference number and estimated response time.
- Tables showing service charge apportionments must show the calculation method used per row.

### Document Automation

- Templates stored as separate `.html` or `.docx` files — never hardcoded strings in business logic.
- Section 20 notices must include: description of works, estimated cost, observation period end date, and RMC contact details.
- Service charge demands must comply with LTA 1985 s.21B — include landlord's name and address, summary of rights, and a valid administration charge schedule.
- All generated PDFs must be stored against the relevant record with a generation timestamp.

---

## File & Folder Structure

```
/app
  /core          # Shared models, utilities, constants
  /units         # Unit and building records
  /leases        # Lease data, leaseholder records
  /repairs       # Repair portal, job tracking
  /service_charge # Budget, apportionment, demands
  /lease_extension # Calculator and premium estimates
  /documents     # Template rendering, PDF generation
  /api           # Route handlers / views
/templates       # HTML or document templates
/tests
/migrations
```

---

## Calculations Reference

### Service Charge Apportionment

```
unit_share = unit_floor_area / total_floor_area   # or as defined in lease
unit_charge = total_expenditure * unit_share
```

Always round to 2 decimal places. The sum of all unit charges must reconcile to total expenditure — handle penny rounding on the largest unit.

### Lease Extension Premium (simplified statutory basis)

```
premium = term_reversion + ground_rent_capitalisation + marriage_value_share
```

- Use an appropriate deferment rate (currently 5% for houses, 5.5% for flats per Sportelli)
- Marriage value applies only where unexpired term < 80 years
- Relativity tables: use Gerald Eve or Savills relativity graphs, store the table in the DB for auditability

### Section 20 Thresholds

```
qualifying_works_threshold = 250 * number_of_units   # £250 per unit
qualifying_long_term_threshold = 100 * number_of_units  # £100 per unit per year
```

Flag any single works order that will exceed these thresholds and require consultation.

---

## Testing

- Write tests for all financial calculations — edge cases include zero ground rent, very short unexpired terms (<5 years), and single-unit buildings.
- Integration tests must cover the full demand generation flow: budget → apportionment → demand letter → PDF.
- Repair portal: test submission, status transitions (Submitted → Acknowledged → In Progress → Completed → Closed), and contractor notification.
- Do not mock the database in unit tests for calculation modules — use a real test Postgres instance with fixtures.

---

## Out of Scope (for now)

- Online rent collection or payment processing
- Full accounting / double-entry bookkeeping
- External integrations (Xero, Sage, Fixflo) unless specifically requested
- Mobile apps
- Multi-tenancy SaaS features
