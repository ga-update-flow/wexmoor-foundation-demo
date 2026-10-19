// Runs after `astro build`: writes sitemap.xml, robots.txt, search-index.json and Netlify _headers into dist/.
import fs from 'node:fs';
import path from 'node:path';

const DIST = path.resolve('dist');
const SITE = (process.env.SITE_URL || 'https://wexmoor-foundation-demo.netlify.app').replace(/\/$/, '');

function walk(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((e) => {
    const p = path.join(dir, e.name);
    return e.isDirectory() ? walk(p) : [p];
  });
}
const files = walk(DIST);
const toUrl = (f) => '/' + path.relative(DIST, f).split(path.sep).join('/').replace(/index\.html$/, '');

const pages = files.filter((f) => f.endsWith('index.html'))
  .map(toUrl)
  .filter((u) => !u.startsWith('/portal/'))   // the demo application portal is a tool, not content
  .sort();
const pdfs = files.filter((f) => f.endsWith('.pdf')).map(toUrl).sort();

const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${[...pages, ...pdfs].map((u) => `  <url><loc>${SITE}${u}</loc></url>`).join('\n')}
</urlset>
`;
fs.writeFileSync(path.join(DIST, 'sitemap.xml'), sitemap);

fs.writeFileSync(path.join(DIST, 'robots.txt'), `# Crawlers are welcome. Pages carry noindex directives to discourage search-engine indexing.
User-agent: *
Allow: /

Sitemap: ${SITE}/sitemap.xml
`);

// Search index for the header search box (titles + visible text of content pages).
const strip = (html) => html
  .replace(/<script[\s\S]*?<\/script>/g, ' ').replace(/<style[\s\S]*?<\/style>/g, ' ')
  .replace(/<header class="header"[\s\S]*?<\/header>/, ' ').replace(/<footer[\s\S]*?<\/footer>/g, ' ')
  .replace(/<div class="announce"[\s\S]*?<\/div>/, ' ')
  .replace(/<[^>]+>/g, ' ').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&[a-z#0-9]+;/gi, "'")
  .replace(/\s+/g, ' ').trim();
const index = pages.filter((u) => u !== '/search/').map((u) => {
  const html = fs.readFileSync(path.join(DIST, u, 'index.html'), 'utf8');
  const title = (html.match(/<title>([^<]*)<\/title>/) || [])[1]?.replace(/ - Wexmoor Foundation$/, '').replace(/&amp;/g, '&') || u;
  return { url: u, title, text: strip(html).slice(0, 6000) };
});
fs.writeFileSync(path.join(DIST, 'search-index.json'), JSON.stringify(index));

// Netlify response headers: discourage indexing of every response, including PDFs.
fs.writeFileSync(path.join(DIST, '_headers'), `/*
  X-Robots-Tag: noindex, nofollow

/*.pdf
  X-Robots-Tag: noindex, nofollow
  Content-Disposition: inline
`);

console.log(`postbuild: ${pages.length} pages + ${pdfs.length} PDFs in sitemap (${SITE}); search index ${index.length} entries`);
