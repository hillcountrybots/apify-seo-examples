// Look up public Chrome Web Store data for extension IDs or store URLs.
// Usage: node chrome-store.mjs nngceckbapebfimnlniiiahkandclblb
// Cost: $1.50 per 1,000 extensions. Not-found and failed lookups are free.
import { runActor, writeCsv } from './_client.mjs';

const exts = process.argv.slice(2);
const rows = await runActor('hillcountrybots/chrome-web-store-scraper', {
    extensions: exts.length ? exts : [
        'nngceckbapebfimnlniiiahkandclblb', // Bitwarden
        'aapbdbdomjkkjkaonfhkkikfgjllcleb', // Google Translate
    ],
    maxItems: 10,
    includeDescription: false,
});

const flat = rows.map((r) => ({
    extensionId: r.extensionId,
    name: r.name,
    users: r.users,
    rating: r.rating,
    ratingCount: r.ratingCount,
    version: r.version,
    manifestVersion: r.manifestVersion,
    permissions: (r.permissions ?? []).join(', '),
    publisherName: r.publisherName,
    status: r.status,
    errorCode: r.errorCode,
}));
for (const r of flat) console.log(`${r.name ?? r.extensionId}: ${r.users} users, v${r.version}, ${r.status}`);
writeCsv('chrome_store.csv', flat, Object.keys(flat[0] ?? { extensionId: '' }));
