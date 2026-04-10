"""
Analysis API router.
"""
from fastapi import APIRouter, HTTPException, Query
from schemas.models import (
    CreateTaskRequest, CreateTaskResponse,
    TaskStatusResponse, ReportResponse,
    InputType
)
from services.url_recognizer import UrlRecognizer, validate_url
from services.task_store import create_task, get_task_status, get_report

router = APIRouter(prefix="/api", tags=["analysis"])


@router.post("/analysis", response_model=CreateTaskResponse)
async def create_analysis(req: CreateTaskRequest):
    """
    Create a new analysis task.
    Input: URL of a Xiaohongshu account or post.
    Output: taskId and initial status.
    """
    try:
        url = validate_url(req.url)
        input_type, note_id = UrlRecognizer.recognize(url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    resp = create_task(url, input_type)
    return resp


@router.get("/analysis/{taskId}", response_model=TaskStatusResponse)
async def get_analysis_status(taskId: str):
    """
    Query the current status of an analysis task.
    """
    result = get_task_status(taskId)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return result


@router.get("/report/{reportId}", response_model=ReportResponse)
async def get_report_data(reportId: str):
    """
    Get the full analysis report.
    """
    result = get_report(reportId)
    if not result:
        raise HTTPException(status_code=404, detail="Report not found")
    return result
