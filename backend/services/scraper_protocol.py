"""
Scraper Protocol — defines the interface for XHS content extraction.
Used by task_store.py; swap scraper implementation via SCRAPER_MODE env var.

Modes:
  mock    — returns MOCK_SCRAPED_DATA (default, no network required)
  real    — uses Playwright-based scraper (requires headless browser + network)

To activate real mode:
  SCRAPER_MODE=real python main.py

Real scraper status:
  BLOCKED — requires: playwright installed, browser drivers, proxy/VPN to CN.
  The real scraper is NOT yet functional; this stub exists to define the contract.
"""
from abc import ABC, abstractmethod
from typing import Literal


class InputType:
    ACCOUNT = 'account'
    POST = 'post'


ScrapedAccount = dict  # {
  # "nickname": str,
  # "bio": str,
  # "stats": { "followers": str, "following": int, "likes_received": str, "posts_count": int,
  #            "avg_likes": int, "avg_collects": int, "avg_comments": int },
  # "top_posts": [{"title": str, "cover": str, "likes": int, "collects": int, "comments": int}, ...],
# }

ScrapedPost = dict  # {
  # "post_title": str,
  # "published_at": str,
  # "post_tags": list[str],
  # "stats": { "likes": int, "collects": int, "comments": int, "shares": int, "cover": str },
  # "top_posts": [...same as above, single-item list],
# }


class BaseScraper(ABC):
    """Abstract scraper interface."""

    @abstractmethod
    async def scrape_account(self, note_id: str, url: str) -> ScrapedAccount:
        """Fetch raw account data from a Xiaohongshu profile page."""
        ...

    @abstractmethod
    async def scrape_post(self, note_id: str, url: str) -> ScrapedPost:
        """Fetch raw post data from a Xiaohongshu note page."""
        ...


# ── Registry ──────────────────────────────────────────────────────

def get_scraper() -> BaseScraper:
    import os
    mode = os.environ.get('SCRAPER_MODE', 'mock').lower()
    if mode == 'real':
        # Real scraper — activated when XHS is accessible
        from services.real_scraper import RealScraper
        return RealScraper()
    # Default: mock scraper
    from services.mock_scraper import MockScraper
    return MockScraper()
