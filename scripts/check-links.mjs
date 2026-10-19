// Validates every internal link, image, script and iframe reference in dist/ resolves to a file.
import fs from 'node:fs';
import path from 'node:path';

const DIST = path.resolve('dist');
const BASE = (process.env.BASE_PATH || '').replace(/\/$/, '');
const walk = (d) => fs.readdirSync(d, { withFileTypes: true }).flatMap((e) => (e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]));
const htmlFiles = walk(DIST).filter((f) => f.endsWith('.html'));

let broken = 0, checked = 0;
const external = new Set();
for (const file of htmlFiles) {
  const html = fs.readFileSync(file, 'utf8');
  const pageUrl = BASE + '/' + path.relative(DIST, file).split(path.sep).join('/');
  for (const m of html.matchAll(/\s(?:href|src|action)="([^"]+)"/g)) {
    let ref = m[1].replace(/&amp;/g, '&');
    if (/^(mailto:|tel:|#|data:)/.test(ref)) continue;
    if (/^https?:\/\//.test(ref)) {
      const u = new URL(ref);
      if (u.hostname.includes('wexmoor-foundation')) ref = u.pathname; // canonical links
      else { external.add(u.origin); continue; }
    }
    ref = ref.split('#')[0].split('?')[0];
    if (!ref) continue;
    if (BASE && ref.startsWith('/')) {
      if (ref !== BASE && !ref.startsWith(BASE + '/')) { broken++; console.log(`MISSING BASE  ${pageUrl}  ->  ${m[1]}`); continue; }
      ref = ref.slice(BASE.length) || '/';
    }
    const abs = ref.startsWith('/') ? ref : path.posix.join(path.posix.dirname(pageUrl.slice(BASE.length)), ref);
    const target = path.join(DIST, decodeURIComponent(abs));
    const ok = fs.existsSync(target) && (fs.statSync(target).isFile() || fs.existsSync(path.join(target, 'index.html')));
    checked++;
    if (!ok) { broken++; console.log(`BROKEN  ${pageUrl}  ->  ${m[1]}`); }
  }
}
console.log(`${htmlFiles.length} HTML files, ${checked} internal references checked, ${broken} broken.`);
console.log('External origins referenced:', [...external].join(', ') || '(none)');
process.exit(broken ? 1 : 0);
