# DEWALT Tool Table and Comparison

Dash app for browsing and comparing DEWALT angle grinders, circular saws, miter saws, table saws, drill drivers, impact drivers, impact wrenches, ratchets, hammer drills, rotary hammers, oscillating multi-tools, cut-out tools, finish/brad nailers, and vacuums with Dash AG Grid.
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

## Refresh the circular-saw snapshot

To refresh the checked-in circular-saw dataset from the live DEWALT catalog:

```bash
uv run python3 -m dewalt.tool_families.circular_saws.scrape
```

To build that snapshot from a local cache of DEWALT product pages instead:

```bash
uv run python3 -m dewalt.tool_families.circular_saws.scrape --source-dir /tmp/dewalt-circular-saws
```

## Refresh the miter-saw snapshot

To refresh the checked-in miter-saw dataset from the live DEWALT catalog:

```bash
uv run python3 -m dewalt.tool_families.miter_saws.scrape
```

To build that snapshot from a local cache of DEWALT product pages instead:

```bash
uv run python3 -m dewalt.tool_families.miter_saws.scrape --source-dir /tmp/dewalt-miter-saws
```

## Refresh the table-saw snapshot

To refresh the checked-in table-saw dataset from the live DEWALT catalog:

```bash
uv run python3 -m dewalt.tool_families.table_saws.scrape
```

To build that snapshot from a local cache of DEWALT product pages instead:

```bash
uv run python3 -m dewalt.tool_families.table_saws.scrape --source-dir /tmp/dewalt-table-saws
```

## Refresh the cut-out-tool snapshot

To refresh the checked-in cut-out-tool dataset from the live DEWALT catalog:

```bash
uv run python3 -m dewalt.tool_families.cut_out_tools.scrape
```

To build that snapshot from a local cache of DEWALT product pages instead:

```bash
uv run python3 -m dewalt.tool_families.cut_out_tools.scrape --source-dir /tmp/dewalt-cut-out-tools
```

## Refresh the finish/brad-nailer snapshot

To refresh the checked-in finish/brad-nailer dataset from the live DEWALT catalog:

```bash
uv run python3 -m dewalt.tool_families.finish_brad_nailers.scrape
```

To build that snapshot from a local cache of DEWALT product pages instead:

```bash
uv run python3 -m dewalt.tool_families.finish_brad_nailers.scrape --source-dir /tmp/dewalt-finish-brad-nailers
```

## Refresh the hammer-drill snapshot

To refresh the checked-in hammer-drill dataset from the live DEWALT catalog:

```bash
uv run python3 -m dewalt.tool_families.hammer_drills.scrape
```

To build that snapshot from a local cache of DEWALT product pages instead:

```bash
uv run python3 -m dewalt.tool_families.hammer_drills.scrape --source-dir /tmp/dewalt-hammer-drills
```

## Refresh the impact-driver snapshot

To refresh the checked-in impact-driver dataset from the live DEWALT catalog:

```bash
uv run python3 -m dewalt.tool_families.impact_drivers.scrape
```

To build that snapshot from a local cache of DEWALT product pages instead:

```bash
uv run python3 -m dewalt.tool_families.impact_drivers.scrape --source-dir /tmp/dewalt-impact-drivers
```

## Refresh the impact-wrench snapshot

To refresh the checked-in impact-wrench dataset from the live DEWALT catalog:

```bash
uv run python3 -m dewalt.tool_families.impact_wrenches.scrape
```

To build that snapshot from a local cache of DEWALT product pages instead:

```bash
uv run python3 -m dewalt.tool_families.impact_wrenches.scrape --source-dir /tmp/dewalt-impact-wrenches
```

## Refresh the oscillating multi-tool snapshot

To refresh the checked-in oscillating multi-tool dataset from the live DEWALT catalog:

```bash
uv run python3 -m dewalt.tool_families.oscillating_multi_tools.scrape
```

To build that snapshot from a local cache of DEWALT product pages instead:

```bash
uv run python3 -m dewalt.tool_families.oscillating_multi_tools.scrape --source-dir /tmp/dewalt-oscillating-multi-tools
```

## Refresh the ratchet snapshot

To refresh the checked-in ratchet dataset from the live DEWALT catalog:

```bash
uv run python3 -m dewalt.tool_families.ratchets.scrape
```

To build that snapshot from a local cache of DEWALT product pages instead:

```bash
uv run python3 -m dewalt.tool_families.ratchets.scrape --source-dir /tmp/dewalt-ratchets
```

## Refresh the rotary-hammer snapshot

To refresh the checked-in rotary-hammer dataset from the live DEWALT catalog:

```bash
uv run python3 -m dewalt.tool_families.rotary_hammers.scrape
```

To build that snapshot from a local cache of DEWALT product pages instead:

```bash
uv run python3 -m dewalt.tool_families.rotary_hammers.scrape --source-dir /tmp/dewalt-rotary-hammers
```

## Refresh the vacuum snapshot

To refresh the checked-in vacuum dataset from the live DEWALT catalog:

```bash
uv run python3 -m dewalt.tool_families.vacuums.scrape
```

To build that snapshot from a local cache of DEWALT product pages instead:

```bash
uv run python3 -m dewalt.tool_families.vacuums.scrape --source-dir /tmp/dewalt-vacuums
```
