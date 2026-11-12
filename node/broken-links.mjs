// Find broken links, redirects and HTTP status codes for a site or a URL list.
// Usage: node broken-links.mjs https://example.com/ https://httpbin.org/status/404
// Cost: $0.80 per 1,000 URLs that return an HTTP status. Failures and skips are free.
import { runActor, writeCsv } from './_client.mjs';

const urls = process.argv.slice(2);
const rows = await runActor('hillcountrybots/broken-link-checker', {
    startUrls: urls.length ? urls : ['https://example.com/', 'https://httpbin.org/status/404'],
    mode: 'list',
    maxUrlsToCheck: 20,
});

const flat = rows.map((r) => ({
    url: r.url,
    verdict: r.verdict,
    statusCode: r.statusCode,
    redirectCount: r.redirectCount,
    redirectChain: (r.redirectChain ?? []).join(' > '),
    foundOn: (r.foundOn ?? []).join(', '),
    anchorText: r.anchorText,
    isBroken: r.isBroken,
    status: r.status,
    errorCode: r.errorCode,
}));
for (const r of flat) console.log(`${r.url}: ${r.verdict ?? r.errorCode} ${r.statusCode ?? ''}`);
writeCsv('broken_links.csv', flat, Object.keys(flat[0] ?? { url: '' }));
