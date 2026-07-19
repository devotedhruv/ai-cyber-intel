#!/usr/bin/env python3
"""Generate the compact seven-slide Sentinel AI pitch deck."""

from pathlib import Path

from generate_redesigned_deck import (
    AMBER, BG, BLUE, CYAN, GREEN, MUTED, PDF as _, PPTX as __, RED, SURFACE,
    SURFACE_2, TEXT, VIOLET, WHITE, Deck, connect, prop,
)


ROOT = Path(__file__).resolve().parent
PPTX = ROOT / "Sentinel_AI_Compact_Pitch_Deck.pptx"
PDF = ROOT / "Sentinel_AI_Compact_Pitch_Deck.pdf"


def build(doc):
    d = Deck(doc)

    # 1 — Vision
    p = d.slide()
    d.pill(p, 760, 1400, 3400, "AI-powered security operations", CYAN)
    d.text(p, 760, 2800, 18500, 1200, "SENTINEL", 44, WHITE, bold=True)
    d.text(p, 760, 4000, 7000, 1200, "AI", 44, CYAN, bold=True)
    d.text(p, 780, 5750, 17500, 1300, "From security signal\nto confident response.", 23, TEXT, bold=True)
    d.text(p, 780, 7900, 16200, 1100, "A modular SOC platform connecting detection, explainable risk, attack prediction, response, and reporting.", 12, MUTED)
    d.ellipse(p, 22800, 2900, 5600, 5600, SURFACE, CYAN)
    d.ellipse(p, 24100, 4200, 3000, 3000, BG, BLUE)
    d.text(p, 24600, 5080, 2000, 700, "AI", 27, CYAN, bold=True, align=1)
    for y, color in [(3300, CYAN), (4500, BLUE), (5700, VIOLET), (6900, GREEN)]:
        d.line(p, 28400, y, 32100, y-450, color, 50)
    d.text(p, 780, 16600, 15000, 350, "FASTAPI  •  REACT  •  POSTGRESQL  •  AI/ML  •  SOAR", 8, MUTED)

    # 2 — Problem and idea
    p = d.slide("The idea")
    d.title(p, "Security tools produce alerts. Sentinel AI produces a decision.", "The idea is to preserve context from the first signal through investigation and controlled response.")
    d.card(p, 800, 3700, 9500, 6500, "PROBLEM 01", "Fragmented context", "Identity, IP, intelligence, detections, incidents, and reports are separated across tools.", RED)
    d.card(p, 12150, 3700, 9500, 6500, "PROBLEM 02", "Alert overload", "Raw events create noise when risk, evidence, and recommended action are not connected.", AMBER)
    d.card(p, 23500, 3700, 9500, 6500, "PROBLEM 03", "Slow response", "Analysts reconstruct the story manually before they can contain, escalate, or explain it.", BLUE)
    d.rect(p, 800, 11300, 32200, 2500, SURFACE_2, CYAN, 160)
    d.text(p, 1350, 11750, 4200, 350, "THE IDEA", 8, CYAN, bold=True)
    d.text(p, 1350, 12450, 30000, 500, "One explainable security loop: detect → understand → predict → respond.", 17, WHITE, bold=True)

    # 3 — Product and proof
    p = d.slide("Product + proof")
    d.title(p, "A working end-to-end threat story", "Sentinel AI already converts authentication behavior into persisted SOC evidence and action.")
    flow = [("LOGIN", CYAN), ("DETECT", RED), ("SCORE", AMBER), ("PREDICT", VIOLET), ("RESPOND", GREEN), ("REPORT", BLUE)]
    x = 700
    for i, (label, color) in enumerate(flow):
        d.node(p, x, 3900, 4400, label, color, f"STEP {i+1:02d}")
        if i < len(flow)-1:
            d.arrow(p, x+4400, 4400, 650, MUTED)
        x += 5050
    d.metric(p, 800, 6800, 7000, ">5", "failed attempts", RED)
    d.metric(p, 8500, 6800, 7000, "5 min", "detection window", AMBER)
    d.metric(p, 16200, 6800, 7000, "90/100", "high risk", VIOLET)
    d.metric(p, 23900, 6800, 7000, "200 OK", "verified report API", GREEN)
    d.rect(p, 800, 9800, 30100, 2800, SURFACE, SURFACE_2, 160)
    d.pill(p, 1300, 10300, 3900, "Implemented + verified", GREEN)
    d.text(p, 5700, 10320, 23900, 500, "Same user + same IP + sixth failure inside five minutes → HIGH alert", 13, WHITE, bold=True)
    d.text(p, 5700, 11200, 23500, 450, "Traceable across security logs, AI risk, threat event, attack path, incident, notification, and report.", 9, MUTED)

    # 4 — Market
    p = d.slide("Market")
    d.title(p, "A broad need with a focused entry point", "Sentinel AI starts with explainable identity threats and expands through modular security telemetry.")
    markets = [
        ("SMALL & MID-SIZE TEAMS", "Need unified visibility without assembling a large SOC stack.", CYAN),
        ("MANAGED SECURITY PROVIDERS", "Need repeatable monitoring, evidence, reporting, and tenant-ready workflows.", BLUE),
        ("EDUCATION & PUBLIC SECTOR", "Need accessible defensive tooling, auditability, and constrained automation.", GREEN),
    ]
    for i, (head, body, color) in enumerate(markets):
        d.card(p, 800+i*10800, 3700, 9800, 6200, "TARGET USER", head, body, color)
    d.rect(p, 800, 10800, 31400, 3000, SURFACE_2, VIOLET, 160)
    d.text(p, 1300, 11250, 4200, 350, "WHY NOW", 8, VIOLET, bold=True)
    d.text(p, 1300, 12000, 29800, 500, "More telemetry + limited analyst capacity + rising identity attacks = demand for explainable automation.", 15, WHITE, bold=True)
    d.text(p, 1300, 13000, 29200, 350, "No invented TAM figure: initial validation focuses on interviews, pilots, conversion, and measurable analyst time saved.", 8, MUTED)

    # 5 — Differentiation
    p = d.slide("Why Sentinel AI")
    d.title(p, "More than a dashboard. More accountable than a black box.", "The advantage is the closed loop and the evidence that remains visible throughout it.")
    d.card(p, 800, 3700, 9800, 7200, "01 / CLOSED LOOP", "End-to-end", "A single event connects authentication, logs, intelligence, risk, prediction, incidents, notifications, and reports.", CYAN)
    d.card(p, 12000, 3700, 9800, 7200, "02 / MODULAR", "Phase-owned", "Nine independent capabilities evolve separately while a central API preserves one operational experience.", BLUE)
    d.card(p, 23200, 3700, 9800, 7200, "03 / EXPLAINABLE", "Evidence first", "Rules and AI scores retain username, IP, time window, frequency, reason, confidence, and response state.", GREEN)
    labels = [("DETECT", CYAN), ("UNDERSTAND", BLUE), ("PREDICT", AMBER), ("RESPOND", GREEN)]
    x = 2600
    for i, (label, color) in enumerate(labels):
        d.pill(p, x, 12200, 4500, label, color)
        if i < len(labels)-1:
            d.arrow(p, x+4500, 12460, 1800, MUTED)
        x += 6900

    # 6 — Go to market
    p = d.slide("Go to market")
    d.title(p, "Land with one visible threat story. Expand with telemetry.", "A product-led technical pilot turns the working authentication use case into broader security adoption.")
    stages = [
        ("01", "PILOT", "Deploy the central SOC and prove login-to-report visibility with a real security team.", CYAN),
        ("02", "INTEGRATE", "Add approved identity, WordPress, WAF, SIEM, and threat-intelligence event sources.", BLUE),
        ("03", "EXPAND", "Enable web, network, endpoint, collaboration, compliance, and multi-tenant modules.", GREEN),
    ]
    for i, (num, head, body, color) in enumerate(stages):
        x = 800+i*10800
        d.rect(p, x, 3700, 9800, 7600, SURFACE, color, 180)
        d.ellipse(p, x+500, 4250, 1000, 1000, BG, color)
        d.text(p, x+690, 4570, 620, 260, num, 9, color, bold=True, align=1)
        d.text(p, x+500, 5850, 8500, 600, head, 19, WHITE, bold=True)
        d.text(p, x+500, 7200, 8500, 2400, body, 11, MUTED)
    d.pill(p, 800, 12500, 3300, "Pilot metrics", AMBER)
    d.text(p, 4600, 12520, 27000, 500, "Time-to-triage  •  detection-to-report completion  •  analyst adoption  •  false-positive review", 11, WHITE, bold=True)

    # 7 — What's next
    p = d.slide("What's next")
    d.title(p, "Turn a verified core into a broader defense platform", "The next milestones expand coverage while preserving accuracy, safety, and the existing architecture.")
    roadmap = [
        ("NOW", "HARDEN", "RBAC\nreal-time streaming\nautomated tests\nproduction observability", CYAN),
        ("NEXT", "WEB DETECTION", "WordPress telemetry\nSQL injection\nXSS + traversal\nAPI abuse", BLUE),
        ("THEN", "ENTERPRISE", "IDS + EDR inputs\nmulti-tenancy\nhigh availability\ncompliance packs", GREEN),
    ]
    for i, (tag, head, body, color) in enumerate(roadmap):
        x = 800+i*10800
        d.rect(p, x, 3600, 9800, 8000, SURFACE, color, 180)
        d.pill(p, x+500, 4150, 1900, tag, color)
        d.text(p, x+500, 5450, 8500, 600, head, 18, WHITE, bold=True)
        d.text(p, x+500, 6800, 8500, 3100, body, 11, TEXT)
    d.line(p, 5200, 12700, 27000, 12700, MUTED, 35)
    for x, color in [(5000, CYAN), (15800, BLUE), (26600, GREEN)]:
        d.ellipse(p, x, 12400, 600, 600, color, color)
    d.text(p, 800, 14300, 30500, 600, "The ask: pilot partners, security feedback, and integration opportunities.", 17, WHITE, bold=True)
    d.text(p, 800, 15300, 30000, 400, "Sentinel AI — detect • understand • predict • respond", 9, CYAN, bold=True)


def main():
    desktop, process = connect()
    try:
        doc = desktop.loadComponentFromURL("private:factory/simpress", "_blank", 0, ())
        build(doc)
        doc.storeAsURL(PPTX.as_uri(), (prop("FilterName", "Impress MS PowerPoint 2007 XML"), prop("Overwrite", True)))
        doc.storeToURL(PDF.as_uri(), (prop("FilterName", "impress_pdf_Export"), prop("Overwrite", True)))
        doc.close(True)
    finally:
        process.terminate()
        process.wait(timeout=10)
    print(PPTX)
    print(PDF)


if __name__ == "__main__":
    main()
