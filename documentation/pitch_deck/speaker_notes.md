# Sentinel AI — Judge Pitch Speaker Notes

Target length: 7–9 minutes plus questions.

## 1. Opening — 30 seconds

“Every login is a security signal. The problem is that organizations often record that signal without turning it into a timely decision. Sentinel AI is an AI-powered cyber threat intelligence and SOC platform that connects secure authentication to detection, risk scoring, attack prediction, automated response, notification, and reporting.”

## 2. Problem — 40 seconds

Explain the three operational gaps: fragmented visibility, alert overload, and slow response. Avoid claiming that the platform replaces analysts; it helps analysts reach an informed decision faster.

## 3. Solution — 45 seconds

Walk left to right through the pipeline. Emphasize that one event keeps its context throughout the system, creating an auditable chain from login to response.

## 4. Demo story — 45 seconds

Set up the live demonstration: one valid login, one invalid login, then repeated failures for the same username and IP. The sixth failure inside five minutes should cross the rule threshold and produce a high-severity brute-force alert.

## 5. Command center — 45 seconds

Show that this is more than a landing dashboard. The analyst can move from login monitoring to threat intelligence, AI risk, attack paths, incidents, SOAR workflows, notifications, and reports without losing context.

## 6. Architecture — 50 seconds

Explain that Phases 1–9 remain independently runnable and retain domain ownership. The Central API provides authentication, routing, health, topology, and aggregation. PostgreSQL stores central security and integration data while React provides the SOC interface.

## 7. AI and detection — 50 seconds

Stress explainability. Deterministic rules provide a reliable baseline, while the Phase 4 service extends detection with AI capabilities. A score is always presented with the behavior that caused it: user, IP, event window, frequency, and detection reason.

## 8. Security by design — 45 seconds

Mention PBKDF2 password hashing, hashed and expiring bearer tokens, environment-based secrets, additive database initialization, auditable authentication records, and defensive-only automated actions.

## 9. Differentiation — 40 seconds

The key distinction is the closed loop: detect, understand, predict, respond. The modular phase architecture also allows individual capabilities to be improved without rewriting the whole platform.

## 10. Validation — 40 seconds

State only verified engineering evidence: frontend production build, backend compile checks, isolated integration testing, Docker Compose startup, and health endpoints. Do not invent customer, accuracy, or performance numbers.

## 11. Roadmap — 35 seconds

Present the roadmap as deliberate hardening: real-time streaming and RBAC first, broader enterprise integrations next, then multi-tenancy, high availability, compliance packs, and analyst collaboration.

## 12. Closing — 25 seconds

“Sentinel AI turns every security signal into a confident response. It gives analysts a continuous and explainable journey from detection to action. I’d now like to show that journey live.”

## Live demo checklist

1. Open the secure login page and confirm the API health endpoint is healthy.
2. Log in successfully; show the new `LOGIN / SUCCESS` event.
3. Sign out, submit one incorrect password, and show the failed-login notification.
4. Submit six failed attempts using the same username and client IP within five minutes.
5. Show the high-severity brute-force alert, AI risk score, attack path, incident, and notification.
6. Open Reports, generate a Daily Security Report, and display its persisted summary.

## Backup if the live demo is unavailable

Use slides 4, 5, 7, and 10 as the fallback sequence. Explain the expected database records and API responses without claiming a live execution occurred.

## Likely judge questions

- **Why call this AI-powered?** Phase 4 owns AI detection, while deterministic risk rules provide a transparent and testable safety baseline.
- **How do you avoid duplicate brute-force alerts?** Detection is scoped to the same username, source IP, and five-minute attack window, with duplicate suppression for that window.
- **Is automated response dangerous?** The current SOAR flow records incidents, starts workflows, notifies administrators, and prepares defensive action; destructive actions are not performed blindly.
- **How are secrets protected?** Passwords, database credentials, tokens, and integration keys are provided through environment variables; credentials are not hardcoded.
- **Can it scale?** The phase services are independently runnable and connected through a central API, allowing capabilities to be deployed and scaled separately.
