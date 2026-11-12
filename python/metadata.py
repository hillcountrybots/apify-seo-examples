"""Extract titles, meta descriptions, canonicals, Open Graph tags and JSON-LD types.

Usage: python metadata.py https://wordpress.org/ https://www.python.org/
Cost: $2 per 1,000 extracted pages. 404s, non-HTML and failures are free.
"""
import sys

from _client import run_actor, write_csv

urls = sys.argv[1:] or ["https://wordpress.org/", "https://www.python.org/", "https://web.dev/"]
rows = run_actor("hillcountrybots/bulk-seo-metadata-extractor", {
    "startUrls": urls,
    "mode": "urls",
    "maxPages": 20,
})

flat = []
for r in rows:
    flat.append({
        "url": r.get("url"),
        "title": r.get("title"),
        "titleLength": r.get("titleLength"),
        "metaDescriptionLength": r.get("metaDescriptionLength"),
        "canonical": r.get("canonical"),
        "canonicalIsSelf": r.get("canonicalIsSelf"),
        "isIndexable": r.get("isIndexable"),
        "h1Count": r.get("h1Count"),
        "jsonLdTypes": ", ".join(r.get("jsonLdTypes") or []),
        "status": r.get("status"),
        "errorCode": r.get("errorCode"),
    })
    print(f"{flat[-1]['url']}: title {flat[-1]['titleLength']} chars, H1s {flat[-1]['h1Count']}, {flat[-1]['status']}")

write_csv("metadata.csv", flat, list(flat[0].keys()) if flat else ["url"])
