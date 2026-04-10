"""
Analysis API router for Red Checking.
Routes:
  POST /api/analysis        — create a new analysis task
  GET  /api/analysis/{id}   — poll task status
  GET  /api/report/{id}     — get full report

Error codes:
  400  — invalid URL or unsupported link format
  404  — task or report not found
  500  — internal pipeline error
"""
from fastapi import APIRouter, HTTPException, status
from schemas.models import CreateTaskRequest, CreateTaskResponse, TaskStatusResponse, ReportResponse
from services.url_recognizer import validate_url, UrlRecognizer
from services.task_store import create_task, get_task_status, get_report

router = APIRouter(prefix="/api", tags=["analysis"])


@router.post("/analysis", response_model=CreateTaskResponse, status_code=status.HTTP_201_CREATED)
async def create_analysis(req: CreateTaskRequest):
    """
    Create a new analysis task.
    Accepts a Xiaohongshu account or post URL and kicks off the async pipeline.
    Returns immediately with a taskId for polling.
    """
    try:
        url = validate_url(req.url)
        input_type, note_id = UrlRecognizer.recognize(url)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"URL 解析失败：{str(e)}",
        )

    try:
        resp = create_task(url, input_type)
        return resp
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建任务失败：{str(e)}",
        )


@router.get("/analysis/{task_id}", response_model=TaskStatusResponse)
async def get_analysis_status(task_id: str):
    """
    Poll the current status of an analysis task.
    Returns progress percentage and status code.
    When status is 'done', reportId is populated for fetching the full report.
    """
    result = get_task_status(task_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务不存在或已过期",
        )
    return result


@router.get("/report/{report_id}", response_model=ReportResponse)
async def get_report_data(report_id: str):
    """
    Fetch the full analysis report.
    Only available after task status transitions to 'done'.
    """
    result = get_report(report_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="报告不存在或尚未生成",
        )
    return result
