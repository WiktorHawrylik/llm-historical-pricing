# Issues

### Wayback Machine

- 2026 [OpenAI's pricing](https://platform.openai.com/docs/pricing) historical archives contain standard pricing data - 2026 snapshots have server-side rendered content that can be scraped. Example: [20260207123851](https://web.archive.org/web/20260207123851/https://platform.openai.com/docs/pricing)
- 2023-2025 [OpenAI's pricing](https://platform.openai.com/docs/pricing) historical archives don't contain standard pricing data - page was JavaScript-rendered during that period. The archived pages (examples in data/input/org_archive_web/com/openai/platform/docs/pricing) only contain empty shells (<div id="root"></div>) - the actual content was loaded client-side and couldn't be captured by internet archivers like Wayback Machine etc. Example: [20250802114943](https://web.archive.org/web/20250802114943/https://platform.openai.com/docs/pricing)