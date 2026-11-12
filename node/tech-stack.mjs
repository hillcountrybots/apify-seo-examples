// Detect the CMS, ecommerce platform, frameworks, CDN and analytics behind a list of websites.
// Usage: node tech-stack.mjs wordpress.org allbirds.com
// Cost: $0.50 per 1,000 analyzed sites. Sites that fail to load are free.
import { runActor, writeCsv } from './_client.mjs';

const sites = process.argv.slice(2);
const rows = await runActor('hillcountrybots/tech-stack-detector', {
    urls: sites.length ? sites : ['wordpress.org', 'https://www.allbirds.com/', 'https://nextjs.org/'],
});

const flat = rows.map((r) => ({
    url: r.url,
    cms: r.cms,
    ecommerce: r.ecommerce,
    server: r.server,
    frameworks: (r.frameworks ?? []).join(', '),
    technologies: (r.technologies ?? []).map((t) => t.name).join(', '),
    status: r.status,
}));
for (const r of flat) console.log(`${r.url}: CMS ${r.cms ?? '-'}, ecommerce ${r.ecommerce ?? '-'}`);
writeCsv('tech_stack.csv', flat, Object.keys(flat[0] ?? { url: '' }));
