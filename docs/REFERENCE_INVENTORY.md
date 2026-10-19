# Reference Inventory — belkfoundation.org (inspected 2026-10-19)

This inventory records the layout and information architecture of the reference site, captured
before any code was written. The fictional Wexmoor Foundation site is built from it. No reference
text, images, logos or documents are reused. Only structure, component types and the
*presence/absence pattern* of information are mirrored.

## 1. Global chrome

| Element | Reference | Fictional equivalent |
|---|---|---|
| Announcement bar | Full-width teal strip above header: "…excited to share our FY 2026 Annual Report! *Click here to learn more.*" with × close | Same strip, Wexmoor colors, links to `/annual-reports/`, dismissible |
| Header | Logo (icon + 2-line wordmark + italic serif tagline) left; small boxed search input right | Same; original "W" facet logo, tagline *Read. Teach. Lead.*; working site search |
| Main nav | 4 uppercase items separated by thin vertical rules; 3 have hover dropdowns | Same order and dropdown structure |
| Mobile | Hamburger toggles a stacked menu including sub-items | Same |
| Page branding | Full-bleed ~250px photo band, page H1 overlaid bottom-left in white | Same, original illustrated banners |
| Content | ~980px centered column | Same |
| Footer | Full-width faceted-polygon (green/teal) background; inline nav (About, What We Fund, Become Our Partner, Contact Us) + X and LinkedIn circle icons | Same polygon treatment in original palette; same 4 links. Social icons **omitted** (fictional org has no social accounts; dead links would violate "meaningful destination") |
| Disclaimer | — | Discreet one-line footer note: independent demonstration site |

### Navigation (labels, order, dropdowns)
1. **About the Foundation** → From the Board Chair · Our History · Our Approach · Our People · Financials · Annual Reports · Careers
2. **What We Fund** → Mission & Guidelines · K-3 Achievement · Teaching & Leadership · Our Partners
3. **Become Our Partner** → Grant Application Process · FAQs
4. **Contact Us** (no dropdown)

Fictional: About the Foundation (same 7 children) · What We Fund → Mission & Guidelines · Early Grades Achievement · Educators & Leaders · Our Grantees · Become Our Partner → Grant Application Process · FAQs · Contact Us.

## 2. Pages, section order and components

### Home `/`
1. Announcement bar. 2. Header. 3. Full-viewport hero image with blue overlay: centered white logo icon → 3-line bold headline whose final phrase is in accent green → one rectangular teal button **"LEARN MORE >"** → `/about-the-foundation/`. 4. Footer.
5. Auto-opening modal popup: "Our FY 2026 Annual Report is now available!" + button **"VIEW IT HERE"** (→ annual reports) + close ×.
*No* funding-priority cards, stats, news feed or "Apply" CTA on the homepage. The fictional homepage does not add them either.

### About the Foundation `/about-the-foundation/`
H3 "EMPOWERING STUDENTS. CHANGING OUTCOMES." + 2 paragraphs (links to both focus areas) → H3 DEI commitment + "here" link to DEI page → **two-column block**: left = vertical uppercase green sub-menu (From the Board Chair, Our History, Our Approach, Our People, Financials, In the News, 2025 Annual Report); right = large italic serif pull statement ("…invests around $2 million annually…").

### From the Board Chair
Left-floated portrait + 4-paragraph letter + signature H4 + embedded YouTube video. Fictional: portrait illustration + letter + signature. **Video omitted** (no real video can be embedded for a fictional org).

### Our History
H3 "A LEGACY OF GIVING" → paragraphs (founding 1928, memorial fund, 1952 foundation formed) → blockquote from long-time executive → paragraphs (relationship to company; 2010 new mission).

### Our Approach
H3 DEI commitment + link → intro paragraph → H3 "BELIEFS TO ACTION…" → 4 belief blocks, each = CAPS title + dash bullets, then "How we work to achieve this:" + ✓ bullets.

### Our People
Board group photo + caption → H3 BOARD OF DIRECTORS (names with officer titles) → hr → H3 RISING GENERATION (intro + names) → hr → H3 COMMUNITY MEMBERS SERVING ON COMMITTEES → hr → H3 FOUNDATION STAFF (portrait grid: photo, name, title).

### Financials
Fiscal year statement; Form 990-PF filing note; "Fiscal Year 2024 (dates)"; total assets; grants distributed; link "Download FY2024 990PF" (PDF).
Fictional: same fields, a PDF financial summary (explicitly fictional, not an IRS form replica).

### Annual Reports `/annual-reports/`
Intro paragraph → H3 "2026 ANNUAL REPORT" → italic "Posted September 16, 2026" → embedded flipbook iframe → text link "Click here to download the pdf version…" → widget "View Previous Annual Reports" with list 2025, 2024, 2023, 2022 (each its own post page: title, posted date, embed, PDF link, prev/next).
Fictional: same; embed is the PDF itself in an iframe; 5 genuine PDFs.

### Careers
H2 "Join our Team!" → H3 JOB OPENINGS → role summary paragraph → "click HERE" → job description PDF → thanks line → H3 "Resumes must be submitted per instructions…".

### DEI page (`/tbf-dei/`) and In the News (`/category/in-the-news/`)
DEI: 2 paragraphs. In the News: intro + post list (thumbnail, H3 title, excerpt, "Read More" button), paginated.

### What We Fund `/what-we-fund/`
Intro paragraphs (bold focus-area names) → two-column block: left = green vertical sub-menu (Mission & Guidelines, K-3 Achievement, Teaching & Leadership, Our Partners); right = large italic serif statistic statement.

### Mission & Guidelines `/what-we-fund/mission-guidelines/`
Grey-blue **shaded box**: H3 MISSION STATEMENT + paragraph → H3 BUILDING BLOCKS FOR SUCCESS → hr → H3 OUTCOMES SOUGHT (inline link to **Outcomes Sought PDF**) → hr → H3 GEOGRAPHIC FOCUS (2 paras: local county + select statewide; historical geographies) → hr → H3 GRANT LIMITATIONS: "not awarded to" bullet list (individuals; private K-12 schools; international; fundraising/events/giveaways) + indirect-cost policy sentence with "here" link → **Indirect Cost Policy PDF** (15% for higher-ed).
*Absent:* award amounts, deadlines, project periods, application form.

### K-3 Achievement
Centered italic blockquote with linked attribution → intro paragraph → H3 OUTCOMES SOUGHT (link to PDF) → hr → centered H1 "STRATEGIC ISSUE: THIRD GRADE READING" → centered photo with credit → 2 paragraphs (local goal with % targets and partner initiative; state-level focus) → hr → H3 STRATEGIES (5 bullets) → **two outlined buttons side by side**: "EXPLORE THE STRATEGIC ISSUE" (1-page landscape PDF) and "EXPLORE THE FULL STRATEGY AND IMPACT PLAN" (18-page landscape PDF) → hr → H3 WHAT'S NEW → hr → H3 DATA THAT SHAPES OUR APPROACH (5 data bullets).

### Teaching & Leadership
Blockquote → intro → 3 goal bullets (recruit / develop / retain) → H3 OUTCOMES SOUGHT → hr → centered H1 "STRATEGIC ISSUE: EQUITABLE ACCESS TO EFFECTIVE TEACHERS" + video embed → 2 paragraphs → hr → H3 STRATEGIES + intro → **two side-by-side image cards**: "EXPAND THE POOL" and "EXTEND THE REACH" (image + lead-in + bullets) → two buttons "EXPLORE THE LOGIC MODEL" (1-page PDF) / "EXPLORE THE FULL STRATEGY AND IMPACT PLAN" → hr → H3 ADDITIONAL INFORMATION → hr → H3 DATA THAT INSPIRES OUR APPROACH (2 sub-groups of bullets) + chart image.
Fictional: video replaced by an illustration (no fabricated video).

### Our Partners
H3 PARTNERS IN A SHARED VISION → intro + 2 focus-area bullets → list of grant-cycle pages (Spring 2026 … Fall 2023) → paragraph → infographic image.
Each cycle page: header image → **table** of grantees: name (H3, linked to org site) + location ("Charlotte, NC" / "State Level - NC") → link to previous cycle. *Absent:* award amounts, grant purposes, durations.
Fictional: same table; org names unlinked (fictional orgs have no websites).

### Become Our Partner `/become-our-partner/`
2 intro paragraphs (two cycles/year, spring & fall, **invitation-only final applications**) → shaded box with belief statement → two columns: grey box H3 "GRANT CYCLE KEY DATES" (6 lines, bold month + event, **months only, no days**) | photo.
*Absent:* Apply Now button, portal button, amounts.

### Grant Application Process `/become-our-partner/grant-application-process/`
Two columns: photo left | **accordion** right (dark-blue headers, +/− toggles, first open):
1. "Step 1: Determine your fit and take Eligibility Quiz": eligible = 501(c)(3), public school systems, higher-ed; focus areas + geography; read list (Our approach, Our guidelines, Outcomes sought [PDF], Past grantees); inline link "Eligibility Quiz" → **external applicant portal** (YourCause sign-in page).
2. "Step 2: Submit a Letter of Inquiry": LOI form via quiz; 4 requested items (contact info, Tax ID, brief description of alignment, geographic area served); response "within a few weeks"; initial interest ≠ invitation. **No LOI deadline.**
3. "Step 3: Submit a Grant Application (by invitation only)": staff contacts invitees; results/evidence; reference Outcomes Sought; two cycles, applications issued February / August.
4. "Step 4: Proposal Review & Funding Determination": Grants Committee → Board; Board meets May and Nov/Dec; staff notifies.
Each step also exists as an individual FAQ post (`/faq/step-…/`) and in the category archive `/faq_categories/grant-application-process/` (excerpt + "Read More" button).

### FAQs `/become-our-partner/faqs/`
Two columns: photo | accordion of 11 questions (scholarships/individuals; outside US; deadlines [spring due March, fall due Sept, invitation only]; how to get an application; non-nonprofits; fiscal sponsors; relationship to sister endowment; relationship to company; sponsor events; raffle items; indirect cost limit + PDF link).

### Contact Us
Header image → H1 → paragraph linking to Become Our Partner → hr → H5 org name, address, "Get Directions", phone, email → hr → newsletter signup form (Mailchimp).
Fictional: reserved `example.org` email, 555 phone; "Get Directions" omitted (fictional address); newsletter form is a demo that states nothing was sent.

### External applicant portal
Separate-looking "Applicant Portal" page: email sign-in, Remember me, Create account, Sign in.
Fictional: `/portal/` demo portal → eligibility quiz → LOI form; clearly a demonstration, no data stored or sent.

## 3. Linked documents (all PDFs)

| Reference document | Where linked | Fictional equivalent |
|---|---|---|
| Outcomes Sought (4 pp, portrait) | Mission & Guidelines, both focus pages, App Process Steps 1–3 | *Outcomes Sought by The Wexmoor Foundation* (4 pp) |
| Indirect Cost Policy (1 p letterhead) | Mission & Guidelines, FAQ | *Indirect Cost Policy* (1 p, 12%) |
| Strategic Issue one-pager (landscape) | K-3 button | *Early Reading Proficiency – Strategic Issue* (1 p) |
| Logic Model (landscape table) | Teaching button | *Strong Teachers Strategic Issue Logic Model* (1 p) |
| Impact Plan (18 pp landscape) | both focus pages | *Wexmoor Foundation Impact Plan* (~12 pp) |
| Annual Reports 2022–2026 | Annual Reports + year pages | 5 fictional annual reports |
| 990-PF FY2024 | Financials | Fictional FY2025 financial summary (not an IRS form replica) |
| Program Officer job description | Careers | Program Associate job description |

## 4. Information presence / absence (governs fictional content)

Present: two focus areas; mission; geography (home county + select statewide); exclusions list;
indirect-cost cap (higher-ed only); eligible applicant types; LOI contents; invitation-only full
application; two cycles with month-level key dates; board meeting months; ~annual grantmaking
total; fiscal year, total assets, grants distributed; strategic-issue % goals (in page text & PDFs);
grantee lists by cycle with location.

Absent (must NOT be invented): per-grant award amounts or ranges; specific day-level deadlines;
LOI deadline; project/grant period; required attachment list for full application; reporting
requirements; public full-application form; "Apply Now" button; numeric targets in Outcomes Sought.
