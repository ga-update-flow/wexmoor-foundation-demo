# The Wexmoor Foundation: Demonstration Website

An independent demonstration website for a **fictional** education foundation, built to test a
grant-opportunity crawler against realistic funder-site structure. Its page hierarchy, navigation,
component types, document formats and the *presence and absence* of grant information mirror the
layout of a real family foundation's site (inspected October 2026; see
[`docs/REFERENCE_INVENTORY.md`](docs/REFERENCE_INVENTORY.md)). All names, people, grantees, figures and
documents are invented. No reference text, images, logos or documents were reused.

## Quick start

```bash
npm install
npm run dev            # http://localhost:4321
npm run build          # static site -> dist/ (pages + PDFs + sitemap.xml, robots.txt, _headers)
npm run preview        # serve dist/
npm run check-links    # every internal href/src in dist/ must resolve
npm test               # build + link check + headless Chromium end-to-end tests
```

Set the deployed origin when building for production so canonical URLs, `sitemap.xml` and
`robots.txt` are correct:

```bash
SITE_URL=https://your-site.netlify.app npm run build
```

Regenerating artwork or PDFs (Python 3 with `reportlab` and `Pillow`):

```bash
npm run images   # scripts/make_images.py -> public/images/*.svg, favicons
npm run pdfs     # scripts/make_pdfs.py   -> public/uploads/**.pdf
```

Generated images and PDFs are committed, so a normal `npm run build` needs only Node.

## Project layout

```
src/data/            Single source of truth (JSON), shared by pages and the PDF generator
  site.json          identity, contact info, financial figures, annual giving
  documents.json     every downloadable document: title + URL path
  steps.json         4-step grant application process (accordion + /faq/ posts)
  faqs.json          FAQ accordion questions/answers
  grantees.json      grant cycles and grantee lists (Our Grantees tables, annual reports)
  reports.json       annual reports (posted dates, totals, highlights)
  people.json        board, rising generation, committees, staff
  news.json          "In the News" posts
src/layouts/Base.astro       <head> (noindex meta), header, footer
src/components/              Header, Footer, PageBranding band, Page template, Accordion,
                             SubMenuStatement (side menu + italic statement), PortalShell
src/pages/                   one file per route (URLs mirror the reference hierarchy)
src/styles/global.css        all styles (design tokens in :root)
public/js/site.js            dropdowns, mobile menu, accordion, popup, search, demo forms
docs-src/*.md                editable sources for the prose PDFs
scripts/                     make_images.py, make_pdfs.py, postbuild.mjs, check-links.mjs, browser-test.mjs
docs/                        reference inventory and testing report
```

## Updating content

* **Program details, dates, contacts:** edit the JSON in `src/data/`, then `npm run build`.
  HTML strings in `steps.json`/`faqs.json` may use `{{outcomes}}`, `{{indirect}}` and similar tokens, which
  resolve to the paths in `documents.json`.
* **Grant cycles:** add an entry to `grantees.json` and a cycle page appears at
  `/what-we-fund/our-grantees/<slug>/`, listed automatically on Our Grantees.
* **A new annual report:** add an entry at the top of `reports.json` (the first entry is "current"),
  run `npm run pdfs`, and update `currentReportYear` in `site.json` (announcement bar, popup).
* **Prose documents (Outcomes Sought, Impact Plan, policies, job profile):** edit `docs-src/*.md`
  and run `npm run pdfs`. The two one-page PDFs are extracted from sections of `impact-plan.md`.
* **Renaming a PDF:** change its `path` in `documents.json`; pages, FAQs and the generator follow.

## Crawler-testing notes

* Real HTML pages with stable trailing-slash URLs. Accordions keep all panel text in the HTML (JS only
  toggles visibility). No login, CAPTCHA, hidden data fields or structured metadata.
* Information is spread across pages as on the reference: cycle months on *Become Our Partner*;
  the 4-step process (LOI, invitation-only application, board meeting months) on *Grant Application
  Process*; deadline months and the indirect-cost cap in *FAQs*; outcomes only in the Outcomes Sought PDF; and so on.
* Deliberately **absent** (as on the reference): per-grant award amounts or ranges, day-level
  deadlines, an LOI deadline, grant periods, required-attachment lists, reporting requirements, a public
  full-application form and an "Apply Now" button.
* `/portal/` is a demonstration applicant portal (sign-in, then eligibility quiz, then Letter of Inquiry). It
  stores and sends nothing and says so. It is excluded from the sitemap, like a vendor portal.
* `robots.txt` allows all crawlers. Every page carries `<meta name="robots" content="noindex, nofollow">`
  and Netlify serves `X-Robots-Tag: noindex, nofollow` on all responses, including PDFs (`dist/_headers`,
  `netlify.toml`). These directives *discourage* indexing by search engines that honor them; they cannot
  guarantee the site never appears in search results.

## Deployment (GitHub Pages)

The site is published as a GitHub Pages project site from the `gh-pages` branch:

```bash
npm run build:gh     # SITE_URL=https://hufsa-stack.github.io BASE_PATH=/wexmoor-foundation-demo
npm run test:gh      # same build + link check + browser tests under the sub-path
```

`BASE_PATH` makes `scripts/postbuild.mjs` prefix every root-relative URL (HTML, CSS, JS, sitemap,
search index). It also writes `.nojekyll` so Pages keeps the `_astro/` folder. GitHub Pages cannot set
custom response headers, so on Pages the `noindex, nofollow` directive is delivered by the
`<meta name="robots">` tag on every HTML page only. PDFs get no `X-Robots-Tag` there. A project site's
`robots.txt` lives under the sub-path, where crawlers do not look for it; the sitemap is at
`/wexmoor-foundation-demo/sitemap.xml`.

## Deployment (Netlify, alternative)

`netlify.toml` builds with `npm run build` and publishes `dist/`. With a Netlify account:

```bash
npx netlify-cli deploy --prod --dir dist          # after `netlify login` / `netlify link`
```

## Known deviations from the reference

| Reference element | Here | Reason |
|---|---|---|
| Photographs | Original SVG illustrations in the same positions/proportions | No reuse of reference imagery |
| X / LinkedIn footer icons | Omitted | A fictional org has no social accounts; dead links would break "meaningful destination" |
| Embedded YouTube videos (Board Chair, Teaching & Leadership) | Omitted or replaced by an illustration | No video exists to embed |
| Grantee names link to their websites | Plain names | Fictional organizations have no websites |
| Flipbook (FlipHTML5) annual-report embed | `<iframe>` of the PDF itself | Same placement, no third-party service |
| "Get Directions" map link | Omitted | Fictional address |
| Form 990-PF download | "Financial Summary and 990-PF Highlights" PDF | Avoids fabricating an IRS form replica |
| External YourCause portal | `/portal/` demo on the same host | No real portal for a fictional funder |
