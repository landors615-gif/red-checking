"""
Real Scraper — Xiaohongshu content extraction via HTTP API + HTML parsing.

STATUS: PARTIALLY FUNCTIONAL
- XHS is accessible from this network (HTTP 200 confirmed)
- XHS uses client-side rendering (SPA); raw HTML doesn't contain structured data
- Internal API endpoints require login cookies/session tokens
- Anti-bot measures block unauthenticated API access

WHAT WORKS:
- HTTP requests to xiaohongshu.com succeed (network is open)
- The scraper attempts real requests and gracefully degrades when blocked

WHAT IS BLOCKED:
- Profile data requires login (cookies needed)
- Note content requires login
- Full data access needs valid session

Activation: SCRAPER_MODE=real python main.py
Set XHS_COOKIES env var for authenticated requests (format: key=value; key2=value2)
"""
from services.scraper_protocol import BaseScraper, ScrapedAccount, ScrapedPost
from typing import Optional
import asyncio
import os
import re
import json


class RealScraper(BaseScraper):
    """
    Real Xiaohongshu scraper using HTTP requests.

    Attempts:
      1. Public XHS API endpoints (no auth - will 406 without cookies)
      2. Web scraping with cookie injection
      3. Graceful degradation to mock data with real network verification

    Status: PARTIAL - real HTTP requests are made, but XHS blocks data without auth.
    The scraper will return whatever it can get and log what's blocked.
    """

    def __init__(self):
        self.cookies = self._parse_cookies()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://www.xiaohongshu.com/',
            'Origin': 'https://www.xiaohongshu.com',
        }
        self._network_verified = False

    def _parse_cookies(self) -> dict:
        """Parse XHS_COOKIES env var into dict."""
        cookies_str = os.environ.get('XHS_COOKIES', '')
        if not cookies_str:
            return {}
        cookies = {}
        for part in cookies_str.split(';'):
            part = part.strip()
            if '=' in part:
                key, val = part.split('=', 1)
                cookies[key.strip()] = val.strip()
        return cookies

    async def scrape_account(self, note_id: str, url: str) -> ScrapedAccount:
        """
        Attempt to scrape XHS account data via real HTTP.
        
        Returns real data if auth cookies are valid and XHS allows access.
        Falls back to minimal real-like data if blocked (with network verification).
        """
        import httpx

        # First: verify network is actually working
        if not self._network_verified:
            try:
                async with httpx.AsyncClient(timeout=5) as client:
                    resp = await client.get('https://www.xiaohongshu.com', headers=self.headers)
                    self._network_verified = resp.status_code == 200
                    print(f"[RealScraper] Network verified: {self._network_verified}, status={resp.status_code}")
            except Exception as e:
                print(f"[RealScraper] Network verification failed: {e}")
                self._network_verified = False

        # Try account data API (requires auth)
        account_data = await self._try_fetch_account(note_id)
        if account_data:
            print(f"[RealScraper] Got real account data for {note_id}")
            return account_data

        # Return data with real network info + realistic mock
        print(f"[RealScraper] Falling back to enhanced mock for {note_id} (XHS requires login for full data)")
        return await self._enhanced_mock_account(note_id, url)

    async def scrape_post(self, note_id: str, url: str) -> ScrapedPost:
        """Attempt to scrape XHS post data via real HTTP."""
        import httpx

        # Strategy 1: SSR page scraping (works when xsec_token is in URL)
        post_data = await self._try_ssr_scrape_post(note_id, url)
        if post_data:
            print(f"[RealScraper] Got real post data via SSR for {note_id}")
            return post_data

        # Strategy 2: API endpoints (usually blocked without full auth)
        post_data = await self._try_fetch_post(note_id)
        if post_data:
            print(f"[RealScraper] Got real post data via API for {note_id}")
            return post_data

        print(f"[RealScraper] Falling back to enhanced mock for post {note_id}")
        return await self._enhanced_mock_post(note_id, url)

    async def _try_ssr_scrape_post(self, note_id: str, url: str) -> Optional[ScrapedPost]:
        """Scrape post data from SSR __INITIAL_STATE__ in the HTML page.
        
        XHS returns server-rendered data when xsec_token is present in the URL.
        """
        import httpx

        try:
            async with httpx.AsyncClient(timeout=15, follow_redirects=True, cookies=self.cookies) as client:
                resp = await client.get(url, headers=self.headers)
                if resp.status_code != 200:
                    print(f"[RealScraper] SSR page returned {resp.status_code}")
                    return None

                html = resp.text
                m = re.search(r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\})\s*</script>', html, re.DOTALL)
                if not m:
                    print(f"[RealScraper] No __INITIAL_STATE__ found in HTML")
                    return None

                raw = m.group(1).replace('undefined', 'null')
                data = json.loads(raw)
                note_map = data.get('note', {}).get('noteDetailMap', {})

                for k, v in note_map.items():
                    nc = v.get('note', {})
                    if not nc:
                        continue
                    interact = nc.get('interactInfo', {})
                    tag_list = [t.get('name', '') for t in nc.get('tagList', []) if t.get('name')]
                    user = nc.get('user', {})

                    # Parse timestamp
                    time_val = nc.get('time', '')
                    published = ''
                    if isinstance(time_val, (int, float)) and time_val > 1000000000:
                        from datetime import datetime
                        ts = time_val / 1000 if time_val > 1e12 else time_val
                        published = datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    elif isinstance(time_val, str):
                        published = time_val

                    return {
                        "post_title": nc.get('title', '') or nc.get('desc', '')[:50],
                        "published_at": published,
                        "post_tags": tag_list,
                        "nickname": user.get('nickname', ''),
                        "stats": {
                            "likes": self._parse_count(interact.get('likedCount', 0)),
                            "collects": self._parse_count(interact.get('collectedCount', 0)),
                            "comments": self._parse_count(interact.get('commentCount', 0)),
                            "shares": self._parse_count(interact.get('shareCount', 0)),
                            "cover": (nc.get('imageList', [{}])[0].get('urlDefault', '') if nc.get('imageList') else ''),
                        },
                        "content": nc.get('desc', ''),
                    }

                print(f"[RealScraper] noteDetailMap empty")
                return None
        except Exception as e:
            print(f"[RealScraper] SSR scrape failed: {e}")
            return None

    @staticmethod
    def _parse_count(val) -> int:
        """Parse count values like '251' or '1.2万' into int."""
        if isinstance(val, int):
            return val
        if isinstance(val, str):
            val = val.strip()
            if '万' in val:
                return int(float(val.replace('万', '')) * 10000)
            try:
                return int(val)
            except ValueError:
                return 0
        return 0

    async def _try_fetch_account(self, user_id: str) -> Optional[ScrapedAccount]:
        """Try XHS account API endpoints. Returns None if blocked."""
        import httpx

        # Try the user profile API (similar to mobile app API)
        endpoints = [
            f'https://edith.xiaohongshu.com/api/sns/web/v1/user/others_info?user_id={user_id}&source=web_explore_feed',
            f'https://www.xiaohongshu.com/api/sns/web/v1/user/others_info?user_id={user_id}',
        ]

        async with httpx.AsyncClient(timeout=10, follow_redirects=True, cookies=self.cookies) as client:
            for endpoint in endpoints:
                try:
                    resp = await client.get(endpoint, headers=self.headers)
                    if resp.status_code == 200:
                        data = resp.json()
                        if data.get('success') and data.get('data'):
                            user_info = data['data'].get('user', {})
                            notes = data['data'].get('notes', [])
                            return self._parse_account_response(user_info, notes)
                except Exception as e:
                    print(f"[RealScraper] Endpoint {endpoint} failed: {e}")
                    continue
        return None

    async def _try_fetch_post(self, note_id: str) -> Optional[ScrapedPost]:
        """Try XHS note API endpoints. Returns None if blocked."""
        import httpx

        endpoints = [
            f'https://edith.xiaohongshu.com/api/sns/web/v1/feed?source=web_explore_feed&FEEDDBNOTEID={note_id}',
            f'https://www.xiaohongshu.com/api/sns/web/v1/feed?note_id={note_id}',
        ]

        async with httpx.AsyncClient(timeout=10, follow_redirects=True, cookies=self.cookies) as client:
            for endpoint in endpoints:
                try:
                    resp = await client.get(endpoint, headers=self.headers)
                    if resp.status_code == 200:
                        data = resp.json()
                        if data.get('success') and data.get('data'):
                            items = data['data'].get('items', [])
                            if items:
                                return self._parse_post_response(items[0])
                except Exception as e:
                    print(f"[RealScraper] Endpoint {endpoint} failed: {e}")
                    continue
        return None

    def _parse_account_response(self, user_info: dict, notes: list) -> ScrapedAccount:
        """Parse XHS API response into ScrapedAccount format."""
        basic_info = user_info.get('basic_info', {})
        return {
            "nickname": basic_info.get('nickname', ''),
            "bio": basic_info.get('desc', ''),
            "stats": {
                "followers": str(user_info.get('fans', 0)),
                "following": user_info.get('follow', 0),
                "likes_received": str(user_info.get('liked', 0)),
                "posts_count": user_info.get('interactions', {}).get('note_count', 0),
                "avg_likes": 0,
                "avg_collects": 0,
                "avg_comments": 0,
            },
            "top_posts": [
                {
                    "title": n.get('display_title', ''),
                    "cover": n.get('cover', {}).get('url_default', ''),
                    "likes": n.get('interact_info', {}).get('liked_count', 0),
                    "collects": n.get('interact_info', {}).get('collected_count', 0),
                    "comments": n.get('interact_info', {}).get('comment_count', 0),
                }
                for n in notes[:4]
            ],
        }

    def _parse_post_response(self, item: dict) -> ScrapedPost:
        """Parse XHS API note item into ScrapedPost format."""
        note_card = item.get('note_card', {})
        interact = note_card.get('interact_info', {})
        return {
            "post_title": note_card.get('title', ''),
            "published_at": note_card.get('time', ''),
            "post_tags": note_card.get('tag_list', []),
            "stats": {
                "likes": int(interact.get('liked_count', 0) or 0),
                "collects": int(interact.get('collected_count', 0) or 0),
                "comments": int(interact.get('comment_count', 0) or 0),
                "shares": int(interact.get('share_count', 0) or 0),
                "cover": note_card.get('cover', {}).get('url_default', ''),
            },
            "top_posts": [
                {
                    "title": note_card.get('title', ''),
                    "cover": note_card.get('cover', {}).get('url_default', ''),
                    "likes": int(interact.get('liked_count', 0) or 0),
                    "collects": int(interact.get('collected_count', 0) or 0),
                    "comments": int(interact.get('comment_count', 0) or 0),
                }
            ],
        }

    async def _enhanced_mock_account(self, note_id: str, url: str) -> ScrapedAccount:
        """Return realistic mock data with network-verified stats."""
        import httpx

        # Try to get any publicly accessible stats
        follower_count = "未知"
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.get(f'https://www.xiaohongshu.com/user/profile/{note_id}', headers=self.headers)
                if resp.status_code == 200:
                    text = resp.text
                    # Try to extract follower count from page data
                    match = re.search(r'"fans":\s*(\d+)', text)
                    if match:
                        follower_count = str(int(match.group(1)))
        except Exception:
            pass

        return {
            "nickname": f"用户_{note_id[:8]}",
            "bio": "该账号数据需要登录后查看，请确保已配置 XHS_COOKIES 环境变量",
            "stats": {
                "followers": follower_count,
                "following": 0,
                "likes_received": "未知",
                "posts_count": 0,
                "avg_likes": 0,
                "avg_collects": 0,
                "avg_comments": 0,
            },
            "top_posts": [],
        }

    async def _enhanced_mock_post(self, note_id: str, url: str) -> ScrapedPost:
        """Return realistic mock post data."""
        return {
            "post_title": f"笔记_{note_id[:8]}",
            "published_at": "未知",
            "post_tags": [],
            "stats": {
                "likes": 0,
                "collects": 0,
                "comments": 0,
                "shares": 0,
                "cover": "",
            },
            "top_posts": [],
        }
