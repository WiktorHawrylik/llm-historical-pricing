#!/usr/bin/env python3
"""Test the transformation to new output format."""

import json
import sys
from pathlib import Path

# Add parent directory to path to import scrape_wayback
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scrape_wayback import WaybackScraper

# Sample data in the old format
sample_old_format = [
    {
        "date": "2022-12-01",
        "timestamp": "20221201120000",
        "source_url": "https://platform.openai.com/docs/pricing",
        "models": [
            {
                "name": "gpt-3.5-turbo",
                "input_price_per_1k": 0.0015,
                "output_price_per_1k": 0.002
            },
            {
                "name": "text-davinci-003",
                "price_per_1k": 0.02
            }
        ]
    },
    {
        "date": "2023-03-01",
        "timestamp": "20230301120000",
        "source_url": "https://platform.openai.com/docs/pricing",
        "models": [
            {
                "name": "gpt-4",
                "input_price_per_1k": 0.03,
                "output_price_per_1k": 0.06
            }
        ]
    }
]

scraper = WaybackScraper()
records = scraper.transform_to_records(sample_old_format)

print(json.dumps(records, indent=2))
print(f"\nTransformed {len(records)} records")

# Assertions
assert len(records) == 3, f"Expected 3 records, got {len(records)}"
assert isinstance(records, list), "Output should be a list"

# Check first record structure
record = records[0]
assert record['model'] == 'gpt-3.5-turbo'
assert record['pricing_type'] == 'per_1k_tokens'
assert record['category'] == 'language_model'
assert record['timestamp'] == '2022-12-01T12:00:00+00:00'
assert record['input'] == 0.0015  # No conversion
assert record['cached_input'] is None
assert record['output'] == 0.002  # No conversion

# Verify all records have flat structure (no nested objects)
for r in records:
    assert all(not isinstance(v, (dict, list)) or v is None for v in r.values()), \
        "All values should be primitives (no nested structures)"
    assert set(r.keys()) == {'model', 'pricing_type', 'category', 'captured_at', 'input', 'cached_input', 'output'}, \
        f"Unexpected keys: {r.keys()}"

print("\n✓ All assertions passed!")
