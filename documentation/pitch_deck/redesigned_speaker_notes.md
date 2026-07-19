# Sentinel AI — Redesigned Pitch Speaker Notes

Target delivery: 10–12 minutes plus demo and questions.

1. **Opening:** Sentinel AI turns scattered security telemetry into an explainable decision and controlled response.
2. **Problem:** Emphasize fragmented context, alert overload, and response delay—not replacement of analysts.
3. **Solution:** Walk left to right through collect, normalize, detect, prioritize, predict, and respond.
4. **Live proof:** Explain the verified six-failure brute-force story and its persisted outcomes.
5. **SOC command center:** Show that analysts can move between monitoring, intelligence, detection, paths, SOAR, and reports without losing context.
6. **Architecture:** Explain independent Phase 1–9 ownership and the central FastAPI security plane.
7. **Trust boundary:** Cover PBKDF2, hashed bearer tokens, expiry, environment secrets, safe schema evolution, and auditability.
8. **Detection engine:** Stress explainability and the exact verified brute-force condition.
9. **Coverage:** Be explicit that authentication detection is implemented; web, network, and endpoint coverage is roadmap.
10. **Web blueprint:** Present SQL injection, XSS, traversal, SSRF, and related modules as safe telemetry-driven extensions.
11. **AI:** AI augments deterministic evidence; it does not replace validation or human judgment.
12. **Threat intelligence:** Explain normalization, IOC correlation, reputation, CVE context, and fault tolerance.
13. **Attack prediction:** Predictions are bounded possibilities linked to evidence—not statements of certainty.
14. **SOAR:** Workflow automation is active; disruptive containment remains behind an approval boundary.
15. **Reporting:** Highlight the authenticated summary API, PostgreSQL-backed archives, and JSON/CSV exports.
16. **Validation:** Only state verified engineering evidence: builds, compile checks, tests, Docker/PostgreSQL, and authenticated API responses.
17. **Roadmap:** Harden first, expand web detection next, then integrate enterprise telemetry and scale.
18. **Closing:** “Sentinel AI connects detection, understanding, prediction, and controlled response in one explainable SOC workflow.”

## Demo sequence

1. Open the landing page and enter the protected SOC console.
2. Show a successful login event.
3. Generate repeated failures for the same username and source IP.
4. Show the HIGH brute-force alert after the sixth failure inside five minutes.
5. Trace the event through risk, threat, attack path, incident, and notification views.
6. Open Reports and show the live PostgreSQL-backed summary and export options.

## Accuracy guardrails

- Do not say Sentinel AI currently detects every attack.
- Label SQL injection, XSS, network, malware, and endpoint detection as roadmap modules until implemented and verified.
- Do not invent customer counts, detection accuracy, latency, or performance benchmarks.
- Describe automated response as controlled and approval-aware.
