"""
Scraper Error Types for Red Checking.

Used to classify failure reasons from the XHS scraper so the frontend
and logs can distinguish between: cookie expiry, rate limiting, video
posts, parse failures, and network errors.
"""

from typing import Optional


class XHSScraperError(Exception):
    """Classified scraper error with machine-readable code."""

    # Machine-readable error codes
    CODE_COOKIE_EXPIRED = "XHS_COOKIE_EXPIRED"
    CODE_RATE_LIMITED = "XHS_RATE_LIMITED"
    CODE_VIDEO_NOT_SUPPORTED = "XHS_VIDEO_NOT_SUPPORTED"
    CODE_PARSE_FAILED = "XHS_PARSE_FAILED"
    CODE_NETWORK_ERROR = "XHS_NETWORK_ERROR"
    CODE_CONTENT_BLOCKED = "XHS_CONTENT_BLOCKED"

    def __init__(
        self,
        code: str,
        message: str,
        debug: Optional[dict] = None,
    ):
        super().__init__(message)
        self.code = code
        self.message = message
        self.debug = debug or {}

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "message": self.message,
            "debug": self.debug,
        }

    def log_prefix(self) -> str:
        return f"[{self.code}] {self.message}"
