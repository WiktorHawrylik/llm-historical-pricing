# llm-historical-pricing

Scrape historical LLM pricing data from OpenAI using the Wayback Machine.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python scrape_wayback.py -o <output.json> [--from-date YYYYMMDD]
```

### Required Arguments
- `-o, --output`: Output JSON file path (must end with `.json`)

### Optional Arguments
- `--from-date`: Start date in YYYYMMDD format (default: `20221101`)

The script scrapes `https://platform.openai.com/docs/pricing` from the Wayback Machine.

### Examples

Scrape pricing history:
```bash
python scrape_wayback.py -o openai_pricing_history.json
```

Scrape from a specific date:
```bash
python scrape_wayback.py -o recent_pricing.json --from-date 20260101
```

## Output Format

The output is a JSON array of flat records, optimized for Spark and data analysis:

```json
[
  {
    "model": "gpt-4",
    "pricing_type": "per_1m_tokens",
    "category": "language_model",
    "timestamp": "2023-03-14T12:00:00+00:00",
    "input": 30.0,
    "cached_input": null,
    "output": 60.0
  }
]
```

### Field Descriptions
- `model`: Model name (string)
- `pricing_type`: Always `"per_1m_tokens"` (string)
- `category`: Always `"language_model"` (string)
- `timestamp`: ISO 8601 timestamp with UTC timezone (string)
- `input`: Input price per 1M tokens (float or null)
- `cached_input`: Cached input price per 1M tokens (float or null)
- `output`: Output price per 1M tokens (float or null)

**Note**: Prices are converted from per-1K-tokens to per-1M-tokens (×1000).

## How It Works

1. Queries Wayback Machine CDX API for archived snapshots (one per day)
2. Fetches HTML from archived pages (1 second delay between requests)
3. Parses HTML to extract pricing information
4. Outputs flat JSON records sorted by timestamp

The scraper retrieves all available snapshots from web.archive.org, including recent ones.

## Rate Limiting

Automatically adds 1 second delay between snapshot requests to respect Wayback Machine rate limits.
