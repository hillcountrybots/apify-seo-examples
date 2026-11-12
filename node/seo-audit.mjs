// Audit the pages of one or more sites for a 0 to 100 SEO score and the top issue on each page.
// Usage: node seo-audit.mjs https://example.com
// Cost: $2 per 1,000 audited pages. Failed pages are free.
import { runActor, writeCsv } from './_client.mjs';

const sites = process.argv.slice(2);
const rows = await runActor('hillcountrybots/seo-audit', {
    startUrls: sites.length ? sites : ['https://crawlee.dev'],
    maxPagesPerSite: 10,
});

const pages = rows.filter((r) => r.rowType === 'page'); // site-summary rows hold the per site totals
for (const r of pages) console.log(`${String(r.score ?? '-').padStart(4)}  ${r.url}  ${r.topIssue ?? r.errorMessage ?? ''}`);
writeCsv('seo_audit.csv', pages, ['url', 'score', 'grade', 'criticalCount', 'warningCount', 'topIssue', 'status', 'errorMessage']);
