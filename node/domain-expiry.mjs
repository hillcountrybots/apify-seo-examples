// Registration and expiry dates for a list of domains, from the official registry (RDAP).
// Usage: node domain-expiry.mjs google.com wikipedia.org
// Cost: $1 per 1,000 checked domains. Invalid entries are free.
import { runActor, writeCsv } from './_client.mjs';

const domains = process.argv.slice(2);
const rows = await runActor('hillcountrybots/domain-availability-checker', {
    domains: domains.length ? domains : ['google.com', 'wikipedia.org', 'python.org'],
});

rows.sort((a, b) => (a.expiresAt ?? '9999').localeCompare(b.expiresAt ?? '9999'));
for (const r of rows) console.log(`${r.domain.padEnd(30)} ${String(r.status).padEnd(12)} expires ${r.expiresAt ?? '-'}  ${r.registrar ?? ''}`);
writeCsv('domains.csv', rows, ['domain', 'status', 'registrar', 'createdAt', 'expiresAt', 'method', 'note']);
