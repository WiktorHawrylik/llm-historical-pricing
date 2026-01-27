#!/usr/bin/env python3
"""
Demo Script: Wayback Machine Pricing Fetcher

This script demonstrates the complete functionality of the wayback_pricing module
by showing how to retrieve and display historical OpenAI pricing data.

This is a standalone demo that can be run to understand the tool's capabilities.
"""

from wayback_pricing import WaybackPricingFetcher
from datetime import datetime


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def demo_basic_usage():
    """Demonstrate basic usage of the WaybackPricingFetcher."""
    print_header("DEMO: Basic Wayback Machine Pricing Fetcher")
    
    print("This tool allows you to access historical OpenAI pricing data from")
    print("the Internet Archive's Wayback Machine.\n")
    
    print("🔧 Initializing fetcher...")
    fetcher = WaybackPricingFetcher()
    
    print("✓ Ready to fetch historical pricing data!\n")
    
    # Show available URLs
    print("📋 Available pricing pages:")
    print(f"  1. API Pricing: {fetcher.API_PRICING_URL}")
    print(f"  2. ChatGPT Pricing: {fetcher.CHATGPT_PRICING_URL}")
    
    return fetcher


def demo_list_snapshots(fetcher):
    """Demonstrate listing available snapshots."""
    print_header("DEMO: Listing Available Snapshots")
    
    print("Searching for API pricing snapshots from Nov 2022 to Mar 2023...")
    print("(This covers the period around ChatGPT's launch)\n")
    
    # Note: This will fail without internet, but shows the API
    print("📡 Querying Wayback Machine CDX API...")
    print("   API Endpoint: " + fetcher.WAYBACK_CDX_API)
    print("   Filter: statuscode:200 (successful captures only)")
    print("   Collapse: Daily snapshots\n")
    
    print("Expected output format:")
    print("-" * 70)
    print("Date: 2022-11-30")
    print("  Wayback URL: https://web.archive.org/web/20221130.../pricing")
    print()
    print("Date: 2022-12-15")
    print("  Wayback URL: https://web.archive.org/web/20221215.../pricing")
    print("-" * 70)
    print()
    print("💡 Each URL can be opened in a browser to view the archived page")


def demo_get_snapshot(fetcher):
    """Demonstrate getting a specific snapshot."""
    print_header("DEMO: Getting a Specific Snapshot")
    
    print("Looking for API pricing snapshot from March 15, 2023...\n")
    
    print("🔍 Search process:")
    print("  1. Query CDX API for exact date")
    print("  2. If not found, search ±7 days")
    print("  3. Return closest available snapshot\n")
    
    print("Expected output format:")
    print("-" * 70)
    print("Found snapshot:")
    print("Date: 2023-03-15")
    print("Wayback URL: https://web.archive.org/web/20230315120000/...")
    print("-" * 70)
    print()
    print("💡 The Wayback URL contains:")
    print("   - Timestamp: YYYYMMDDhhmmss")
    print("   - Original URL: The page that was archived")


def demo_comparison():
    """Demonstrate comparing pricing over time."""
    print_header("DEMO: Comparing Pricing Over Time")
    
    print("To compare pricing across different dates, you can:")
    print()
    print("1️⃣  Get snapshots from multiple dates:")
    print("   - November 2022 (ChatGPT launch)")
    print("   - March 2023 (GPT-4 announcement)")
    print("   - September 2023 (Later in the year)")
    print()
    print("2️⃣  Open each Wayback URL in browser tabs")
    print()
    print("3️⃣  Compare pricing side-by-side:")
    print("   - GPT-3.5 Turbo pricing changes")
    print("   - GPT-4 pricing introduction")
    print("   - API rate changes")
    print()
    print("💡 This gives you the exact pricing as it appeared on those dates")


def demo_cli_usage():
    """Demonstrate CLI usage."""
    print_header("DEMO: Command Line Usage")
    
    print("You can use this tool from the command line:\n")
    
    print("📝 List snapshots:")
    print("   $ python wayback_pricing.py list --url api --limit 5")
    print()
    
    print("📝 Get specific snapshot:")
    print("   $ python wayback_pricing.py get --url api --date 20230315")
    print()
    
    print("📝 Custom date range:")
    print("   $ python wayback_pricing.py list --url chatgpt \\")
    print("       --start-date 20221101 --end-date 20231231")
    print()
    
    print("💡 Use --help for more options:")
    print("   $ python wayback_pricing.py --help")


def demo_programmatic_usage():
    """Demonstrate programmatic usage."""
    print_header("DEMO: Programmatic Usage (Python API)")
    
    print("You can also use the module in your Python scripts:\n")
    
    code = """
from wayback_pricing import WaybackPricingFetcher

# Initialize
fetcher = WaybackPricingFetcher()

# List snapshots
snapshots = fetcher.list_snapshots(
    url=fetcher.API_PRICING_URL,
    start_date="20221101",
    end_date="20231231",
    limit=10
)

# Process snapshots
for snapshot in snapshots:
    print(f"Date: {snapshot['date']}")
    print(f"URL: {snapshot['wayback_url']}")
    
# Get specific snapshot
snapshot = fetcher.get_snapshot(
    url=fetcher.API_PRICING_URL,
    date="20230315"
)

# Fetch content (optional)
if snapshot:
    content = fetcher.fetch_content(snapshot['wayback_url'])
    print(f"Page size: {len(content)} bytes")
"""
    
    print("Example code:")
    print("-" * 70)
    print(code)
    print("-" * 70)


def demo_use_cases():
    """Show practical use cases."""
    print_header("DEMO: Real-World Use Cases")
    
    print("Here are some practical ways to use this tool:\n")
    
    print("📊 1. COST ANALYSIS")
    print("   - Track how API pricing has changed over time")
    print("   - Calculate cost impact on existing applications")
    print("   - Plan budgets based on historical trends")
    print()
    
    print("📈 2. RESEARCH & REPORTING")
    print("   - Create charts showing pricing evolution")
    print("   - Compare OpenAI pricing with competitors")
    print("   - Document pricing for academic papers")
    print()
    
    print("🔍 3. BILLING VERIFICATION")
    print("   - Verify you were charged correct historical rates")
    print("   - Check when pricing changes took effect")
    print("   - Audit past invoices")
    print()
    
    print("📚 4. DOCUMENTATION")
    print("   - Reference exact pricing for specific dates")
    print("   - Archive pricing for compliance")
    print("   - Create historical records")


def main():
    """Run all demos."""
    print("\n" + "🚀" * 35)
    print("     WAYBACK MACHINE PRICING FETCHER - COMPLETE DEMO")
    print("🚀" * 35)
    
    print("\nThis demo shows all features of the wayback_pricing tool.")
    print("Note: Some features require internet access to web.archive.org\n")
    
    # Run demos
    fetcher = demo_basic_usage()
    demo_list_snapshots(fetcher)
    demo_get_snapshot(fetcher)
    demo_comparison()
    demo_cli_usage()
    demo_programmatic_usage()
    demo_use_cases()
    
    # Final message
    print_header("Demo Complete!")
    
    print("Next steps:")
    print("  1. Run: python wayback_pricing.py list --url api --limit 5")
    print("  2. Open a Wayback URL in your browser")
    print("  3. Explore the archived pricing pages")
    print("  4. Try the examples in examples.py")
    print()
    print("For more information:")
    print("  - Read README.md for full documentation")
    print("  - Check QUICK_REFERENCE.md for command syntax")
    print("  - See CONTRIBUTING.md to contribute")
    print()
    print("Happy exploring! 🎉")
    print("\n" + "=" * 70 + "\n")


if __name__ == '__main__':
    main()
