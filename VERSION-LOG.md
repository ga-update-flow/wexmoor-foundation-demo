# Version Log — preview-loi-budget-only

| Field | Value |
|---|---|
| Branch | `preview-loi-budget-only` |
| Baseline | `main` at `d95b431000d797172bb3484f7d67fddec5ce4ca8` (verified original website) |
| Single update | Letter of Inquiry (Step 2) requires a proposed project budget outlining the anticipated costs |
| Excludes | International eligibility change; Extracurricular Activities focus area |
| Date | 2026-10-20 |
| Live URL (when deployed) | https://hufsa-stack.github.io/wexmoor-foundation-demo/ |

Changes from the baseline (all in support of the one update):

* Grant Application Process, Step 2 LOI requirements (also shown on `/faq/step-2-submit-a-letter-of-inquiry/` and in the
  archive excerpt): adds "A proposed project budget outlining the anticipated costs" after the unchanged mission-alignment item.
* Letter of Inquiry form (`/portal/letter-of-inquiry/`): adds a required field "Proposed project budget outlining the
  anticipated costs" so the form asks for what Step 2 says the LOI requires. No template, format or amount is specified.
* `scripts/browser-test.mjs` (tooling only): fills the new field when present so the LOI demo-submit test still runs.

Geographic eligibility (international programs remain ineligible) and the two original focus areas are unchanged.
This file is repository documentation only; it is not part of the built website.
