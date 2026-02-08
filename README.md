# llm-historical-pricing

In this repo you will find 
- OpenAI historical LLM pricing in [data/output](data/output) 
- OpenAI `https://platform.openai.com/docs/pricing` HTML snapshots in [data/input](data/input) 
- OpenAI historical LLM pricing scrapers, simplistic and mininal stanalone scripts that processed data into well defiend unified format
- List of [issues](docs/ISSUES.md) with scraping OpenAI data from Wayback Machine

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

The script scrapes `https://platform.openai.com/docs/pricing` from the Wayback Machine.

### Examples

Scrape pricing history:

```bash
python scrape_wayback.py -o data/output/data/output/wayback_openai_prices_since_2023.json
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
- `model`: Model name (string)
- `pricing_type`: Pricing unit as found in the HTML (e.g., "per_1k_tokens", "per_1m_tokens")
- `category`: Always `"language_model"` (string)
- `captured_at`: Wayback Machine snapshot timestamp in ISO 8601 format with UTC timezone (string)
- `input`: Input price in the unit specified by pricing_type (float or null)
- `cached_input`: Cached input price in the unit specified by pricing_type (float or null). A feature where OpenAI charges less for input tokens that have been cached from previous API requests.
- `output`: Output price in the unit specified by pricing_type (float or null)

**Note**: `captured_at` represents captured snapshot, not when OpenAI implemented the pricing. Prices are reported as-is from the source HTML without conversion.

## How It Works

1. Queries Wayback Machine CDX API for archived snapshots (one per day)
2. Checks cache directory (`data/input/org_archive_web/com/openai/platform/docs/pricing/`) for previously downloaded HTML
3. Fetches HTML from archived pages if not cached (1 second delay between requests)
4. Parses HTML to extract pricing information
5. Outputs flat JSON records sorted by timestamp to `data/output/`

The scraper retrieves all available snapshots from web.archive.org, including recent ones. HTML snapshots are cached locally to avoid redundant downloads.

## Rate Limiting

Automatically adds 1 second delay between snapshot requests to respect Wayback Machine rate limits.

## Data Disclaimer

**Data Source**: This project scrapes publicly available pricing information from OpenAI's pricing documentation page (`platform.openai.com/docs/pricing`) via the Internet Archive's Wayback Machine.

**Purpose**: This tool and the data it generates are provided for **informational, research, and archival purposes only**. The data represents historical snapshots of publicly posted pricing information.

**No Affiliation**: This project is not affiliated with, endorsed by, or sponsored by OpenAI. All pricing data belongs to OpenAI and is subject to their terms of service.

**License**: The GPL-3.0 license applies to the scraper code only, not to the pricing data itself. Users should respect OpenAI's intellectual property rights and terms of service when using this data.

**No Warranty**: The data is provided "as is" without warranty of any kind. Pricing information may be incomplete, inaccurate, or outdated.
