// Shared helper: builds an Apify client from the APIFY_TOKEN environment variable.
import { writeFileSync } from 'node:fs';
import { ApifyClient } from 'apify-client';

export function getClient() {
    const token = process.env.APIFY_TOKEN;
    if (!token) {
        console.error('Set APIFY_TOKEN first. Get it at https://console.apify.com/settings/integrations');
        process.exit(1);
    }
    return new ApifyClient({ token });
}

// Start an Actor, wait for it to finish, and return its dataset rows.
export async function runActor(actorId, input) {
    const client = getClient();
    const run = await client.actor(actorId).call(input);
    if (run.status !== 'SUCCEEDED') throw new Error(`Run did not succeed: ${run.status}`);
    const { items } = await client.dataset(run.defaultDatasetId).listItems();
    return items;
}

export function writeCsv(path, rows, fields) {
    const cell = (v) => {
        const s = v == null ? '' : String(v);
        return /[",\n\r]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
    };
    const lines = [fields.join(','), ...rows.map((r) => fields.map((f) => cell(r[f])).join(','))];
    writeFileSync(path, lines.join('\n') + '\n');
    console.log(`Wrote ${rows.length} rows to ${path}`);
}
