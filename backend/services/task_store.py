"""
Simple in-memory task store for MVP.
For demo purposes only — not for production use.
"""
import uuid
import time
import threading
from typing import Optional
from schemas.models import TaskStatus, InputType, CreateTaskResponse, TaskStatusResponse, ReportResponse
from mocks.data import MOCK_ACCOUNT_REPORT, MOCK_POST_REPORT


# In-memory storage
_tasks: dict[str, dict] = {}
_reports: dict[str, dict] = {}

# Simulated async task states for progress simulation
_running_tasks: dict[str, threading.Thread] = {}


def create_task(url: str, input_type: InputType) -> CreateTaskResponse:
    """Create a new analysis task."""
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
    _reports[report_id] = None  # Will be populated after "analysis"

    # Start simulated async task
    t = threading.Thread(target=_simulate_task, args=(task_id, report_id, input_type), daemon=True)
    _running_tasks[task_id] = t
    t.start()

    return CreateTaskResponse(
        taskId=task_id,
        type=input_type,
        status=TaskStatus.PENDING,
    )


def get_task_status(task_id: str) -> Optional[TaskStatusResponse]:
    """Get current task status."""
    task = _tasks.get(task_id)
    if not task:
        return None

    return TaskStatusResponse(
        taskId=task["taskId"],
        type=task["type"],
        status=task["status"],
        reportId=task["reportId"] if task["status"] == TaskStatus.DONE else None,
        errorMessage=task.get("errorMessage"),
        progress=task["progress"],
    )


def get_report(report_id: str) -> Optional[ReportResponse]:
    """Get report data."""
    report = _reports.get(report_id)
    if not report:
        return None
    return ReportResponse(**report)


def _simulate_task(task_id: str, report_id: str, input_type: InputType):
    """Simulate the analysis pipeline with progress updates."""
    import time

    task = _tasks[task_id]

    # Step 1: Scraping (0-30%)
    task["status"] = TaskStatus.SCRAPING
    task["progress"] = 10
    time.sleep(1.5)
    task["progress"] = 30
    time.sleep(1.5)

    # Step 2: Analyzing (30-70%)
    task["status"] = TaskStatus.ANALYZING
    task["progress"] = 45
    time.sleep(2.0)
    task["progress"] = 65
    time.sleep(1.5)

    # Step 3: Generating (70-95%)
    task["status"] = TaskStatus.GENERATING
    task["progress"] = 80
    time.sleep(1.5)
    task["progress"] = 95
    time.sleep(1.0)

    # Step 4: Done
    task["status"] = TaskStatus.DONE
    task["progress"] = 100

    # Populate mock report
    base_report = MOCK_ACCOUNT_REPORT if input_type == InputType.ACCOUNT else MOCK_POST_REPORT
    report_data = {
        **base_report,
        "reportId": report_id,
        "taskId": task_id,
        "type": input_type.value,
    }
    _reports[report_id] = report_data
