"""
URL recognizer for Xiaohongshu links.
Identifies whether a URL is an account link or a post link.
"""
import re
from typing import Literal
from schemas.models import InputType


class UrlRecognizer:
    # 小红书账号 URL patterns
    ACCOUNT_PATTERNS = [
        re.compile(r"xiaohongshu\.com/user/profile/([^/?]+)"),
        re.compile(r"xhslink\.com/[^/]+/profile/([^/?]+)"),
        re.compile(r"honghong\.top/u/([^/?]+)"),
        # 新版小绿书分享格式
        re.compile(r"www\.xiaohongshu\.com/explore/([a-zA-Z0-9]+)"),
    ]

    # 小红书帖子 URL patterns
    POST_PATTERNS = [
        re.compile(r"xiaohongshu\.com/explore/([a-zA-Z0-9]+)"),
        re.compile(r"xhslink\.com/[^/]+/explore/([a-zA-Z0-9]+)"),
        re.compile(r"www\.xiaohongshu\.com/discovery/item/([a-zA-Z0-9]+)"),
    ]

    @classmethod
    def recognize(cls, url: str) -> tuple[Literal[InputType.ACCOUNT, InputType.POST], str]:
        """
        Recognize the URL type and extract note ID.
        Returns (type, note_id).
        Raises ValueError if URL is not recognized.
        """
        url_lower = url.lower()

        # Check post links first (more specific)
        for pattern in cls.POST_PATTERNS:
            match = pattern.search(url_lower)
            if match:
                return (InputType.POST, match.group(1))

        # Check account links
        for pattern in cls.ACCOUNT_PATTERNS:
            match = pattern.search(url_lower)
            if match:
                return (InputType.ACCOUNT, match.group(1))

        raise ValueError(f"无法识别的链接格式: {url}")


def validate_url(url: str) -> str:
    """Validate and normalize URL."""
    url = url.strip()
    if not url:
        raise ValueError("URL不能为空")
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url
