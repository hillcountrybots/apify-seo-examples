"""Detect the CMS, ecommerce platform, frameworks, CDN and analytics behind a list of websites.

Usage: python tech_stack.py wordpress.org allbirds.com
Cost: $0.50 per 1,000 analyzed sites. Sites that fail to load are free.
"""
import sys

from _client import run_actor, write_csv

sites = sys.argv[1:] or ["wordpress.org", "https://www.allbirds.com/", "https://nextjs.org/"]
rows = run_actor("hillcountrybots/tech-stack-detector", {"urls": sites})

flat = []
for r in rows:
    flat.append({
        "url": r.get("url"),
        "cms": r.get("cms"),
        "ecommerce": r.get("ecommerce"),
        "server": r.get("server"),
        "frameworks": ", ".join(r.get("frameworks") or []),
        "technologies": ", ".join(t["name"] for t in (r.get("technologies") or [])),
        "status": r.get("status"),
    })
    print(f"{flat[-1]['url']}: CMS {flat[-1]['cms'] or '-'}, ecommerce {flat[-1]['ecommerce'] or '-'}")

write_csv("tech_stack.csv", flat, list(flat[0].keys()) if flat else ["url"])
