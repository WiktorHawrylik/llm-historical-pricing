

# 


# Scrapping historical data
 Only 2026 snapshots have content, everything before that is empty. This isn't a bug you introduced - the Wayback Machine simply couldn't capture JavaScript-rendered pages from OpenAI's old website architecture.

Your code is working exactly as designed. The issue is that historical snapshots from 2023-2025 don't contain pricing data because they relied on client-side JavaScript rendering.

Summary: The scraper is working correctly. The "no pricing data found" warnings are expected for older snapshots - they're JavaScript-rendered pages that Wayback Machine couldn't capture. Only 2026 snapshots have server-side rendered content that can be scraped.


- see latest snapshots