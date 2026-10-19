// End-to-end checks in headless Chromium against a local static server of dist/.
// Usage: node scripts/browser-test.mjs [baseUrl]   (default starts a local server on :4399)
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); } catch { ({ chromium } = require('/opt/node-tools/node_modules/playwright')); }

const DIST = path.resolve('dist');
let BASE = process.argv[2];
let server;
if (!BASE) {
  const types = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.pdf': 'application/pdf', '.json': 'application/json', '.png': 'image/png', '.ico': 'image/x-icon', '.xml': 'application/xml', '.txt': 'text/plain' };
  server = http.createServer((req, res) => {
    let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
    let f = path.join(DIST, p);
    if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html');
    if (!fs.existsSync(f)) { res.writeHead(404); return res.end(fs.readFileSync(path.join(DIST, '404.html'))); }
    res.writeHead(200, { 'content-type': types[path.extname(f)] || 'application/octet-stream' });
    fs.createReadStream(f).pipe(res);
  }).listen(4399);
  BASE = 'http://localhost:4399';
}

const sitemap = fs.readFileSync(path.join(DIST, 'sitemap.xml'), 'utf8');
const urls = [...sitemap.matchAll(/<loc>[^<]*?(\/[^<]*)<\/loc>/g)].map((m) => new URL(m[1], 'http://x').pathname);
const pages = [...urls.filter((u) => !u.endsWith('.pdf')), '/portal/', '/portal/eligibility-quiz/', '/portal/letter-of-inquiry/'];
const pdfs = urls.filter((u) => u.endsWith('.pdf'));

const results = [];
const check = (name, ok, detail = '') => { results.push({ name, ok, detail }); console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? '  ' + detail : ''}`); };

const browser = await chromium.launch();
try {
  for (const [w, h, label] of [[1440, 900, 'desktop'], [390, 844, 'mobile']]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h } });
    const page = await ctx.newPage();
    const errors = [];
    page.on('pageerror', (e) => errors.push(e.message));
    page.on('console', (m) => { if (m.type() === 'error' && !/fonts\.(googleapis|gstatic)/.test(m.text())) errors.push(m.text()); });
    let bad = [];
    for (const u of pages) {
      errors.length = 0;
      const r = await page.goto(BASE + u, { waitUntil: 'load' });
      const robots = await page.getAttribute('meta[name="robots"]', 'content');
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
      const h1 = await page.locator('h1').count();
      if (r.status() !== 200 || robots !== 'noindex, nofollow' || errors.length || overflow || !h1)
        bad.push(`${u} status=${r.status()} robots=${robots} errors=${errors.join('|')} overflow=${overflow} h1=${h1}`);
    }
    check(`${label}: ${pages.length} pages load (200, noindex meta, no JS errors, h1, no horizontal scroll)`, !bad.length, bad.join('\n'));
    await ctx.close();
  }

  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();

  // Homepage popup + hero button
  await page.goto(BASE + '/');
  await page.waitForTimeout(1000);
  check('home: annual report popup auto-opens', await page.locator('#report-popup').evaluate((d) => d.open));
  await page.click('#report-popup .pum-close');
  check('home: popup closes', !(await page.locator('#report-popup').evaluate((d) => d.open)));
  await page.click('.home-hero a.btn-solid');
  check('home: Learn More button -> About', page.url().endsWith('/about-the-foundation/'));

  // Dropdown menus
  await page.goto(BASE + '/');
  for (const [i, n] of [[0, 7], [1, 4], [2, 2]]) {
    const li = page.locator('#main-nav > li').nth(i);
    await li.hover();
    const vis = await li.locator('.sub-menu a:visible').count();
    check(`nav: dropdown ${i + 1} shows ${n} items on hover`, vis === n, `visible=${vis}`);
  }

  // Announcement bar
  await page.click('[data-announce-close]');
  check('announcement bar dismisses', await page.locator('[data-announce]').evaluate((e) => e.classList.contains('is-hidden')));

  // Accordions
  for (const u of ['/become-our-partner/grant-application-process/', '/become-our-partner/faqs/']) {
    await page.goto(BASE + u);
    const items = page.locator('.accordion-item');
    const n = await items.count();
    const firstOpen = await items.nth(0).locator('.accordion_content').isVisible();
    const secondHidden = !(await items.nth(1).locator('.accordion_content').isVisible());
    await items.nth(1).locator('button').click();
    const toggled = (await items.nth(1).locator('.accordion_content').isVisible()) && !(await items.nth(0).locator('.accordion_content').isVisible());
    const html = await page.content();
    const allInDom = (await page.locator('.accordion_content').count()) === n && html.includes(u.includes('faqs') ? 'Indirect' : 'Board meets in April');
    check(`${u}: accordion (${n} items) expands/collapses; collapsed text present in HTML`, firstOpen && secondHidden && toggled && allInDom);
  }

  // Search
  await page.goto(BASE + '/');
  await page.fill('.search-field', 'indirect');
  await page.press('.search-field', 'Enter');
  await page.waitForSelector('#search-results article', { timeout: 5000 }).catch(() => {});
  check('search: header search returns results', (await page.locator('#search-results article').count()) > 0);

  // Portal flow
  await page.goto(BASE + '/become-our-partner/grant-application-process/');
  await page.click('.accordion_content a:has-text("Eligibility Quiz") >> nth=0');
  check('process: Eligibility Quiz link -> portal sign-in', page.url().endsWith('/portal/'));
  await page.fill('#p-email', 'tester@example.org');
  await page.click('button:has-text("Sign in")');
  await page.waitForURL('**/portal/eligibility-quiz/');
  check('portal: sign in continues to quiz without sending email', !page.url().includes('example.org'));
  for (const [n, v] of [['orgtype', 'yes'], ['geo', 'yes'], ['focus', 'yes'], ['excluded', 'yes'], ['reviewed', 'yes']]) await page.check(`input[name=${n}][value=${v}]`);
  await page.click('button:has-text("Check eligibility")');
  check('quiz: excluded answer -> not eligible', await page.locator('#quiz-fail').isVisible());
  await page.check('input[name=excluded][value=no]');
  await page.click('button:has-text("Check eligibility")');
  check('quiz: eligible answers -> continue to LOI', await page.locator('#quiz-pass').isVisible());
  await page.click('text=Continue to Letter of Inquiry');
  await page.fill('#c-first', 'Test'); await page.fill('#c-last', 'User'); await page.fill('#c-email', 'test@example.org');
  await page.fill('#o-name', 'Test Org'); await page.fill('#o-ein', '12-3456789'); await page.fill('#o-desc', 'Testing');
  await page.selectOption('#o-geo', { index: 1 });
  const reqs = [];
  page.on('request', (r) => { if (r.method() !== 'GET') reqs.push(r.url()); });
  await page.click('button:has-text("Submit Letter of Inquiry")');
  check('LOI: demo submit shows honest notice and sends nothing', (await page.locator('.form-status').isVisible()) && !reqs.length && (await page.locator('.form-status').innerText()).includes('not'));

  // Newsletter demo
  await page.goto(BASE + '/contact-us/');
  await page.fill('#nl-email', 'test@example.org');
  await page.click('button:has-text("Subscribe")');
  check('contact: newsletter demo shows honest notice', await page.locator('.form-status').isVisible());

  // Mobile menu
  const m = await browser.newContext({ viewport: { width: 390, height: 844 } });
  const mp = await m.newPage();
  await mp.goto(BASE + '/what-we-fund/');
  await mp.click('[data-menu-toggle]');
  const mobileLinks = await mp.locator('#mobile-menu a:visible').count();
  check('mobile: hamburger opens full menu hierarchy', mobileLinks === 17, `links=${mobileLinks}`);
  await m.close();

  // PDFs
  let pdfBad = [];
  for (const u of pdfs) {
    const r = await page.request.get(BASE + u);
    const body = await r.body();
    if (r.status() !== 200 || body.subarray(0, 5).toString() !== '%PDF-') pdfBad.push(u);
  }
  check(`PDFs: ${pdfs.length} documents download as valid PDF`, !pdfBad.length, pdfBad.join(', '));
  if (process.argv[2]) {
    const xr = await page.request.get(BASE + pdfs[0]);
    check('PDF responses carry X-Robots-Tag noindex', /noindex/.test(xr.headers()['x-robots-tag'] || ''), xr.headers()['x-robots-tag']);
    const hr = await page.request.get(BASE + '/');
    check('HTML responses carry X-Robots-Tag noindex', /noindex/.test(hr.headers()['x-robots-tag'] || ''));
  }
  await ctx.close();
} finally {
  await browser.close();
  server && server.close();
}
const failed = results.filter((r) => !r.ok).length;
console.log(`\n${results.length - failed}/${results.length} checks passed`);
process.exit(failed ? 1 : 0);
