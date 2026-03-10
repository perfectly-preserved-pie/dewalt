# DEWALT Tool Table and Comparison

Dash app for browsing and comparing DEWALT angle grinders and drill drivers with Dash AG Grid.
The current scrapers are scoped to all corded tools plus bare-tool cordless SKUs.

## AI Disclosure
This app was generated entirely with GPT-5.4.

## Run

```bash
uv sync
uv run python3 app.py
```

## Refresh the angle-grinder snapshot

The checked-in dataset is intended to be a local snapshot. To refresh it from the
live DEWALT catalog:

```bash
uv run python3 -m dewalt.scrape
```

To build the snapshot from a local cache of DEWALT product pages instead:

```bash
uv run python3 -m dewalt.scrape --source-dir /tmp/dewalt-products
```

## Refresh the drill-driver snapshot

To refresh the checked-in drill-driver dataset from the live DEWALT catalog:

```bash
uv run python3 -m dewalt.tool_families.drill_drivers.scrape
```

To build that snapshot from a local cache of DEWALT product pages instead:

```bash
uv run python3 -m dewalt.tool_families.drill_drivers.scrape --source-dir /tmp/dewalt-drill-drivers
```
