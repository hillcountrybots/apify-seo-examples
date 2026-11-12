// Core Web Vitals and Lighthouse scores for a list of URLs.
// Usage: node bulk-pagespeed.mjs https://example.com https://example.org
// Cost: $3 per 1,000 successful checks. Failed checks are free.
import { runActor, writeCsv } from './_client.mjs';

const urls = process.argv.slice(2);
const rows = await runActor('hillcountrybots/bulk-pagespeed-checker', {
    urls: urls.length ? urls : ['https://www.wikipedia.org/', 'https://web.dev/'],
    strategy: 'mobile',
});

const flat = rows.map((r) => ({
    url: r.url,
    status: r.status,
    performance: r.scores?.performance,
    field_lcp_ms: r.fieldData?.lcpMs?.p75,
    field_inp_ms: r.fieldData?.inpMs?.p75,
    field_cls: r.fieldData?.cls?.p75,
    top_fix: r.opportunities?.[0]?.title,
    error: r.errorMessage,
}));
for (const r of flat) console.log(`${r.url}: performance ${r.performance}, LCP ${r.field_lcp_ms} ms`);
writeCsv('pagespeed.csv', flat, Object.keys(flat[0] ?? { url: '' }));
