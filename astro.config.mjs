import { defineConfig } from 'astro/config';

// SITE_URL is used for canonical/sitemap URLs. Set it to the deployed origin when building for production.
export default defineConfig({
  site: process.env.SITE_URL || 'https://wexmoor-foundation-demo.netlify.app',
  trailingSlash: 'always',
  build: { format: 'directory' },
  devToolbar: { enabled: false },
});
