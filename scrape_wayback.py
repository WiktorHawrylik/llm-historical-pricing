#!/usr/bin/env python3
"""
Scrape historical OpenAI pricing data from the Wayback Machine.

This script fetches archived snapshots of OpenAI pricing pages and extracts
pricing information to create a historical pricing database.
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup


class WaybackScraper:
    """Scraper for OpenAI pricing data from Wayback Machine."""
    
    WAYBACK_API = "https://web.archive.org/cdx/search/cdx"
    WAYBACK_URL = "https://web.archive.org/web/{timestamp}/{url}"
    
    PRICING_URLS = [
        "https://platform.openai.com/docs/pricing",
    ]
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def get_snapshots(self, url: str, from_date: str = "20221101") -> List[Dict]:
        """
        Get available snapshots for a URL from Wayback Machine.
        
        Args:
            url: The URL to search for
            from_date: Start date in YYYYMMDD format (default: Nov 1, 2022)
        
        Returns:
            List of snapshot dictionaries with timestamp and original URL
        """
        params = {
            'url': url,
            'from': from_date,
            'output': 'json',
            'fl': 'timestamp,original',
            'filter': 'statuscode:200',
            'collapse': 'timestamp:6',  # One snapshot per month
        }
        
        try:
            response = self.session.get(self.WAYBACK_API, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Skip header row
            if len(data) > 1:
                headers = data[0]
                snapshots = []
                for row in data[1:]:
                    snapshot = dict(zip(headers, row))
                    snapshots.append(snapshot)
                return snapshots
            return []
        except Exception as e:
            print(f"Error fetching snapshots for {url}: {e}", file=sys.stderr)
            return []
    
    def fetch_snapshot_content(self, timestamp: str, url: str) -> Optional[str]:
        """
        Fetch the content of a specific snapshot.
        
        Args:
            timestamp: Wayback Machine timestamp
            url: Original URL
        
        Returns:
            HTML content or None if fetch fails
        """
        wayback_url = self.WAYBACK_URL.format(timestamp=timestamp, url=url)
        
        try:
            response = self.session.get(wayback_url, timeout=30)
            response.raise_for_status()
            
            # Check if we got actual content (not an error page)
            if len(response.text) < 1000:
                print(f"Warning: Snapshot content seems too small, may be broken", file=sys.stderr)
                return None
                
            return response.text
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error {e.response.status_code}: Snapshot not available", file=sys.stderr)
            return None
        except requests.exceptions.Timeout:
            print(f"Timeout: Snapshot took too long to fetch", file=sys.stderr)
            return None
        except Exception as e:
            print(f"Error fetching snapshot: {e}", file=sys.stderr)
            return None
    
    def parse_pricing_data(self, html: str, timestamp: str, source_url: str) -> Optional[Dict]:
        """
        Parse pricing data from HTML content.
        
        Args:
            html: HTML content from snapshot
            timestamp: Wayback Machine timestamp
            source_url: Original URL
        
        Returns:
            Dictionary with pricing data or None if parsing fails
        """
        soup = BeautifulSoup(html, 'lxml')
        
        # Convert timestamp to readable date
        try:
            dt = datetime.strptime(timestamp, '%Y%m%d%H%M%S')
            date_str = dt.strftime('%Y-%m-%d')
        except ValueError:
            date_str = timestamp
        
        pricing_data = {
            'date': date_str,
            'timestamp': timestamp,
            'source_url': source_url,
            'models': []
        }
        
        # Extract pricing information based on page structure
        # This parser handles different page layouts across different time periods
        
        # Method 1: Look for pricing tables
        for table in soup.find_all('table'):
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    cell_texts = [cell.get_text(strip=True) for cell in cells]
                    
                    # Check if this row contains a model name
                    model_name = None
                    for i, text in enumerate(cell_texts):
                        if any(keyword in text.lower() for keyword in 
                               ['gpt-4', 'gpt-3.5', 'gpt-3', 'davinci', 'curie', 
                                'babbage', 'ada', 'turbo', 'claude', 'embedding']):
                            model_name = text
                            
                            # Try to find pricing in subsequent cells
                            model_info = {'name': model_name}
                            
                            # Look for price patterns in remaining cells
                            for j in range(i + 1, len(cell_texts)):
                                price_text = cell_texts[j]
                                # Match patterns like $0.002, 0.002, 5, $10, etc.
                                price_match = re.search(r'\$?(\d+(?:\.\d+)?)', price_text)
                                if price_match:
                                    price_value = float(price_match.group(1))
                                    
                                    # Determine if it's input or output pricing
                                    if 'input' in price_text.lower():
                                        model_info['input_price_per_1k'] = price_value
                                    elif 'output' in price_text.lower():
                                        model_info['output_price_per_1k'] = price_value
                                    else:
                                        model_info['price_per_1k'] = price_value
                            
                            if len(model_info) > 1:  # Has name and at least one price
                                pricing_data['models'].append(model_info)
                            break
        
        # Method 2: Look for structured divs/sections
        # Common patterns in OpenAI pricing pages
        for section in soup.find_all(['div', 'section'], class_=re.compile(r'pricing|model|price')):
            section_text = section.get_text()
            
            # Look for model names followed by prices
            lines = [line.strip() for line in section_text.split('\n') if line.strip()]
            
            for i, line in enumerate(lines):
                if any(keyword in line.lower() for keyword in 
                       ['gpt-4', 'gpt-3.5', 'gpt-3', 'turbo']):
                    model_info = {'name': line}
                    
                    # Check next few lines for pricing
                    for j in range(i + 1, min(i + 5, len(lines))):
                        price_match = re.search(r'\$?(\d+(?:\.\d+)?)', lines[j])
                        if price_match:
                            price_value = float(price_match.group(1))
                            if 'input' in lines[j].lower():
                                model_info['input_price_per_1k'] = price_value
                            elif 'output' in lines[j].lower():
                                model_info['output_price_per_1k'] = price_value
                            else:
                                model_info['price_per_1k'] = price_value
                    
                    if len(model_info) > 1:
                        pricing_data['models'].append(model_info)
        
        # Return data if we found any pricing information
        if pricing_data['models']:
            return pricing_data
        
        # Last resort: check if the page even mentions pricing
        text_content = soup.get_text().lower()
        if 'pricing' in text_content or 'price' in text_content:
            # Return minimal data to indicate a pricing page was found
            return pricing_data
        
        return None
    
    def scrape_all(self, from_date: str = "20221101") -> List[Dict]:
        """
        Scrape all available pricing data from Wayback Machine.
        
        Args:
            from_date: Start date in YYYYMMDD format
        
        Returns:
            List of pricing data dictionaries
        """
        all_pricing_data = []
        
        for url in self.PRICING_URLS:
            print(f"Fetching snapshots for {url}...", file=sys.stderr)
            snapshots = self.get_snapshots(url, from_date=from_date)
            print(f"Found {len(snapshots)} snapshots", file=sys.stderr)
            
            for i, snapshot in enumerate(snapshots, 1):
                timestamp = snapshot['timestamp']
                wayback_url = self.WAYBACK_URL.format(timestamp=timestamp, url=url)
                print(f"Processing snapshot {i}/{len(snapshots)}: {timestamp} - {wayback_url}", file=sys.stderr)
                
                html = self.fetch_snapshot_content(timestamp, url)
                if html:
                    pricing_data = self.parse_pricing_data(html, timestamp, url)
                    if pricing_data:
                        all_pricing_data.append(pricing_data)
                        print(f"✓ Successfully extracted pricing data", file=sys.stderr)
                    else:
                        print(f"✗ No pricing data found in snapshot", file=sys.stderr)
                else:
                    print(f"✗ Failed to fetch snapshot", file=sys.stderr)
                
                # Add 1 second delay between requests to respect rate limits
                if i < len(snapshots):
                    time.sleep(1)
        
        # Sort by date
        all_pricing_data.sort(key=lambda x: x['timestamp'])
        
        return all_pricing_data
    
    def transform_to_records(self, pricing_data: Dict, category: str = "language_model") -> List[Dict]:
        """
        Transform pricing data to flat record format.
        
        Args:
            pricing_data: Original pricing data structure
            category: Model category (default: language_model)
        
        Returns:
            List of flat records
        """
        records = []
        
        for snapshot in pricing_data:
            date_str = snapshot['date']
            timestamp_str = snapshot['timestamp']
            
            # Convert timestamp to ISO format
            try:
                dt = datetime.strptime(timestamp_str, '%Y%m%d%H%M%S')
                iso_timestamp = dt.isoformat() + '+00:00'
            except ValueError:
                iso_timestamp = datetime.now().isoformat() + '+00:00'
            
            for model in snapshot['models']:
                # Convert prices from per_1k to per_1m tokens (multiply by 1000)
                input_price_1k = model.get('input_price_per_1k') or model.get('price_per_1k')
                output_price_1k = model.get('output_price_per_1k') or model.get('price_per_1k')
                cached_input_price_1k = model.get('cached_input_price_per_1k')
                
                record = {
                    'model': model['name'],
                    'pricing_type': 'per_1m_tokens',
                    'category': category,
                    'timestamp': iso_timestamp,
                    'input': input_price_1k * 1000 if input_price_1k is not None else None,
                    'cached_input': cached_input_price_1k * 1000 if cached_input_price_1k is not None else None,
                    'output': output_price_1k * 1000 if output_price_1k is not None else None
                }
                records.append(record)
        
        return records


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Scrape historical OpenAI pricing data from Wayback Machine'
    )
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output JSON file path (must end with .json)'
    )
    parser.add_argument(
        '--from-date',
        default='20221101',
        help='Start date in YYYYMMDD format (default: 20221101)'
    )
    
    args = parser.parse_args()
    
    # Validate output is a JSON file
    if not args.output.endswith('.json'):
        parser.error('Output file must end with .json')
    
    scraper = WaybackScraper()
    
    pricing_history = scraper.scrape_all(from_date=args.from_date)
    
    # Transform to flat records format
    records = scraper.transform_to_records(pricing_history, category='language_model')
    
    # Create output directory if needed
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # Write flat array of records
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    
    print(f"\nSuccessfully scraped {len(pricing_history)} pricing snapshots", file=sys.stderr)
    print(f"Written {len(records)} records to {args.output}", file=sys.stderr)


if __name__ == '__main__':
    main()
