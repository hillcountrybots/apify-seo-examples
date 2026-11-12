// Get yearly Wayback Machine snapshots for a URL or domain.
// Usage: node wayback-history.mjs sitemaps.org
// Cost: $1 per 1,000 rows. Empty lookups and failed archive calls are free.
import { runActor, writeCsv } from './_client.mjs';

const urls = process.argv.slice(2);
const rows = await runActor('hillcountrybots/wayback-history', {
    urls: urls.length ? urls : ['sitemaps.org'],
    mode: 'snapshots',
    collapse: 'year',
    maxRowsPerUrl: 20,
    maxRows: 40,
});

const flat = rows.map((r) => ({
    input: r.input,
    url: r.url,
    capturedAt: r.capturedAt,
    statusCode: r.statusCode,
    snapshotUrl: r.snapshotUrl,
    status: r.status,
    errorCode: r.errorCode,
}));
for (const r of flat) console.log(`${r.capturedAt ?? r.errorCode}: ${r.url ?? r.input} ${r.statusCode ?? ''}`);
writeCsv('wayback_history.csv', flat, Object.keys(flat[0] ?? { input: '' }));
