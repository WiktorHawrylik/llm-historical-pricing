# Quick Reference Guide

## Common Commands

### List all snapshots
```bash
python wayback_pricing.py list --url api
python wayback_pricing.py list --url chatgpt
```

### List snapshots with date range
```bash
# From November 2022 to December 2023
python wayback_pricing.py list --url api --start-date 20221101 --end-date 20231231

# Last 10 snapshots
python wayback_pricing.py list --url api --limit 10
```

### Get a specific snapshot
```bash
# Get snapshot from March 15, 2023
python wayback_pricing.py get --url api --date 20230315

# Get snapshot and view URL
python wayback_pricing.py get --url chatgpt --date 20230601
```

## URL Options

- `api` - OpenAI API pricing (https://platform.openai.com/docs/pricing)
- `chatgpt` - ChatGPT subscription pricing (https://openai.com/chatgpt/pricing)

## Date Format

All dates must be in `YYYYMMDD` format:
- `20221130` - November 30, 2022
- `20230315` - March 15, 2023
- `20240101` - January 1, 2024

## Output Format

### List Command
```
Date: 2023-03-15
  Wayback URL: https://web.archive.org/web/20230315.../pricing
```

### Get Command
```
Found snapshot:
Date: 2023-03-15
Wayback URL: https://web.archive.org/web/20230315.../pricing
```

## Integration Examples

### Python Script
```python
from wayback_pricing import WaybackPricingFetcher

fetcher = WaybackPricingFetcher()
snapshots = fetcher.list_snapshots(
    url="https://platform.openai.com/docs/pricing",
    start_date="20221101",
    limit=5
)

for snapshot in snapshots:
    print(f"{snapshot['date']}: {snapshot['wayback_url']}")
```

### Shell Script
```bash
#!/bin/bash
# Get monthly snapshots for 2023
for month in {01..12}; do
    python wayback_pricing.py get --url api --date 2023${month}01
done
```

## Tips

1. **Default start date**: If not specified, starts from November 1, 2022 (around ChatGPT launch)
2. **Snapshot frequency**: The tool collapses to daily snapshots to avoid overwhelming results
3. **Nearest match**: When getting a specific date, the tool finds the closest available snapshot
4. **Browser viewing**: Open the Wayback URL in a browser to view the archived page exactly as it appeared

## Troubleshooting

### No snapshots found
- Check your internet connection
- Verify the date range (snapshots may not exist for all dates)
- Try a broader date range

### Connection errors
- Ensure you can access web.archive.org
- Check firewall/proxy settings
- Wait a moment and retry (rate limiting)

## API Details

The tool uses the Internet Archive's CDX API:
- Endpoint: `https://web.archive.org/cdx/search/cdx`
- Filter: Only returns successful captures (HTTP 200)
- Collapse: Groups snapshots by day to reduce duplicates
