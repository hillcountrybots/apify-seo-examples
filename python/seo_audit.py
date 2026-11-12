"""Audit the pages of one or more sites for a 0 to 100 SEO score and the top issue on each page.

Usage: python seo_audit.py https://example.com
Cost: $2 per 1,000 audited pages. Failed pages are free.
"""
import sys

from _client import run_actor, write_csv

sites = sys.argv[1:] or ["https://crawlee.dev"]
rows = run_actor("hillcountrybots/seo-audit", {"startUrls": sites, "maxPagesPerSite": 10})

pages = [r for r in rows if r.get("rowType") == "page"]  # site-summary rows hold the per site totals
for r in pages:
    print(f"{r.get('score', '-'):>4}  {r.get('url')}  {r.get('topIssue') or r.get('errorMessage') or ''}")

write_csv("seo_audit.csv", pages, ["url", "rowType", "score", "grade", "criticalCount", "warningCount", "topIssue", "status", "errorMessage"])
