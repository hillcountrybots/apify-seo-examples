"""Chain two Actors: pull every URL from a sitemap, then check Core Web Vitals for each one.

Usage: python sitemap_to_pagespeed.py https://example.com 25
The second argument caps how many URLs get a PageSpeed check (default 25).
Cost for 25 URLs: about $0.01 for the sitemap step and $0.08 for PageSpeed.
"""
import sys

from _client import run_actor, write_csv

site = sys.argv[1] if len(sys.argv) > 1 else "https://www.sitemaps.org/"
cap = int(sys.argv[2]) if len(sys.argv) > 2 else 25

urls = [r["url"] for r in run_actor("hillcountrybots/sitemap-url-extractor", {"startUrls": [site], "maxUrls": cap}) if r.get("status") == "ok"]
print(f"Checking {len(urls)} URLs from the sitemap")

rows = run_actor("hillcountrybots/bulk-pagespeed-checker", {"urls": urls, "strategy": "mobile"})
flat = [{
    "url": r.get("url"),
    "performance": (r.get("scores") or {}).get("performance"),
    "lab_lcp_ms": (r.get("lab") or {}).get("lcpMs"),
    "status": r.get("status"),
} for r in rows]
flat.sort(key=lambda r: r["performance"] if r["performance"] is not None else 999)
for r in flat[:5]:
    print(f"Slowest: {r['url']} performance {r['performance']}")
write_csv("site_pagespeed.csv", flat, ["url", "performance", "lab_lcp_ms", "status"])
