# Version Log — version-06-contact-email-update

| Field | Value |
|---|---|
| Version | 6 — Contact email changed from info@example.org to wexmoorinfo@example.org |
| Branch | `version-06-contact-email-update` |
| Baseline commit | `d95b431000d797172bb3484f7d67fddec5ce4ca8` (original website, `main`) |
| Date | 2026-10-20 |
| Live URL (when deployed) | https://hufsa-stack.github.io/wexmoor-foundation-demo/ |

Changes from the baseline:

* `src/data/site.json`: `"email": "info@example.org"` → `"wexmoorinfo@example.org"` — the single source for the contact address.
* Contact Us page: the visible address and its `mailto:` link now use wexmoorinfo@example.org (rendered from site.json).
* 9 PDFs regenerated so their letterhead/footer contact line (and the Financial Summary's "questions … may be directed to"
  line) show the new address: Outcomes Sought, Indirect Cost Policy, Program Officer job profile, FY2025 Financial Summary,
  and the FY2022–FY2026 annual reports. Their pages and words are otherwise identical to the baseline.

Unchanged: grants@example.org and careers@example.org (different addresses), the 3 Impact Plan PDFs (no contact email),
phone number and street address, and every other page, document and asset.
This file is repository documentation only; it is not part of the built website.
