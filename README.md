# DEWALT Tool Table and Comparison

Dash app for browsing and comparing DEWALT bare-tool angle grinders with Dash AG Grid.
The scraper is currently scoped to all corded grinders plus bare-tool cordless SKUs.

## AI Disclosure
This app was generated entirely with GPT-5.4.

## Run

```bash
uv sync
uv run python3 app.py
```

## Refresh the grinder snapshot

The checked-in dataset is intended to be a local snapshot. To refresh it from the
live DEWALT catalog:

```bash
uv run python3 -m dewalt.scrape
```

To build the snapshot from a local cache of DEWALT product pages instead:

```bash
uv run python3 -m dewalt.scrape --source-dir /tmp/dewalt-products
```
