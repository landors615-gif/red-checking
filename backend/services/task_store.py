"""
In-memory task store for Red Checking MVP.
Coordinates scraping → analysis pipeline using the scraper protocol.

Production note: replace with Redis/Postgres for multi-instance deployments.
"""
import asyncio
import uuid
import time
import threading
import random
import os
from typing import Optional

from schemas.models import (
    TaskStatus, InputType,
    CreateTaskResponse, TaskStatusResponse, ReportResponse,
)
from mocks.data import MOCK_ACCOUNT_REPORT, MOCK_POST_REPORT

# Lazy imports for real services
_scraper = None
_analysis_service = None

def _get_scraper():
    global _scraper
    if _scraper is None:
        from services.scraper_protocol import get_scraper
        _scraper = get_scraper()
    return _scraper

def _get_analysis_service():
    global _analysis_service
    if _analysis_service is None:
        from services.analysis_service import get_analysis_service
        _analysis_service = get_analysis_service()
    return _analysis_service


# ── In-memory storage ────────────────────────────────────────────────

_tasks: dict[str, dict] = {}
_reports: dict[str, dict] = {}
_running_tasks: dict[str, threading.Thread] = {}

# Allow injecting random failures for demo/testing
_SIMULATE_FAILURES = os.environ.get('SIMULATE_FAILURES', 'false').lower() == 'true'


# ── Public API ───────────────────────────────────────────────────────

def create_task(url: str, input_type: InputType) -> CreateTaskResponse:
    task_id = f"task_{uuid.uuid4().hex[:12]}"
    report_id = f"rpt_{uuid.uuid4().hex[:12]}"

    task = {
        "taskId": task_id,
        "type": input_type,
        "status": TaskStatus.PENDING,
        "url": url,
        "reportId": report_id,
        "errorMessage": None,
        "progress": 0,
        "createdAt": time.time(),
    }
    _tasks[task_id] = task
    _reports[report_id] = None

    t = threading.Thread(
        target=_run_pipeline,
        args=(task_id, report_id, input_type, url),
        daemon=True,
    )
    _running_tasks[task_id] = t
    t.start()

    return CreateTaskResponse(
        taskId=task_id,
        type=input_type,
        status=TaskStatus.PENDING,
    )


def get_task_status(task_id: str) -> Optional[TaskStatusResponse]:
    task = _tasks.get(task_id)
    if not task:
        return None
    return TaskStatusResponse(
        taskId=task["taskId"],
        type=task["type"],
        status=task["status"],
        reportId=task["reportId"] if task["status"] == TaskStatus.DONE else None,
        errorMessage=task.get("errorMessage"),
        errorCode=task.get("errorCode"),
        progress=task["progress"],
    )


def get_report(report_id: str) -> Optional[ReportResponse]:
    report = _reports.get(report_id)
    if not report:
        return None
    return ReportResponse(**report)


# ── Pipeline ────────────────────────────────────────────────────────

def _run_pipeline(task_id: str, report_id: str, input_type: InputType, url: str):
    """
    Executes: validate → scrape → analyze → generate report.
    Updates task progress in-place.  Stores final report in _reports.
    """
    task = _tasks[task_id]

    try:
        # ── Step 1: Scrape (0-30%) ──────────────────────────────────
        task["status"] = TaskStatus.SCRAPING
        task["progress"] = 10
        time.sleep(1.2)

        # _run_pipeline is a plain thread; use asyncio.run() to call async scraper methods.
        scraper = _get_scraper()
        note_id = _extract_note_id(url, input_type)
        if input_type == InputType.ACCOUNT:
            raw = asyncio.run(scraper.scrape_account(note_id, url))
        else:
            raw = asyncio.run(scraper.scrape_post(note_id, url))

        task["progress"] = 30
        time.sleep(1.2)

        # ── Step 2: Analyze (30-70%) ────────────────────────────────
        task["status"] = TaskStatus.ANALYZING
        task["progress"] = 45
        time.sleep(1.8)

        # Call real AI analysis service (falls back to mock if no API key)
        # Runs in thread context via asyncio.run()
        async def _do_analysis():
            svc = _get_analysis_service()
            if input_type == InputType.ACCOUNT:
                return await svc.analyze_account(raw)
            else:
                return await svc.analyze_post(raw)
        analysis_result = asyncio.run(_do_analysis())
        analysis_payload = {"analysis": analysis_result}

        task["progress"] = 65
        time.sleep(1.2)

        # ── Step 3: Generate report (70-95%) ────────────────────────
        task["status"] = TaskStatus.GENERATING
        task["progress"] = 80
        time.sleep(1.2)

        # Simulate random failure for testing error handling
        if _SIMULATE_FAILURES and random.random() < 0.3:
            raise RuntimeError("模拟分析失败：内容获取超时，请重试")

        # Build final report
        report_data = {
            **(_build_base_report(input_type, raw)),
            **analysis_payload,
            "reportId": report_id,
            "taskId": task_id,
            "type": input_type.value,
            "generatedAt": _iso_now(),
        }
        _reports[report_id] = report_data

        task["progress"] = 95
        time.sleep(0.8)

        # ── Done ────────────────────────────────────────────────────
        task["status"] = TaskStatus.DONE
        task["progress"] = 100

    except Exception as exc:
        task["status"] = TaskStatus.FAILED
        task["progress"] = 0
        # Handle classified scraper errors
        from services.scraper_errors import XHSScraperError
        from services.analysis_service import AIAnalysisError
        if isinstance(exc, XHSScraperError):
            task["errorMessage"] = f"[{exc.code}] {exc.message}"
            task["errorCode"] = exc.code
            task["errorDebug"] = exc.debug
            print(f"[CRITICAL] {exc.log_prefix()}")
            if exc.debug:
                print(f"[DEBUG] {exc.debug}")
        elif isinstance(exc, AIAnalysisError):
            task["errorCode"] = exc.code
            # Map error codes to user-friendly Chinese messages
            friendly_messages = {
                AIAnalysisError.CODE_EMPTY_RESPONSE: "AI 分析结果为空，请稍后重试",
                AIAnalysisError.CODE_OUTPUT_PARSE_FAILED: "AI 返回格式异常，请稍后重试",
                AIAnalysisError.CODE_MINIMAX_HTTP_ERROR: "AI 服务请求失败，请稍后重试",
                AIAnalysisError.CODE_MINIMAX_EMPTY_RESPONSE: "AI 服务返回为空，请稍后重试",
            }
            task["errorMessage"] = friendly_messages.get(exc.code, str(exc))
            task["errorDebug"] = exc.debug
            print(f"[CRITICAL] {exc.log_prefix()}")
            if exc.debug:
                print(f"[DEBUG] {exc.debug}")
        else:
            task["errorMessage"] = str(exc)
            print(f"[ERROR] Pipeline exception: {exc}")
        # Clean up failed report slot
        if _reports.get(report_id) is None:
            del _reports[report_id]


# ── Helpers ─────────────────────────────────────────────────────────

def _extract_note_id(url: str, input_type: InputType) -> str:
    """Extract note ID from URL (used for real scraper routing)."""
    from services.url_recognizer import UrlRecognizer
    _, note_id = UrlRecognizer.recognize(url)
    return note_id


def _get_analysis_payload(input_type: InputType) -> dict:
    """Return the AI analysis section for the given type.
    
    NOTE: This is only used as fallback when no real AI API is configured.
    The real analysis path goes through _get_analysis_service() in _run_pipeline.
    """
    if input_type == InputType.ACCOUNT:
        return {"analysis": MOCK_ACCOUNT_REPORT["analysis"]}
    return {"analysis": MOCK_POST_REPORT["analysis"]}


def _build_base_report(input_type: InputType, raw: dict) -> dict:
    """Merge scraped raw data into report structure."""
    base = {}
    if input_type == InputType.ACCOUNT:
        base["nickname"] = raw.get("nickname", "")
        base["bio"] = raw.get("bio", "")
        base["stats"] = raw.get("stats", {})
        base["top_posts"] = raw.get("top_posts", [])
    else:
        base["post_title"] = raw.get("post_title", "")
        base["published_at"] = raw.get("published_at", "")
        base["post_tags"] = raw.get("post_tags", [])
        base["stats"] = raw.get("stats", {})
        base["top_posts"] = raw.get("top_posts", [])
    return base


def _iso_now() -> str:
    from datetime import datetime, timezone, timedelta
    tz = timezone(timedelta(hours=8))
    return datetime.now(tz).isoformat()
