# Apify SEO examples: PageSpeed, SEO audit, sitemaps, tech stack and domains in Python and Node.js

Small, runnable scripts that call five website checking tools on Apify with the official `apify-client` library and save the results to CSV. Copy one into your own project, a cron job or a notebook and you have bulk SEO data in a few lines.

We built these tools and these examples. We are [Hill Country Bots](https://hillcountrybots.com), a small shop that makes public website checks with a clear price per result. The examples are MIT licensed and free to use. Running the tools costs a fraction of a cent per result, paid through your Apify account, and failed checks are never charged.

| Tool on Apify | What it returns | Price |
|---|---|---|
| [Bulk PageSpeed Checker](https://apify.com/hillcountrybots/bulk-pagespeed-checker) | Lighthouse scores, lab metrics, real user Core Web Vitals (LCP, INP, CLS) and top fixes for a list of URLs | $3 per 1,000 checks |
| [SEO Audit Tool](https://apify.com/hillcountrybots/seo-audit) | A 0 to 100 score, grade and top issue per page, plus a site summary and an HTML report | $2 per 1,000 pages |
| [Sitemap URL Extractor](https://apify.com/hillcountrybots/sitemap-url-extractor) | Every URL from XML sitemaps, nested indexes and .gz files, with lastmod and source file | $0.50 per 1,000 URLs |
| [Tech Stack Detector](https://apify.com/hillcountrybots/tech-stack-detector) | CMS, ecommerce platform, frameworks, server, CDN and analytics per site | $0.50 per 1,000 sites |
| [Domain Availability Checker](https://apify.com/hillcountrybots/domain-availability-checker) | Registered or available, registrar, created and expiry dates from the official registry (RDAP) | $1 per 1,000 domains |

Prices are the live Apify Store prices as of November 11, 2026. New Apify accounts get a small free monthly credit, which covers trying every example here.

## Setup

1. Create a free account at [apify.com](https://apify.com) and copy your API token from [Settings, API and Integrations](https://console.apify.com/settings/integrations).
2. Put it in your environment. Never paste it into the code or commit it.

```bash
export APIFY_TOKEN=your_token_here
```

### Python (3.9 or newer)

```bash
cd python
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python bulk_pagespeed.py https://www.wikipedia.org/ https://web.dev/
```

### Node.js (18 or newer)

```bash
cd node
npm install
node bulk-pagespeed.mjs https://www.wikipedia.org/ https://web.dev/
```

## The examples

Each script runs with sensible defaults if you pass no arguments, prints a short summary and writes a CSV next to it.

| Task | Python | Node.js |
|---|---|---|
| Core Web Vitals for a list of URLs | `bulk_pagespeed.py` | `bulk-pagespeed.mjs` |
| SEO audit of one or more sites | `seo_audit.py` | `seo-audit.mjs` |
| Expiry dates for a list of domains | `domain_expiry.py` | `domain-expiry.mjs` |
| Every URL in a site's sitemaps | `sitemap_urls.py` | `sitemap-urls.mjs` |
| What a list of sites is built with | `tech_stack.py` | `tech-stack.mjs` |
| Sitemap to PageSpeed, chained | `sitemap_to_pagespeed.py` | `sitemap-to-pagespeed.mjs` |

The chained example is the one we use most. It pulls a site's URLs from its sitemap and sends them straight to the PageSpeed checker, so you get the slowest pages on a whole site in one command:

```bash
python sitemap_to_pagespeed.py https://www.sitemaps.org/ 25
```

### The core pattern

Every example is a variation of this:

```python
from apify_client import ApifyClient
import os

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("hillcountrybots/tech-stack-detector").call(
    run_input={"urls": ["wordpress.org", "https://www.allbirds.com/"]}
)
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(row["url"], row.get("cms"), row.get("ecommerce"))
```

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('hillcountrybots/tech-stack-detector').call({
    urls: ['wordpress.org', 'https://www.allbirds.com/'],
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const row of items) console.log(row.url, row.cms, row.ecommerce);
```

## Sample output

The [sample-output](sample-output) folder has the full JSON from real runs of all five tools on November 11, 2026, against public sites like wikipedia.org, web.dev, python.org and sitemaps.org. Each run also included a made up domain on purpose, so you can see what an error row looks like. Those error rows were not charged.

One PageSpeed row, shortened:

```json
{
  "url": "https://www.python.org/",
  "strategy": "mobile",
  "scores": { "performance": 90 },
  "fieldData": {
    "lcpMs": { "p75": 1319, "category": "FAST" },
    "inpMs": { "p75": 89, "category": "FAST" },
    "cls": { "p75": 0, "category": "FAST" }
  },
  "opportunities": [{ "title": "Render-blocking requests", "estimatedSavingsMs": 1600 }],
  "status": "ok"
}
```

## Tips

* **Cap your spend.** Every tool has a limit input (`maxUrls`, `maxPagesPerSite`, `maxResults`, `maxSites`), and Apify lets you set a maximum charge per run.
* **Schedule it.** Save a task in the Apify console and add a schedule, or use our free [n8n nodes](https://github.com/hillcountrybots/n8n-nodes) to drop results into Google Sheets or Slack every week.
* **Public data only.** These tools read public pages, sitemaps, DNS and registry records. They do not log in anywhere and do not collect personal data.

## More

* Free one page speed and SEO check, no account: [hillcountrybots.com/tools/free-site-check](https://hillcountrybots.com/tools/free-site-check)
* Guides: [How to check PageSpeed for many URLs](https://hillcountrybots.com/guides/how-to-check-pagespeed-for-many-urls), [How to find every page on a website](https://hillcountrybots.com/guides/how-to-find-all-pages-on-a-website)
* Questions or a bug: open an issue here or email hillcountrybots@proton.me

MIT licensed. Built by Hill Country Bots.
