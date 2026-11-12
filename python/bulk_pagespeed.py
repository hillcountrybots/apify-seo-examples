"""Core Web Vitals and Lighthouse scores for a list of URLs.

Usage: python bulk_pagespeed.py https://example.com https://example.org
Cost: $3 per 1,000 successful checks. Failed checks are free.
"""
import sys

from _client import run_actor, write_csv

urls = sys.argv[1:] or ["https://www.wikipedia.org/", "https://web.dev/"]
rows = run_actor("hillcountrybots/bulk-pagespeed-checker", {"urls": urls, "strategy": "mobile"})

flat = []
for r in rows:
    field = r.get("fieldData") or {}
    flat.append({
        "url": r.get("url"),
        "status": r.get("status"),
        "performance": (r.get("scores") or {}).get("performance"),
        "field_lcp_ms": (field.get("lcpMs") or {}).get("p75"),
        "field_inp_ms": (field.get("inpMs") or {}).get("p75"),
        "field_cls": (field.get("cls") or {}).get("p75"),
        "top_fix": ((r.get("opportunities") or [{}])[0]).get("title"),
        "error": r.get("errorMessage"),
    })
    print(f"{flat[-1]['url']}: performance {flat[-1]['performance']}, LCP {flat[-1]['field_lcp_ms']} ms")

write_csv("pagespeed.csv", flat, list(flat[0].keys()) if flat else ["url"])
