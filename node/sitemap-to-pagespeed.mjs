// Chain two Actors: pull every URL from a sitemap, then check Core Web Vitals for each one.
// Usage: node sitemap-to-pagespeed.mjs https://example.com 25
// The second argument caps how many URLs get a PageSpeed check (default 25).
// Cost for 25 URLs: about $0.01 for the sitemap step and $0.08 for PageSpeed.
import { runActor, writeCsv } from './_client.mjs';

const site = process.argv[2] ?? 'https://www.sitemaps.org/';
const cap = Number(process.argv[3] ?? 25);

const sitemapRows = await runActor('hillcountrybots/sitemap-url-extractor', { startUrls: [site], maxUrls: cap });
const urls = sitemapRows.filter((r) => r.status === 'ok').map((r) => r.url);
console.log(`Checking ${urls.length} URLs from the sitemap`);

const rows = await runActor('hillcountrybots/bulk-pagespeed-checker', { urls, strategy: 'mobile' });
const flat = rows
    .map((r) => ({ url: r.url, performance: r.scores?.performance, lab_lcp_ms: r.lab?.lcpMs, status: r.status }))
    .sort((a, b) => (a.performance ?? 999) - (b.performance ?? 999));
for (const r of flat.slice(0, 5)) console.log(`Slowest: ${r.url} performance ${r.performance}`);
writeCsv('site_pagespeed.csv', flat, ['url', 'performance', 'lab_lcp_ms', 'status']);
