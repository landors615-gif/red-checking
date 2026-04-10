from pydantic import BaseModel
from typing import Optional, Literal
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    SCRAPING = "scraping"
    ANALYZING = "analyzing"
    GENERATING = "generating"
    DONE = "done"
    FAILED = "failed"


class InputType(str, Enum):
    ACCOUNT = "account"
    POST = "post"


class CreateTaskRequest(BaseModel):
    url: str


class CreateTaskResponse(BaseModel):
    taskId: str
    type: InputType
    status: TaskStatus


class TaskStatusResponse(BaseModel):
    taskId: str
    type: InputType
    status: TaskStatus
    reportId: Optional[str] = None
    errorMessage: Optional[str] = None
    progress: int = 0  # 0-100


# ---- Report Schemas ----

class AccountReportPayload(BaseModel):
    account_summary: str
    positioning: str
    target_audience: str
    content_topics: list[str]
    viral_posts: list[dict]
    title_patterns: list[str]
    content_patterns: list[str]
    comment_insights: dict
    strengths: list[str]
    weaknesses: list[str]
    benchmarking: dict
    action_suggestions: list[str]


class PostReportPayload(BaseModel):
    post_summary: str
    theme: str
    title_analysis: dict
    structure_analysis: dict
    emotional_hooks: list[str]
    value_points: list[str]
    conflict_points: list[str]
    spread_factors: list[str]
    comment_insights: dict
    benchmark_reference: dict
    improvement_suggestions: list[str]


class ReportResponse(BaseModel):
    reportId: str
    taskId: str
    type: InputType
    generatedAt: str

    # Basic info
    nickname: Optional[str] = None
    bio: Optional[str] = None
    post_title: Optional[str] = None
    post_tags: Optional[list[str]] = None
    published_at: Optional[str] = None

    # Core data
    stats: Optional[dict] = None
    top_posts: Optional[list[dict]] = None

    # AI analysis
    analysis: Optional[dict] = None  # AccountReportPayload or PostReportPayload
