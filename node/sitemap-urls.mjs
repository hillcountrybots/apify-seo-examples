// Every URL from a site's XML sitemaps, including nested indexes and .gz files.
// Usage: node sitemap-urls.mjs https://example.com
// Cost: $0.50 per 1,000 URLs kept.
import { runActor, writeCsv } from './_client.mjs';

const sites = process.argv.slice(2);
const rows = await runActor('hillcountrybots/sitemap-url-extractor', {
    startUrls: sites.length ? sites : ['https://www.sitemaps.org/'],
    maxUrls: 500,
});

console.log(`Found ${rows.filter((r) => r.status === 'ok').length} URLs`);
writeCsv('sitemap_urls.csv', rows, ['url', 'lastmod', 'changefreq', 'priority', 'sourceSitemap', 'status', 'errorMessage']);
