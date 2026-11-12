"""Shared helper: builds an Apify client from the APIFY_TOKEN environment variable."""
import csv
import os
import sys

from apify_client import ApifyClient


def get_client() -> ApifyClient:
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set APIFY_TOKEN first. Get it at https://console.apify.com/settings/integrations")
    return ApifyClient(token)


def run_actor(actor_id: str, run_input: dict) -> list[dict]:
    """Start an Actor, wait for it to finish, and return its dataset rows."""
    client = get_client()
    run = client.actor(actor_id).call(run_input=run_input)
    if run is None or run.get("status") != "SUCCEEDED":
        sys.exit(f"Run did not succeed: {run and run.get('status')}")
    return list(client.dataset(run["defaultDatasetId"]).iterate_items())


def write_csv(path: str, rows: list[dict], fields: list[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} rows to {path}")
