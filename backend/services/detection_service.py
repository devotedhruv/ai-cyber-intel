from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.models import Alert, SecurityLog
from backend.services.notification_service import NotificationService


class SecurityDetectionService:
    """Small, deterministic authentication detection rules for the central SOC."""

    WINDOW_MINUTES = 5
    FAILED_ATTEMPT_THRESHOLD = 5

    def __init__(self, db: Session):
        self.db = db

    def detect_brute_force(self, username: str, ip_address: str) -> Alert | None:
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=self.WINDOW_MINUTES)
        failed_count = self.db.scalar(
            select(func.count(SecurityLog.id)).where(
                SecurityLog.event_type == "LOGIN",
                SecurityLog.status == "FAILED",
                SecurityLog.username == username,
                SecurityLog.ip_address == ip_address,
                SecurityLog.created_at >= cutoff,
            )
        ) or 0
        if failed_count <= self.FAILED_ATTEMPT_THRESHOLD:
            return None

        existing = self.db.scalar(
            select(Alert).where(
                Alert.alert_type == "BRUTE_FORCE_ATTACK",
                Alert.status == "ACTIVE",
                Alert.username == username,
                Alert.ip_address == ip_address,
                Alert.created_at >= cutoff,
            )
        )
        if existing:
            return existing

        alert = Alert(
            alert_type="BRUTE_FORCE_ATTACK",
            severity="HIGH",
            username=username,
            ip_address=ip_address,
            description="Multiple failed authentication attempts detected",
            status="ACTIVE",
            attempt_count=failed_count,
        )
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        NotificationService(self.db).create(
            title="BRUTE FORCE ATTACK DETECTED",
            message=f"More than five failed login attempts detected for {username} from {ip_address}.",
            notification_type="BRUTE_FORCE_ATTACK",
            severity="HIGH",
            related_user=username,
            ip_address=ip_address,
            deduplicate_minutes=self.WINDOW_MINUTES,
        )
        return alert
