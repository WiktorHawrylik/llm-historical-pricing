# llm-historical-pricing
LLM cost per token history

## Overview

This project uses the Internet Archive's Wayback Machine to retrieve historical pricing data for OpenAI's language models. It scrapes archived versions of OpenAI's pricing pages and compiles them into a structured JSON format.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the scraper to fetch historical pricing data:

```bash
python scrape_wayback.py
```

### Command Line Options

```bash
python scrape_wayback.py [options]

Options:
  -o, --output FILE      Output JSON file path (default: history.json)
  --from-date YYYYMMDD   Start date for snapshots (default: 20221101)
  --urls URL [URL ...]   Custom URLs to scrape (overrides defaults)
  -h, --help            Show help message
```

### Examples

Scrape with custom output file:
```bash
python scrape_wayback.py -o openai_pricing_history.json
```

Scrape from a specific date:
```bash
python scrape_wayback.py --from-date 20230101
```

Scrape custom URLs:
```bash
python scrape_wayback.py --urls https://example.com/pricing
```

This will:
1. Query the Wayback Machine for snapshots of OpenAI pricing pages going back to late 2022
2. Fetch and parse pricing information from each snapshot
3. Generate a `history.json` file with the compiled pricing history

The output JSON structure includes:
- `generated_at`: Timestamp when the data was generated
- `sources`: URLs that were scraped
- `history`: Array of pricing snapshots, each containing:
  - `date`: Human-readable date
  - `timestamp`: Wayback Machine timestamp
  - `source_url`: Original pricing page URL
  - `models`: Extracted pricing information

## Data Sources

The scraper retrieves data from:
- https://platform.openai.com/docs/pricing
- https://openai.com/chatgpt/pricing

## Sample Output

A sample output file (`history_sample.json`) is included in this repository to demonstrate the expected JSON structure. This shows how pricing data for models like GPT-4, GPT-3.5-turbo, and others are organized chronologically.

## How It Works

1. **Wayback Machine API**: Queries the Wayback Machine CDX API to find available snapshots
2. **Snapshot Retrieval**: Fetches HTML content from archived pages
3. **Price Extraction**: Parses HTML to extract model pricing information
4. **JSON Output**: Compiles data into a structured format similar to [openai-pricing-api](https://bes-dev.github.io/openai-pricing-api/history.json)
