from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.models import Notification


class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        *,
        title: str,
        message: str,
        notification_type: str,
        severity: str,
        related_user: str | None = None,
        ip_address: str | None = None,
        deduplicate_minutes: int | None = None,
    ) -> Notification:
        if deduplicate_minutes:
            cutoff = datetime.now(timezone.utc) - timedelta(minutes=deduplicate_minutes)
            existing = self.db.scalar(select(Notification).where(
                Notification.title == title,
                Notification.related_user == related_user,
                Notification.ip_address == ip_address,
                Notification.created_at >= cutoff,
            ).order_by(Notification.created_at.desc()))
            if existing:
                return existing
        item = Notification(
            title=title,
            message=message,
            notification_type=notification_type,
            severity=severity,
            related_user=related_user,
            ip_address=ip_address,
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def latest(self, *, limit: int, unread_only: bool = False) -> tuple[list[Notification], int, int]:
        filters = [Notification.is_read.is_(False)] if unread_only else []
        rows = list(self.db.scalars(select(Notification).where(*filters).order_by(Notification.created_at.desc()).limit(limit)).all())
        total = self.db.scalar(select(func.count(Notification.id)).where(*filters)) or 0
        unread = self.db.scalar(select(func.count(Notification.id)).where(Notification.is_read.is_(False))) or 0
        return rows, total, unread

    def mark_read(self, notification_id: int) -> Notification | None:
        item = self.db.get(Notification, notification_id)
        if not item:
            return None
        item.is_read = True
        self.db.commit()
        self.db.refresh(item)
        return item
