# Copilot Instructions: LLM Historical Pricing Scraper

## Project Overview
Simple web scraper that extracts historical LLM pricing data from Wayback Machine archives and outputs flat JSON records optimized for Spark/data analysis.

## Core Requirements

### Output Schema (STRICT)
Always output a flat JSON array. Each record must have exactly these fields:
```json
{
  "model": "string",
  "pricing_type": "string (as found in HTML)",
  "category": "language_model",
  "timestamp": "ISO-8601 with +00:00 timezone",
  "input": float | null,
  "cached_input": float | null,
  "output": float | null
}
```

**Critical rules:**
- Prices are reported AS-IS from source HTML (NO conversion)
- `pricing_type` should reflect the actual pricing unit from the HTML (e.g., "per_1k_tokens", "per_1m_tokens")
- `category` is always `"language_model"`
- `timestamp` must be ISO 8601 format with UTC timezone (`+00:00`)
- NO nested objects or arrays in records
- Use `null` for missing prices, never omit fields

### Wayback Machine Integration
- Use CDX API with `collapse=timestamp:6` (monthly snapshots)
- Add 1-second delay between snapshot requests (`time.sleep(1)`)
- Handle HTTP errors gracefully (snapshots may be unavailable)
- Validate content size (skip if < 1000 bytes)
- **HTML Caching**: Save fetched HTML to `data/html_snapshot/<timestamp>.html`
  - Check cache before making HTTP requests
  - Load from cache if file exists
  - Save to cache on successful download

### Code Style
- Use type hints for all function signatures
- Keep parsing logic in `parse_pricing_data()` method
- Print progress to stderr, data to stdout/file
- Use `lxml` parser for BeautifulSoup
- Handle exceptions without crashing (log and continue)
- **Visual Icons**: Use emoji icons in progress messages for clarity
  - 🔍 Fetching snapshots
  - 📊 Snapshot count
  - ⏳ Processing snapshot
  - 💾 Cache operations
  - ✅ Success
  - ⚠️ Warning
  - ❌ Error
  - 📝 Final output

### Data Transformation
The `transform_to_records()` method must:
1. Accept list of historical snapshots (old format)
2. Flatten to one record per model per snapshot
3. Convert timestamps to ISO 8601
4. Report prices as-is WITHOUT conversion
5. Map `input_price_per_1k` → `input`, `output_price_per_1k` → `output`
6. Use `price_per_1k` as fallback for both input/output if separate prices not available
7. Extract `pricing_type` from model data (defaults to "per_1k_tokens" if not specified)

### Testing
- Test output schema with `tests/unit/io_schema.py`
- Verify all records are primitives (no nested structures)
- Confirm NO price conversion (values as-is from HTML)
- Check field presence (all 7 fields required)
- For integration tests use `--from-date 20260101`

### Project Structure
- **Source code**: `scrape_wayback.py` (main scraper)
- **Tests**: `tests/unit/io_schema.py` (output schema validation)
- **Data directory**: `data/` (gitignored)
  - `data/html_snapshot/` - cached HTML files
  - `data/output/` - generated JSON files
- **Output files**: Should be placed in `data/output/*.json`

## Legal & Data Considerations
- GPL-3.0 applies to **code only**, not scraped data
- Data belongs to OpenAI, subject to their terms
- Always include data disclaimer in README
- Tool is for informational/research purposes only
- No affiliation with or endorsement by OpenAI
- Test output schema with `test_transform.py`
- Verify all records are primitives (no nested structures)
- Check field presence (all 7 fields required)
- For integration tests use --from-date 20260101

## Don't Do
- ❌ Change output format (must be flat array)
- ❌ Use daily snapshots (`timestamp:8`) - too many requests
- ❌ Return nested structures or dictionaries of arrays
- ❌ Skip the 1-second delay between requests
- ❌ Add markdown/documentation files unless explicitly requested
- ❌ Make output argument optional (it's required)
- ❌ Remove HTML caching (improves performance and reduces load)
- ❌ Change cache directory from `data/html_snapshot/`
- ❌ Change output directory from `data/output/`

## When Adding Features
1. Maintain backward compatibility with output schema
2. Add new fields to schema only if absolutely necessary
3. Update `tests/unit/io_schema.py` if schema changes
4. Document changes in README.md
5. Keep scraper logic separate from transformation logic
