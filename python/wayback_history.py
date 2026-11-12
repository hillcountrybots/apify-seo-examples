"""Get yearly Wayback Machine snapshots for a URL or domain.

Usage: python wayback_history.py sitemaps.org
Cost: $1 per 1,000 rows. Empty lookups and failed archive calls are free.
"""
import sys

from _client import run_actor, write_csv

urls = sys.argv[1:] or ["sitemaps.org"]
rows = run_actor("hillcountrybots/wayback-history", {
    "urls": urls,
    "mode": "snapshots",
    "collapse": "year",
    "maxRowsPerUrl": 20,
    "maxRows": 40,
})

flat = []
for r in rows:
    flat.append({
        "input": r.get("input"),
        "url": r.get("url"),
        "capturedAt": r.get("capturedAt"),
        "statusCode": r.get("statusCode"),
        "snapshotUrl": r.get("snapshotUrl"),
        "status": r.get("status"),
        "errorCode": r.get("errorCode"),
    })
    print(f"{flat[-1]['capturedAt'] or flat[-1]['errorCode']}: {flat[-1]['url'] or flat[-1]['input']} {flat[-1]['statusCode'] or ''}")

write_csv("wayback_history.csv", flat, list(flat[0].keys()) if flat else ["input"])
