#!/usr/bin/env python3
"""
Unit tests for the Wayback Pricing Fetcher

These tests verify the basic functionality of the wayback_pricing module.
Note: These are offline tests that don't require internet access.
"""

import unittest
from datetime import datetime
from wayback_pricing import WaybackPricingFetcher


class TestWaybackPricingFetcher(unittest.TestCase):
    """Test cases for WaybackPricingFetcher class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.fetcher = WaybackPricingFetcher()
    
    def test_format_timestamp(self):
        """Test timestamp formatting."""
        timestamp = "20230315120000"
        formatted = self.fetcher._format_timestamp(timestamp)
        self.assertEqual(formatted, "2023-03-15")
    
    def test_wayback_url_format(self):
        """Test Wayback URL generation."""
        timestamp = "20230315120000"
        url = "https://platform.openai.com/docs/pricing"
        expected = f"https://web.archive.org/web/{timestamp}/{url}"
        actual = self.fetcher.WAYBACK_URL_FORMAT.format(
            timestamp=timestamp,
            url=url
        )
        self.assertEqual(actual, expected)
    
    def test_api_pricing_url(self):
        """Test API pricing URL constant."""
        self.assertEqual(
            self.fetcher.API_PRICING_URL,
            "https://platform.openai.com/docs/pricing"
        )
    
    def test_chatgpt_pricing_url(self):
        """Test ChatGPT pricing URL constant."""
        self.assertEqual(
            self.fetcher.CHATGPT_PRICING_URL,
            "https://openai.com/chatgpt/pricing"
        )
    
    def test_session_headers(self):
        """Test session has proper headers."""
        self.assertIn('User-Agent', self.fetcher.session.headers)
        self.assertTrue(
            'WaybackPricingFetcher' in 
            self.fetcher.session.headers['User-Agent']
        )


class TestWaybackURLs(unittest.TestCase):
    """Test URL construction and validation."""
    
    def test_cdx_api_url(self):
        """Test CDX API URL constant."""
        fetcher = WaybackPricingFetcher()
        self.assertEqual(
            fetcher.WAYBACK_CDX_API,
            "https://web.archive.org/cdx/search/cdx"
        )
    
    def test_wayback_url_structure(self):
        """Test Wayback URL structure."""
        fetcher = WaybackPricingFetcher()
        url_format = fetcher.WAYBACK_URL_FORMAT
        self.assertIn('web.archive.org', url_format)
        self.assertIn('{timestamp}', url_format)
        self.assertIn('{url}', url_format)


class TestDateHandling(unittest.TestCase):
    """Test date-related functionality."""
    
    def test_format_timestamp_with_time(self):
        """Test timestamp formatting with time component."""
        fetcher = WaybackPricingFetcher()
        timestamp = "20221130235959"
        formatted = fetcher._format_timestamp(timestamp)
        self.assertEqual(formatted, "2022-11-30")
    
    def test_format_timestamp_invalid(self):
        """Test timestamp formatting with invalid input."""
        fetcher = WaybackPricingFetcher()
        timestamp = "invalid"
        formatted = fetcher._format_timestamp(timestamp)
        # Should return original timestamp if parsing fails
        self.assertEqual(formatted, timestamp)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestWaybackPricingFetcher))
    suite.addTests(loader.loadTestsFromTestCase(TestWaybackURLs))
    suite.addTests(loader.loadTestsFromTestCase(TestDateHandling))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    import sys
    sys.exit(run_tests())
