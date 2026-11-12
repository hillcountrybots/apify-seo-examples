"""Find broken links, redirects and HTTP status codes for a site or a URL list.

Usage: python broken_links.py https://example.com/ https://httpbin.org/status/404
Cost: $0.80 per 1,000 URLs that return an HTTP status. Failures and skips are free.
"""
import sys

from _client import run_actor, write_csv

urls = sys.argv[1:] or ["https://example.com/", "https://httpbin.org/status/404"]
rows = run_actor("hillcountrybots/broken-link-checker", {
    "startUrls": urls,
    "mode": "list",
    "maxUrlsToCheck": 20,
})

flat = []
for r in rows:
    chain = r.get("redirectChain") or []
    flat.append({
        "url": r.get("url"),
        "verdict": r.get("verdict"),
        "statusCode": r.get("statusCode"),
        "redirectCount": r.get("redirectCount"),
        "redirectChain": " > ".join(str(h) for h in chain),
        "foundOn": ", ".join(r.get("foundOn") or []),
        "anchorText": r.get("anchorText"),
        "isBroken": r.get("isBroken"),
        "status": r.get("status"),
        "errorCode": r.get("errorCode"),
    })
    print(f"{flat[-1]['url']}: {flat[-1]['verdict'] or flat[-1]['errorCode']} {flat[-1]['statusCode'] or ''}")

write_csv("broken_links.csv", flat, list(flat[0].keys()) if flat else ["url"])
