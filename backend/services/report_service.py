from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.models import Alert, Incident, Report, SecurityLog, ThreatEvent


class ReportService:
    SUPPORTED_TYPES = {"DAILY_SECURITY_REPORT", "THREAT_REPORT", "INCIDENT_REPORT"}

    def __init__(self, db: Session):
        self.db = db

    def generate(self, report_type: str, generated_by: str) -> Report:
        normalized = report_type.strip().upper()
        if normalized not in self.SUPPORTED_TYPES:
            raise ValueError("Unsupported report type")
        builders = {
            "DAILY_SECURITY_REPORT": self._daily_summary,
            "THREAT_REPORT": self._threat_summary,
            "INCIDENT_REPORT": self._incident_summary,
        }
        report = Report(report_type=normalized, generated_by=generated_by, summary=builders[normalized]())
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def list(self, limit: int) -> list[Report]:
        return list(self.db.scalars(select(Report).order_by(Report.created_at.desc()).limit(limit)).all())

    def get(self, report_id: int) -> Report | None:
        return self.db.get(Report, report_id)

    def security_summary(self) -> dict:
        """Return the current SOC authentication and threat posture."""
        login_filter = (SecurityLog.event_type == "LOGIN",)
        count_logins = lambda *extra: self.db.scalar(
            select(func.count(SecurityLog.id)).where(*login_filter, *extra)
        ) or 0
        active_alerts = self.db.scalar(
            select(func.count(Alert.id)).where(func.upper(Alert.status) == "ACTIVE")
        ) or 0
        detected_threats = self.db.scalar(select(func.count(ThreatEvent.id))) or 0
        alert_severities = set(self.db.scalars(
            select(func.upper(Alert.severity)).where(func.upper(Alert.status) == "ACTIVE")
        ).all())
        threat_levels = set(self.db.scalars(select(func.upper(ThreatEvent.risk_level))).all())

        levels = alert_severities | threat_levels
        if levels & {"HIGH", "CRITICAL"}:
            threat_level = "HIGH"
        elif "MEDIUM" in levels:
            threat_level = "MEDIUM"
        else:
            threat_level = "LOW"

        return {
            "total_logins": count_logins(),
            "successful_logins": count_logins(SecurityLog.status == "SUCCESS"),
            "failed_logins": count_logins(SecurityLog.status == "FAILED"),
            "active_alerts": active_alerts,
            "detected_threats": detected_threats,
            "threat_level": threat_level,
        }

    def _daily_summary(self) -> dict:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
        login_filter = (SecurityLog.event_type == "LOGIN", SecurityLog.created_at >= cutoff)
        count_logs = lambda *extra: self.db.scalar(select(func.count(SecurityLog.id)).where(*login_filter, *extra)) or 0
        return {
            "period": "Last 24 hours",
            "total_logins": count_logs(),
            "successful_logins": count_logs(SecurityLog.status == "SUCCESS"),
            "failed_logins": count_logs(SecurityLog.status == "FAILED"),
            "detected_threats": self.db.scalar(select(func.count(ThreatEvent.id)).where(ThreatEvent.created_at >= cutoff)) or 0,
            "alerts": self.db.scalar(select(func.count(Alert.id)).where(Alert.created_at >= cutoff)) or 0,
            "incidents": self.db.scalar(select(func.count(Incident.id)).where(Incident.created_at >= cutoff)) or 0,
        }

    def _threat_summary(self) -> dict:
        rows = self.db.scalars(select(ThreatEvent).order_by(ThreatEvent.created_at.desc()).limit(100)).all()
        return {"threats": [{
            "threat_type": row.threat_type,
            "risk_level": row.risk_level,
            "risk_score": row.risk_score,
            "source_ip": row.source_ip,
            "time": row.created_at.isoformat(),
        } for row in rows]}

    def _incident_summary(self) -> dict:
        rows = self.db.scalars(select(Incident).order_by(Incident.created_at.desc()).limit(100)).all()
        return {"incidents": [{
            "incident_type": row.incident_type,
            "severity": row.severity,
            "status": row.status,
            "response_action": row.response_action,
            "time": row.created_at.isoformat(),
        } for row in rows]}
