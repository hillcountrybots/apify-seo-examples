// Extract titles, meta descriptions, canonicals, Open Graph tags and JSON-LD types.
// Usage: node metadata.mjs https://wordpress.org/ https://www.python.org/
// Cost: $2 per 1,000 extracted pages. 404s, non-HTML and failures are free.
import { runActor, writeCsv } from './_client.mjs';

const urls = process.argv.slice(2);
const rows = await runActor('hillcountrybots/bulk-seo-metadata-extractor', {
    startUrls: urls.length ? urls : ['https://wordpress.org/', 'https://www.python.org/', 'https://web.dev/'],
    mode: 'urls',
    maxPages: 20,
});

const flat = rows.map((r) => ({
    url: r.url,
    title: r.title,
    titleLength: r.titleLength,
    metaDescriptionLength: r.metaDescriptionLength,
    canonical: r.canonical,
    canonicalIsSelf: r.canonicalIsSelf,
    isIndexable: r.isIndexable,
    h1Count: r.h1Count,
    jsonLdTypes: (r.jsonLdTypes ?? []).join(', '),
    status: r.status,
    errorCode: r.errorCode,
}));
for (const r of flat) console.log(`${r.url}: title ${r.titleLength} chars, H1s ${r.h1Count}, ${r.status}`);
writeCsv('metadata.csv', flat, Object.keys(flat[0] ?? { url: '' }));
