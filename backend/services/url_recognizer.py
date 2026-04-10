"""
URL recognizer for Xiaohongshu links.
Correctly identifies whether a URL is an account or post link and extracts the note ID.
"""
import re
from typing import Literal
from schemas.models import InputType


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

    return url
