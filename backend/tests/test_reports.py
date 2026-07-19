import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.main import app
from backend.models import Alert, Base, SecurityLog, ThreatEvent
from backend.services.report_service import ReportService


class ReportServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine("sqlite+pysqlite:///:memory:")
        Base.metadata.create_all(self.engine)

    def tearDown(self) -> None:
        self.engine.dispose()

    def test_security_summary_uses_existing_soc_tables(self) -> None:
        with Session(self.engine) as db:
            db.add_all([
                SecurityLog(
                    event_type="LOGIN",
                    username="analyst",
                    status="SUCCESS",
                    source_ip="127.0.0.1",
                    severity="low",
                    description="Successful login",
                ),
                SecurityLog(
                    event_type="LOGIN",
                    username="analyst",
                    status="FAILED",
                    source_ip="127.0.0.1",
                    severity="medium",
                    description="Failed login",
                ),
                Alert(
                    alert_type="BRUTE_FORCE_ATTACK",
                    severity="HIGH",
                    username="analyst",
                    ip_address="127.0.0.1",
                    status="ACTIVE",
                ),
                ThreatEvent(
                    source_ip="127.0.0.1",
                    threat_type="BRUTE_FORCE_ATTACK",
                    risk_level="HIGH",
                    risk_score=90,
                ),
            ])
            db.commit()

            self.assertEqual(ReportService(db).security_summary(), {
                "total_logins": 2,
                "successful_logins": 1,
                "failed_logins": 1,
                "active_alerts": 1,
                "detected_threats": 1,
                "threat_level": "HIGH",
            })

    def test_reports_routes_are_registered(self) -> None:
        routes = {(route.path, frozenset(route.methods or [])) for route in app.routes}

        self.assertIn(("/api/reports", frozenset({"GET"})), routes)
        self.assertIn(("/api/reports/archive", frozenset({"GET"})), routes)
        self.assertIn(("/api/reports/generate", frozenset({"POST"})), routes)
        self.assertIn(("/api/reports/{report_id}", frozenset({"GET"})), routes)


if __name__ == "__main__":
    unittest.main()
