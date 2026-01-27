# LLM Historical Pricing

A tool for tracking and analyzing historical pricing data for Large Language Models (LLMs), with a focus on OpenAI's pricing through the Internet Archive's Wayback Machine.

## Features

✅ **Internet Archive (Wayback Machine) Integration** — Access official pricing snapshots from OpenAI's original pricing pages

- View archived versions of [platform.openai.com/docs/pricing](https://platform.openai.com/docs/pricing) (API pricing)
- View archived versions of [openai.com/chatgpt/pricing](https://openai.com/chatgpt/pricing) (ChatGPT subscription pricing)
- Browse snapshots by date going back to late 2022 / early 2023 (when ChatGPT launched)
- Compare prices at different points in time

This is the most reliable method to see exact historical pricing from the original OpenAI pages themselves.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/WiktorHawrylik/llm-historical-pricing.git
cd llm-historical-pricing
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### List Available Snapshots

List all available archived snapshots of OpenAI pricing pages:

```bash
# List API pricing snapshots
python wayback_pricing.py list --url api

# List ChatGPT pricing snapshots
python wayback_pricing.py list --url chatgpt

# List with date range
python wayback_pricing.py list --url api --start-date 20221101 --end-date 20231231

# Limit number of results
python wayback_pricing.py list --url api --limit 10
```

### Get a Specific Snapshot

Retrieve a specific snapshot from a given date:

```bash
# Get API pricing from a specific date
python wayback_pricing.py get --url api --date 20230315

# Get ChatGPT pricing from a specific date
python wayback_pricing.py get --url chatgpt --date 20230601

# Fetch the actual HTML content (warning: can be large)
python wayback_pricing.py get --url api --date 20230315 --fetch-content
```

## How It Works

The tool uses the Internet Archive's Wayback Machine CDX API to:

1. **Search for snapshots** - Query the Wayback Machine for archived versions of OpenAI pricing pages
2. **Filter by date** - Find snapshots within a specific date range (default: November 2022 onwards)
3. **Generate URLs** - Create direct links to view the archived pages in your browser
4. **Fetch content** - Optionally download the archived HTML for analysis

## API Reference

### WaybackPricingFetcher Class

The main class for interacting with the Wayback Machine:

```python
from wayback_pricing import WaybackPricingFetcher

fetcher = WaybackPricingFetcher()

# List snapshots
snapshots = fetcher.list_snapshots(
    url="https://platform.openai.com/docs/pricing",
    start_date="20221101",
    end_date="20231231",
    limit=10
)

# Get a specific snapshot
snapshot = fetcher.get_snapshot(
    url="https://platform.openai.com/docs/pricing",
    date="20230315"
)

# Fetch content from a snapshot
content = fetcher.fetch_content(snapshot['wayback_url'])
```

## Example Output

```bash
$ python wayback_pricing.py list --url api --limit 5

Fetching snapshots for: https://platform.openai.com/docs/pricing
Date range: 20221101 to today

Found 5 snapshots:

Date: 2022-11-30
  Wayback URL: https://web.archive.org/web/20221130.../pricing

Date: 2022-12-15
  Wayback URL: https://web.archive.org/web/20221215.../pricing

Date: 2023-01-10
  Wayback URL: https://web.archive.org/web/20230110.../pricing
...
```

## Requirements

- Python 3.7+
- requests
- beautifulsoup4
- python-dateutil

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is provided as-is for educational and research purposes.

## Acknowledgments

- [Internet Archive's Wayback Machine](https://web.archive.org/) for providing access to historical web pages
- OpenAI for their pricing transparency
