"""Registration and expiry dates for a list of domains, from the official registry (RDAP).

Usage: python domain_expiry.py google.com wikipedia.org
Cost: $1 per 1,000 checked domains. Invalid entries are free.
"""
import sys

from _client import run_actor, write_csv

domains = sys.argv[1:] or ["google.com", "wikipedia.org", "python.org"]
rows = run_actor("hillcountrybots/domain-availability-checker", {"domains": domains})

rows.sort(key=lambda r: r.get("expiresAt") or "9999")
for r in rows:
    print(f"{r.get('domain'):30} {r.get('status'):12} expires {r.get('expiresAt') or '-'}  {r.get('registrar') or ''}")

write_csv("domains.csv", rows, ["domain", "status", "registrar", "createdAt", "expiresAt", "method", "note"])
