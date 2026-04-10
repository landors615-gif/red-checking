"""
Real Scraper — Xiaohongshu content extraction via headless browser.

STATUS: BLOCKED
Requires ALL of the following to be functional:
  1. playwright installed (pip install playwright && playwright install chromium)
  2. Chinese mainland proxy or direct network access to xiaohongshu.com
  3. XHS anti-bot headers/cookies handled (requires periodic cookie refresh)
  4. Note: XHS requires login for full data; public scraping is limited

Activation: SCRAPER_MODE=real python main.py
"""
from services.scraper_protocol import BaseScraper, ScrapedAccount, ScrapedPost
from typing import Optional
import os

# Raise immediately if someone tries to use it
_RAISE_ON_INIT = os.environ.get('SCRAPER_MODE', '').lower() == 'real'


class RealScraperBLOCKED(Exception):
    """Raised when RealScraper is instantiated without required setup."""
    pass


class RealScraper(BaseScraper):
    """
    Real Xiaohongshu scraper using Playwright.

    BLOCKED — not functional. See docstring above.
    """

    def __init__(self):
        if _RAISE_ON_INIT:
            raise RealScraperBLOCKED(
                "RealScraper is BLOCKED. Requirements:\n"
                "  1. pip install playwright && playwright install chromium\n"
                "  2. Chinese proxy/VPN to access xiaohongshu.com\n"
                "  3. Valid session cookies for full data access\n"
                "  4. Set SCRAPER_MODE=real to activate\n"
                "\n"
                "Until these are resolved, the app runs in SCRAPER_MODE=mock (default)."
            )

    async def scrape_account(self, note_id: str, url: str) -> ScrapedAccount:
        raise NotImplementedError("RealScraper is BLOCKED — use SCRAPER_MODE=mock")

    async def scrape_post(self, note_id: str, url: str) -> ScrapedPost:
        raise NotImplementedError("RealScraper is BLOCKED — use SCRAPER_MODE=mock")
