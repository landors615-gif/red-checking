"""
Mock Scraper — implements BaseScraper protocol.
Returns pre-defined fixture data simulating real XHS content.
Used when SCRAPER_MODE=mock (default).
"""
from services.scraper_protocol import BaseScraper, ScrapedAccount, ScrapedPost
import asyncio


class MockScraper(BaseScraper):
    """Returns canned fixture data — no network calls."""

    async def scrape_account(self, note_id: str, url: str) -> ScrapedAccount:
        await asyncio.sleep(0.05)  # tiny delay to simulate async
        return {
            "nickname": "美妆护肤实验室",
            "bio": "专注成分党测评 | 真实使用反馈 | 护肤干货分享\n📩合作请私信",
            "stats": {
                "followers": "12.8万",
                "following": 486,
                "likes_received": "98.6万",
                "posts_count": 328,
                "avg_likes": 3008,
                "avg_collects": 892,
                "avg_comments": 156,
            },
            "top_posts": [
                {"title": "这瓶精华液我用了28天，真实反馈来了", "cover": "https://placehold.co/600x400/pink/white?text=精华测评", "likes": 12800, "collects": 4200, "comments": 892},
                {"title": "油皮夏季控油指南｜10款产品横向对比", "cover": "https://placehold.co/600x400/orange/white?text=控油对比", "likes": 9600, "collects": 3100, "comments": 643},
                {"title": "早C晚A入门指南｜新手必看", "cover": "https://placehold.co/600x400/yellow/white?text=早C晚A", "likes": 8700, "collects": 2900, "comments": 521},
                {"title": "敏感肌修护红宝书｜皮肤科医生推荐", "cover": "https://placehold.co/600x400/red/white?text=敏感肌", "likes": 7400, "collects": 2600, "comments": 478},
            ],
        }

    async def scrape_post(self, note_id: str, url: str) -> ScrapedPost:
        await asyncio.sleep(0.05)
        return {
            "post_title": "这瓶精华液我用了28天，真实反馈来了",
            "published_at": "2026-03-28",
            "post_tags": ["精华液", "护肤测评", "成分党", "敏感肌", "早C晚A"],
            "stats": {
                "likes": 12800,
                "collects": 4200,
                "comments": 892,
                "shares": 1203,
                "cover": "https://placehold.co/600x400/pink/white?text=精华测评",
            },
            "top_posts": [
                {"title": "这瓶精华液我用了28天，真实反馈来了", "cover": "https://placehold.co/600x400/pink/white?text=精华测评", "likes": 12800, "collects": 4200, "comments": 892},
            ],
        }
