from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from backend.api.auth import current_user
from backend.database import get_db
from backend.models import Report, User
from backend.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["Security reports"])
ReportType = Literal["DAILY_SECURITY_REPORT", "THREAT_REPORT", "INCIDENT_REPORT"]


class ReportGenerateRequest(BaseModel):
    report_type: ReportType


class ReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    report_type: str
    generated_by: str
    summary: dict
    created_at: datetime


class SecuritySummaryResponse(BaseModel):
    total_logins: int
    successful_logins: int
    failed_logins: int
    active_alerts: int
    detected_threats: int
    threat_level: Literal["LOW", "MEDIUM", "HIGH"]


@router.get("", response_model=SecuritySummaryResponse)
def security_summary(
    _: User = Depends(current_user),
    db: Session = Depends(get_db),
) -> dict:
    return ReportService(db).security_summary()


@router.get("/archive", response_model=list[ReportResponse])
def report_archive(
    limit: int = Query(default=50, ge=1, le=200),
    _: User = Depends(current_user),
    db: Session = Depends(get_db),
) -> list[Report]:
    return ReportService(db).list(limit)


@router.post("/generate", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def generate_report(payload: ReportGenerateRequest, user: User = Depends(current_user), db: Session = Depends(get_db)) -> Report:
    return ReportService(db).generate(payload.report_type, user.username)


@router.get("/{report_id}", response_model=ReportResponse)
def report(report_id: int, _: User = Depends(current_user), db: Session = Depends(get_db)) -> Report:
    item = ReportService(db).get(report_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return item
