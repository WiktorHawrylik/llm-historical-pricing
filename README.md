# llm-historical-pricing

Historical OpenAI LLM pricing data scraped from Wayback Machine archives. **Fixes required:**

- Prio 1: use archive.md instead of web.archive, since the later has only data for 2026
- But if you want to continue with web.archive than
  - Use latest to snapshot to fix the outputs, examples:
    - "gpt-4.1-nano" pricing captured at "2026-02-07T07:04:09+00:00" have 0.2, 0.4 and 0.8 which seem to be "output" price from batch, standard and priority pricing respecively, fix it.
    - "gpt-4.1-nano" pricing captured at "2026-02-07T07:04:09+00:00" all have null as cached_input value as well as input value is equal to output value. This is an error, fix it.
    - "gpt-4.1-nano" pricing captured at "2026-02-07T07:04:09+00:00"  - "pricing_type" is incorrectelly parsed, it should come from "Prices per 1M tokens." and be equal to "per_1kk_tokens"
    - There should be another field called "token_type" and should be equal to "text" for "Text tokens"

**Contents:**

- Historical pricing data: [data/output](data/output)
- Archived HTML snapshots: [data/input](data/input)
- Minimal standalone scraper with well-defined output format
- Selected [issues](docs/ISSUES.md) with Wayback Machine scraping

**Note:** OpenAI has 4 pricing tiers: [batch](https://platform.openai.com/docs/pricing?latest-pricing=batch), [flex](https://platform.openai.com/docs/pricing?latest-pricing=flex), [standard](https://platform.openai.com/docs/pricing?latest-pricing=standard), and [priority](https://platform.openai.com/docs/pricing?latest-pricing=priority). This scraper currently extracts standard pricing, there seems to be very few historical datapoints for others.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python scrape_wayback.py -o <output.json> [--from-date YYYYMMDD] [--no-cache]
```

### Required Arguments

- `-o, --output`: Output JSON file path (must end with `.json`)

### Optional Arguments

- `--from-date`: Start date in YYYYMMDD format (default: `20221101`)
- `--no-cache`: Bypass HTML cache and force re-download from Wayback Machine

### Examples

```bash
python scrape_wayback.py -o data/output/openai_pricing.json
python scrape_wayback.py -o data/output/recent.json --from-date 20260101
python scrape_wayback.py -o data/output/fresh.json --no-cache
```

## Output Format

The output is a JSON array of flat records, optimized for Spark and data analysis:

```json
[
  {
    "model": "gpt-4",
    "pricing_type": "per_1k_tokens",
    "category": "language_model",
    "captured_at": "2023-03-14T12:00:00+00:00",
    "input": 0.03,
    "cached_input": null,
    "output": 0.06
  }
]
```

### Field Descriptions

- `model`: Model name
- `pricing_type`: Pricing unit from HTML (e.g., "per_1k_tokens", "per_1m_tokens")
- `category`: Always `"language_model"`
- `captured_at`: Wayback Machine snapshot timestamp (ISO 8601, UTC)
- `input`: Input token price (float or null)
- `cached_input`: Cached input token price (prompt caching discount, float or null)
- `output`: Output token price (float or null)

**Note:** `captured_at` is the snapshot date, not the pricing effective date. Prices are reported as-is without conversion.

## How It Works

1. Queries Wayback Machine CDX API for archived snapshots (one per day)
2. Checks cache directory (`input/org_archive_web/com/openai/platform/docs/pricing/`)
3. Fetches HTML from Wayback Machine if not cached (1-second delay between requests)
4. Parses HTML to extract pricing data
5. Outputs flat JSON records sorted by timestamp

## Disclaimer

**Data Source:** Publicly available OpenAI pricing pages archived by Internet Archive's Wayback Machine.

**Purpose:** Informational, research, and archival use only.

**Affiliation:** Not affiliated with or endorsed by OpenAI. All pricing data belongs to OpenAI.

**License:** GPL-3.0 applies to scraper code only, not the data. Respect OpenAI's terms of service.

**Warranty:** Provided "as is" without warranty. Data may be incomplete or inaccurate.
