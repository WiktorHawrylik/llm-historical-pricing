#!/usr/bin/env python3
"""
Example usage of the Wayback Pricing Fetcher

This script demonstrates how to use the WaybackPricingFetcher class
to retrieve historical OpenAI pricing data.
"""

from wayback_pricing import WaybackPricingFetcher


def example_list_snapshots():
    """Example: List available snapshots for API pricing."""
    print("=" * 60)
    print("Example 1: List API Pricing Snapshots")
    print("=" * 60)
    
    fetcher = WaybackPricingFetcher()
    
    # List snapshots from late 2022 to early 2023
    snapshots = fetcher.list_snapshots(
        url=WaybackPricingFetcher.API_PRICING_URL,
        start_date="20221101",
        end_date="20230331",
        limit=10
    )
    
    if snapshots:
        print(f"\nFound {len(snapshots)} snapshots:\n")
        for snapshot in snapshots:
            print(f"Date: {snapshot['date']}")
            print(f"  Wayback URL: {snapshot['wayback_url']}")
            print()
    else:
        print("\nNo snapshots found.")
    
    return snapshots


def example_get_specific_snapshot():
    """Example: Get a specific snapshot from March 2023."""
    print("\n" + "=" * 60)
    print("Example 2: Get Specific Snapshot (March 2023)")
    print("=" * 60)
    
    fetcher = WaybackPricingFetcher()
    
    # Get snapshot from March 15, 2023
    snapshot = fetcher.get_snapshot(
        url=WaybackPricingFetcher.API_PRICING_URL,
        date="20230315"
    )
    
    if snapshot:
        print(f"\nFound snapshot:")
        print(f"Date: {snapshot['date']}")
        print(f"Wayback URL: {snapshot['wayback_url']}")
        print(f"\nYou can view this snapshot in your browser at:")
        print(snapshot['wayback_url'])
    else:
        print("\nNo snapshot found for the specified date.")
    
    return snapshot


def example_compare_pricing():
    """Example: Compare pricing between two time periods."""
    print("\n" + "=" * 60)
    print("Example 3: Compare Pricing Over Time")
    print("=" * 60)
    
    fetcher = WaybackPricingFetcher()
    
    # Get snapshots from different periods
    dates = ["20221130", "20230315", "20230901"]
    
    print("\nFetching snapshots from different time periods...\n")
    
    for date in dates:
        snapshot = fetcher.get_snapshot(
            url=WaybackPricingFetcher.API_PRICING_URL,
            date=date
        )
        
        if snapshot:
            print(f"Date: {snapshot['date']}")
            print(f"  URL: {snapshot['wayback_url']}")
        else:
            print(f"Date: {date} - No snapshot found")
    
    print("\nNote: Open these URLs in your browser to manually compare pricing.")


def example_chatgpt_pricing():
    """Example: Get ChatGPT subscription pricing snapshots."""
    print("\n" + "=" * 60)
    print("Example 4: ChatGPT Subscription Pricing")
    print("=" * 60)
    
    fetcher = WaybackPricingFetcher()
    
    # List ChatGPT pricing snapshots
    snapshots = fetcher.list_snapshots(
        url=WaybackPricingFetcher.CHATGPT_PRICING_URL,
        start_date="20221101",
        end_date="20230630",
        limit=5
    )
    
    if snapshots:
        print(f"\nFound {len(snapshots)} ChatGPT pricing snapshots:\n")
        for snapshot in snapshots:
            print(f"Date: {snapshot['date']}")
            print(f"  Wayback URL: {snapshot['wayback_url']}")
            print()
    else:
        print("\nNo snapshots found.")
    
    return snapshots


def main():
    """Run all examples."""
    print("\nWayback Machine OpenAI Pricing Fetcher - Examples\n")
    print("These examples demonstrate how to use the tool to retrieve")
    print("historical pricing data from the Internet Archive.\n")
    
    try:
        # Run examples
        example_list_snapshots()
        example_get_specific_snapshot()
        example_compare_pricing()
        example_chatgpt_pricing()
        
        print("\n" + "=" * 60)
        print("Examples completed!")
        print("=" * 60)
        print("\nNote: Internet access is required for these examples to work.")
        print("The Wayback Machine API will be queried to fetch snapshot data.")
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        print("\nMake sure you have:")
        print("1. Installed all dependencies (pip install -r requirements.txt)")
        print("2. Internet access to reach web.archive.org")
        return 1
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
