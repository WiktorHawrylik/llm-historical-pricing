#!/usr/bin/env python3
"""
Wayback Machine OpenAI Pricing Scraper

This script fetches historical pricing data for OpenAI from the Internet Archive's
Wayback Machine. It allows you to:
- List available snapshots for OpenAI pricing pages
- Fetch archived pricing pages from specific dates
- Compare pricing over time

Usage:
    python wayback_pricing.py list --url <pricing_url>
    python wayback_pricing.py get --url <pricing_url> --date <YYYYMMDD>
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional

import requests


class WaybackPricingFetcher:
    """Fetches historical pricing data from the Wayback Machine."""
    
    WAYBACK_CDX_API = "https://web.archive.org/cdx/search/cdx"
    WAYBACK_URL_FORMAT = "https://web.archive.org/web/{timestamp}/{url}"
    
    # OpenAI pricing URLs
    API_PRICING_URL = "https://platform.openai.com/docs/pricing"
    CHATGPT_PRICING_URL = "https://openai.com/chatgpt/pricing"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; WaybackPricingFetcher/1.0)'
        })
    
    def list_snapshots(
        self,
        url: str,
        start_date: Optional[str] = "20221101",
        end_date: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, str]]:
        """
        List available snapshots for a given URL in the Wayback Machine.
        
        Args:
            url: The URL to search for
            start_date: Start date in YYYYMMDD format (default: Nov 1, 2022)
            end_date: End date in YYYYMMDD format (default: today)
            limit: Maximum number of snapshots to return
            
        Returns:
            List of snapshots with timestamp and URL information
        """
        if end_date is None:
            end_date = datetime.now().strftime("%Y%m%d")
        
        params = {
            'url': url,
            'from': start_date,
            'to': end_date,
            'output': 'json',
            'fl': 'timestamp,statuscode,original',
            'filter': 'statuscode:200',
            'collapse': 'timestamp:8'  # Collapse to daily snapshots
        }
        
        try:
            response = self.session.get(self.WAYBACK_CDX_API, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Skip header row
            if not data or len(data) < 2:
                return []
            
            snapshots = []
            for row in data[1:]:
                if len(row) >= 3:
                    timestamp, statuscode, original = row[0], row[1], row[2]
                    snapshots.append({
                        'timestamp': timestamp,
                        'date': self._format_timestamp(timestamp),
                        'wayback_url': self.WAYBACK_URL_FORMAT.format(
                            timestamp=timestamp,
                            url=original
                        ),
                        'original_url': original
                    })
            
            if limit:
                snapshots = snapshots[:limit]
            
            return snapshots
            
        except requests.RequestException as e:
            print(f"Error fetching snapshots: {e}", file=sys.stderr)
            return []
    
    def get_snapshot(self, url: str, date: str) -> Optional[Dict[str, str]]:
        """
        Get the closest snapshot for a given URL and date.
        
        Args:
            url: The URL to search for
            date: Date in YYYYMMDD format
            
        Returns:
            Snapshot information including the wayback URL
        """
        snapshots = self.list_snapshots(url, start_date=date, end_date=date, limit=1)
        
        if not snapshots:
            # Try to find nearest snapshot within a week
            start_date = datetime.strptime(date, "%Y%m%d")
            for days_offset in range(1, 8):
                # Try before
                before_date = (start_date - timedelta(days=days_offset)).strftime("%Y%m%d")
                snapshots = self.list_snapshots(url, start_date=before_date, end_date=before_date, limit=1)
                if snapshots:
                    return snapshots[0]
                
                # Try after
                after_date = (start_date + timedelta(days=days_offset)).strftime("%Y%m%d")
                snapshots = self.list_snapshots(url, start_date=after_date, end_date=after_date, limit=1)
                if snapshots:
                    return snapshots[0]
        
        return snapshots[0] if snapshots else None
    
    def fetch_content(self, wayback_url: str) -> Optional[str]:
        """
        Fetch the actual content from a Wayback Machine URL.
        
        Args:
            wayback_url: The Wayback Machine URL to fetch
            
        Returns:
            The HTML content of the archived page
        """
        try:
            response = self.session.get(wayback_url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching content: {e}", file=sys.stderr)
            return None
    
    @staticmethod
    def _format_timestamp(timestamp: str) -> str:
        """Format a Wayback timestamp (YYYYMMDDhhmmss) to a readable date."""
        try:
            dt = datetime.strptime(timestamp[:8], "%Y%m%d")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            return timestamp


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Fetch historical OpenAI pricing data from the Wayback Machine"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List available snapshots')
    list_parser.add_argument(
        '--url',
        choices=['api', 'chatgpt'],
        default='api',
        help='Pricing page to query (api or chatgpt)'
    )
    list_parser.add_argument(
        '--start-date',
        default='20221101',
        help='Start date in YYYYMMDD format (default: 20221101)'
    )
    list_parser.add_argument(
        '--end-date',
        help='End date in YYYYMMDD format (default: today)'
    )
    list_parser.add_argument(
        '--limit',
        type=int,
        help='Maximum number of snapshots to return'
    )
    
    # Get command
    get_parser = subparsers.add_parser('get', help='Get a specific snapshot')
    get_parser.add_argument(
        '--url',
        choices=['api', 'chatgpt'],
        default='api',
        help='Pricing page to query (api or chatgpt)'
    )
    get_parser.add_argument(
        '--date',
        required=True,
        help='Date in YYYYMMDD format'
    )
    get_parser.add_argument(
        '--fetch-content',
        action='store_true',
        help='Fetch the actual HTML content (warning: can be large)'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Map URL choice to actual URL
    url_map = {
        'api': WaybackPricingFetcher.API_PRICING_URL,
        'chatgpt': WaybackPricingFetcher.CHATGPT_PRICING_URL
    }
    
    fetcher = WaybackPricingFetcher()
    
    if args.command == 'list':
        target_url = url_map[args.url]
        print(f"Fetching snapshots for: {target_url}")
        print(f"Date range: {args.start_date} to {args.end_date or 'today'}")
        print()
        
        snapshots = fetcher.list_snapshots(
            target_url,
            start_date=args.start_date,
            end_date=args.end_date,
            limit=args.limit
        )
        
        if not snapshots:
            print("No snapshots found.")
            return 1
        
        print(f"Found {len(snapshots)} snapshots:\n")
        for snapshot in snapshots:
            print(f"Date: {snapshot['date']}")
            print(f"  Wayback URL: {snapshot['wayback_url']}")
            print()
        
        return 0
    
    elif args.command == 'get':
        target_url = url_map[args.url]
        print(f"Fetching snapshot for: {target_url}")
        print(f"Date: {args.date}")
        print()
        
        snapshot = fetcher.get_snapshot(target_url, args.date)
        
        if not snapshot:
            print("No snapshot found for the specified date.")
            return 1
        
        print(f"Found snapshot:")
        print(f"Date: {snapshot['date']}")
        print(f"Wayback URL: {snapshot['wayback_url']}")
        print()
        
        if args.fetch_content:
            print("Fetching content...")
            content = fetcher.fetch_content(snapshot['wayback_url'])
            if content:
                print(f"Content length: {len(content)} characters")
                print("\nTo view the page, open the Wayback URL in your browser:")
                print(snapshot['wayback_url'])
            else:
                print("Failed to fetch content.")
                return 1
        
        return 0
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
