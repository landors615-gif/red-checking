"""
URL recognizer for Xiaohongshu links.
Correctly identifies whether a URL is an account or post link and extracts the note ID.
"""
import re
from typing import Literal
from schemas.models import InputType


def _resolve_xhslink_short_url(url: str) -> str:
    """Resolve generic xhslink.com share links to canonical XHS URLs.

    小红书分享文案里最常见的是 `xhslink.com/a/xxx` / `xhslink.com/m/xxx`
    这类短链。它们本身不包含 note/user id，必须先跟随跳转，否则后端只能
    识别到“这是小红书域名”，但无法判断账号/帖子类型。

    Resolution is best-effort: if the request fails or does not land on a
    recognizable xiaohongshu.com URL, return the original URL and let the normal
    recognizer produce a clear validation error.
    """
    if "xhslink.com" not in url.lower():
        return url

    # Already-expanded xhslink URLs used by some tests/legacy links.
    if re.search(r"xhslink\.com/.*?(explore|profile)/", url, re.I):
        return url

    try:
        import httpx

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
                "Mobile/15E148 Safari/604.1"
            ),
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }
        with httpx.Client(timeout=8, follow_redirects=True, headers=headers) as client:
            resp = client.get(url)
            final_url = str(resp.url)
            if "xiaohongshu.com" in final_url.lower() or "xhslink.com" in final_url.lower():
                return final_url
    except Exception as exc:
        print(f"[UrlRecognizer] xhslink resolve failed: {type(exc).__name__}: {exc}")

    return url


class UrlRecognizer:
    """
    Pattern priority:
      - POST patterns are checked FIRST because they are more specific
      - ACCOUNT patterns are checked second
    """

    # Account URL patterns (checked after post patterns)
    # xhslink.com has variable path depth; match .*?profile/ to handle both
    # /user/profile/ID and /a/xxx/profile/ID formats (non-greedy stops at 'profile')
    ACCOUNT_PATTERNS = [
        re.compile(r"xhslink\.com/.*?profile/([^/?#]+)"),
        re.compile(r"xiaohongshu\.com/user/profile/([^/?#]+)"),
        re.compile(r"honghong\.top/u/([^/?#]+)"),
    ]

    # Post URL patterns (checked FIRST — most specific)
    POST_PATTERNS = [
        re.compile(r"xhslink\.com/.*?explore/([^/?#]+)"),
        # Web URL: xiaohongshu.com/explore/xxx  (note-style share)
        re.compile(r"xiaohongshu\.com/explore/([^/?#]+)"),
        # Web URL: xiaohongshu.com/discovery/item/xxx  (old style)
        re.compile(r"xiaohongshu\.com/discovery/item/([^/?#]+)"),
        # Web URL: xiaohongshu.com/explore/xxx  (new style, same domain)
        re.compile(r"www\.xiaohongshu\.com/explore/([^/?#]+)"),
        # Explicit item page
        re.compile(r"www\.xiaohongshu\.com/discovery/item/([^/?#]+)"),
    ]

    @classmethod
    def recognize(cls, url: str) -> tuple[Literal[InputType.ACCOUNT, InputType.POST], str]:
        """
        Recognize URL type and extract note ID.
        Returns (type, note_id).
        Raises ValueError if URL is not recognized as a supported XHS format.
        """
        url_lower = url.lower()

        # Check post links first (more specific, also catches explore)
        for pattern in cls.POST_PATTERNS:
            match = pattern.search(url_lower)
            if match:
                note_id = match.group(1).strip()
                if note_id:
                    return (InputType.POST, note_id)

        # Check account links
        for pattern in cls.ACCOUNT_PATTERNS:
            match = pattern.search(url_lower)
            if match:
                note_id = match.group(1).strip()
                if note_id:
                    return (InputType.ACCOUNT, note_id)

        raise ValueError(
            f"无法识别的链接格式。请确保链接来自小红书（xiaohongshu.com 或 xhslink.com）。\n"
            f"收到：{url[:80]}"
        )


def validate_url(url: str) -> str:
    """Normalize and validate URL input."""
    url = url.strip()
    if not url:
        raise ValueError("URL不能为空")

    if not url.startswith(("http://", "https://", "//")):
        url = "https://" + url

    # Very basic domain check
    if "xiaohongshu" not in url.lower() and "xhslink" not in url.lower():
        raise ValueError(
            "仅支持小红书链接。请提供 xiaohongshu.com 或 xhslink.com 开头的链接。"
        )

    return _resolve_xhslink_short_url(url)
