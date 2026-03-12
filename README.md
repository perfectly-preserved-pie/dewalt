# DEWALT Tool Table

DeWalt's website is trash and comically slow to browse and it PISSES me off. So I wanted to build a website that would allow me to quickly compare tools across categories without having to click through dozens of slow pages.

This website allows you to browse and compare DEWALT tools across multiple categories using Dash AG Grid. 

The app allows users to filter, sort, and compare tools based on various attributes such as price, features, and specifications.

The app is stylized using Dash Mantine Components and Dash Bootstrap Components, and it uses Dash AG Grid to display the tool data in an interactive table format.

## AI Disclosure

This app was created entirely with GPT-5.4.
![lulz](assets/aislop.png)

## Run

```bash
uv sync
uv run python3 app.py
```

## Data

The repo includes checked-in JSON snapshots under `data/`.

To refresh a dataset, run the scraper module for that tool family. Examples:

```bash
uv run python3 -m dewalt.scrape
uv run python3 -m dewalt.tool_families.drill_drivers.scrape
uv run python3 -m dewalt.tool_families.circular_saws.scrape
```

## Contributing

Please open an issue or submit a pull request with improvements, bug fixes, or new features.
Alternatively, you can email hey@xxxxxxxxxx