"""Every URL from a site's XML sitemaps, including nested indexes and .gz files.

Usage: python sitemap_urls.py https://example.com
Cost: $0.50 per 1,000 URLs kept.
"""
import sys

from _client import run_actor, write_csv

sites = sys.argv[1:] or ["https://www.sitemaps.org/"]
rows = run_actor("hillcountrybots/sitemap-url-extractor", {"startUrls": sites, "maxUrls": 500})

ok = [r for r in rows if r.get("status") == "ok"]
print(f"Found {len(ok)} URLs")
write_csv("sitemap_urls.csv", rows, ["url", "lastmod", "changefreq", "priority", "sourceSitemap", "status", "errorMessage"])
