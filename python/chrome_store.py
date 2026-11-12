"""Look up public Chrome Web Store data for extension IDs or store URLs.

Usage: python chrome_store.py nngceckbapebfimnlniiiahkandclblb
Cost: $1.50 per 1,000 extensions. Not-found and failed lookups are free.
"""
import sys

from _client import run_actor, write_csv

exts = sys.argv[1:] or [
    "nngceckbapebfimnlniiiahkandclblb",  # Bitwarden
    "aapbdbdomjkkjkaonfhkkikfgjllcleb",  # Google Translate
]
rows = run_actor("hillcountrybots/chrome-web-store-scraper", {
    "extensions": exts,
    "maxItems": 10,
    "includeDescription": False,
})

flat = []
for r in rows:
    perms = r.get("permissions") or []
    flat.append({
        "extensionId": r.get("extensionId"),
        "name": r.get("name"),
        "users": r.get("users"),
        "rating": r.get("rating"),
        "ratingCount": r.get("ratingCount"),
        "version": r.get("version"),
        "manifestVersion": r.get("manifestVersion"),
        "permissions": ", ".join(perms),
        "publisherName": r.get("publisherName"),
        "status": r.get("status"),
        "errorCode": r.get("errorCode"),
    })
    print(f"{flat[-1]['name'] or flat[-1]['extensionId']}: {flat[-1]['users']} users, v{flat[-1]['version']}, {flat[-1]['status']}")

write_csv("chrome_store.csv", flat, list(flat[0].keys()) if flat else ["extensionId"])
