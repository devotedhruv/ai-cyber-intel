#!/usr/bin/env python3
"""Generate the Sentinel AI redesigned pitch deck with LibreOffice UNO."""

from __future__ import annotations

import os
import subprocess
import tempfile
import time
from pathlib import Path

import uno
from com.sun.star.awt import Point, Size
from com.sun.star.beans import PropertyValue


ROOT = Path(__file__).resolve().parent
PPTX = ROOT / "Sentinel_AI_Redesigned_Pitch_Deck.pptx"
PDF = ROOT / "Sentinel_AI_Redesigned_Pitch_Deck.pdf"

W, H = 33867, 19050
BG = 0x06111F
SURFACE = 0x0B1C2D
SURFACE_2 = 0x10263A
GRID = 0x102437
WHITE = 0xF2F7FB
TEXT = 0xC8D6E3
MUTED = 0x71879A
CYAN = 0x20D6BD
BLUE = 0x4A9CFF
VIOLET = 0xA979FF
AMBER = 0xFFB547
RED = 0xFF536A
GREEN = 0x48E0A4


def prop(name, value):
    item = PropertyValue()
    item.Name = name
    item.Value = value
    return item


def connect():
    profile = Path(tempfile.mkdtemp(prefix="sentinel-ai-lo-"))
    process = subprocess.Popen([
        "soffice", "--headless", "--norestore", "--nodefault", "--nolockcheck",
        f"-env:UserInstallation={profile.as_uri()}",
        "--accept=socket,host=127.0.0.1,port=2002;urp;StarOffice.ComponentContext",
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    local = uno.getComponentContext()
    resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
    for _ in range(50):
        try:
            context = resolver.resolve("uno:socket,host=127.0.0.1,port=2002;urp;StarOffice.ComponentContext")
            desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)
            return desktop, process
        except Exception:
            time.sleep(0.2)
    process.terminate()
    raise RuntimeError("Could not connect to LibreOffice")


class Deck:
    def __init__(self, doc):
        self.doc = doc
        self.pages = doc.getDrawPages()
        self.index = 0

    def slide(self, section=""):
        if self.index == 0:
            page = self.pages.getByIndex(0)
        else:
            page = self.pages.insertNewByIndex(self.index)
        page.Width, page.Height = W, H
        self.index += 1
        self.rect(page, 0, 0, W, H, BG, BG)
        for x in range(0, W, 2200):
            self.line(page, x, 0, x, H, GRID, 18)
        for y in range(0, H, 2200):
            self.line(page, 0, y, W, y, GRID, 18)
        self.rect(page, 220, 0, 90, H, CYAN, CYAN)
        if section:
            self.text(page, 700, 430, 4200, 400, "SENTINEL AI", 10, CYAN, bold=True)
            self.text(page, W - 4800, 430, 4000, 400, section.upper(), 8, MUTED, align=2)
            self.text(page, W - 1250, H - 700, 500, 250, f"{self.index:02d}", 7, MUTED, align=2)
        return page

    def shape(self, page, service, x, y, w, h):
        item = self.doc.createInstance(service)
        item.Position = Point(int(x), int(y))
        item.Size = Size(int(w), int(h))
        page.add(item)
        return item

    def rect(self, page, x, y, w, h, fill, line=SURFACE_2, radius=0):
        item = self.shape(page, "com.sun.star.drawing.RectangleShape", x, y, w, h)
        item.FillColor = fill
        item.LineColor = line
        item.LineWidth = 28
        if radius:
            try: item.CornerRadius = radius
            except Exception: pass
        return item

    def ellipse(self, page, x, y, w, h, fill, line):
        item = self.shape(page, "com.sun.star.drawing.EllipseShape", x, y, w, h)
        item.FillColor = fill
        item.LineColor = line
        item.LineWidth = 45
        return item

    def line(self, page, x1, y1, x2, y2, color, width=35):
        item = self.shape(page, "com.sun.star.drawing.LineShape", x1, y1, x2-x1, y2-y1)
        item.LineColor = color
        item.LineWidth = width
        return item

    def text(self, page, x, y, w, h, value, size=16, color=TEXT, bold=False, align=0, font="Noto Sans"):
        item = self.shape(page, "com.sun.star.drawing.TextShape", x, y, w, h)
        item.String = value
        item.FillStyle = 0
        item.LineStyle = 0
        cursor = item.createTextCursor()
        cursor.gotoEnd(True)
        cursor.CharFontName = font
        cursor.CharHeight = float(size)
        cursor.CharColor = color
        cursor.CharWeight = 150.0 if bold else 100.0
        cursor.ParaAdjust = align
        try:
            item.TextAutoGrowHeight = False
            item.TextVerticalAdjust = 1
        except Exception:
            pass
        return item

    def title(self, page, headline, subtitle=""):
        self.text(page, 700, 1250, 30500, 1050, headline, 25, WHITE, bold=True)
        if subtitle:
            self.text(page, 710, 2280, 29200, 620, subtitle, 11, MUTED)

    def pill(self, page, x, y, w, label, color=CYAN):
        self.rect(page, x, y, w, 520, SURFACE, color, 160)
        self.text(page, x+120, y+85, w-240, 300, label.upper(), 7, color, bold=True, align=1)

    def card(self, page, x, y, w, h, label, headline, body, color=CYAN):
        self.rect(page, x, y, w, h, SURFACE, SURFACE_2, 140)
        self.rect(page, x, y, 65, h, color, color)
        self.text(page, x+360, y+300, w-620, 350, label.upper(), 7, color, bold=True)
        self.text(page, x+360, y+800, w-620, 700, headline, 15, WHITE, bold=True)
        self.text(page, x+360, y+1550, w-650, h-1800, body, 9, MUTED)

    def metric(self, page, x, y, w, value, label, color=CYAN):
        self.rect(page, x, y, w, 2100, SURFACE, SURFACE_2, 140)
        self.text(page, x+260, y+300, w-520, 800, value, 25, WHITE, bold=True)
        self.text(page, x+260, y+1230, w-520, 400, label.upper(), 8, color, bold=True)
        self.rect(page, x+260, y+1750, w-520, 35, color, color)

    def node(self, page, x, y, w, label, color=CYAN, sub=""):
        self.rect(page, x, y, w, 1000, SURFACE, color, 120)
        self.text(page, x+160, y+230, w-320, 350, label, 9, WHITE, bold=True, align=1)
        if sub:
            self.text(page, x+160, y+600, w-320, 220, sub, 6, MUTED, align=1)

    def arrow(self, page, x, y, w, color=CYAN):
        self.line(page, x, y, x+w, y, color, 45)
        self.line(page, x+w-180, y-120, x+w, y, color, 45)
        self.line(page, x+w-180, y+120, x+w, y, color, 45)


def build(doc):
    d = Deck(doc)

    # 1 — Cover
    p = d.slide()
    d.pill(p, 720, 1250, 3600, "AI-powered security operations", CYAN)
    d.text(p, 720, 2500, 20000, 1200, "SENTINEL", 44, WHITE, bold=True)
    d.text(p, 720, 3700, 8000, 1200, "AI", 44, CYAN, bold=True)
    d.text(p, 760, 5350, 17500, 1400, "Detect threats. Predict attacks.\nRespond intelligently.", 20, TEXT, bold=True)
    d.text(p, 760, 7800, 15000, 900, "A modular cyber threat intelligence and SOC platform that turns security telemetry into explainable decisions.", 12, MUTED)
    d.ellipse(p, 23000, 2900, 5200, 5200, SURFACE, CYAN)
    d.ellipse(p, 24100, 4000, 3000, 3000, BG, BLUE)
    d.text(p, 24600, 4870, 2000, 850, "AI", 27, CYAN, bold=True, align=1)
    for y, color in [(3300,CYAN),(4300,BLUE),(5300,VIOLET),(6300,GREEN)]:
        d.line(p, 28200, y, 31900, y-500, color, 45)
    d.text(p, 760, H-1700, 8500, 400, "PROJECT PITCH • 2026", 8, CYAN, bold=True)
    d.text(p, 760, H-1150, 11000, 350, "FASTAPI  •  REACT  •  POSTGRESQL  •  AI/ML  •  SOAR", 7, MUTED)

    # 2 — Problem
    p = d.slide("The problem")
    d.title(p, "Security teams see signals. They need decisions.", "Authentication events, alerts, threat intelligence, and incidents are often separated by tools and time.")
    d.card(p, 750, 3550, 9800, 7600, "01 / Fragmented", "Context breaks", "Logs, identities, IP reputation, detections, and response evidence live in disconnected systems.", RED)
    d.card(p, 12000, 3550, 9800, 7600, "02 / Overloaded", "Noise wins", "High-volume alerts lack prioritization, explainability, and a visible connection to business risk.", AMBER)
    d.card(p, 23250, 3550, 9800, 7600, "03 / Delayed", "Response waits", "Analysts spend time reconstructing evidence before they can contain or escalate a threat.", BLUE)
    d.pill(p, 750, 12350, 2400, "The gap", CYAN)
    d.text(p, 3500, 12320, 27000, 700, "A continuous, explainable loop—from security event to controlled response.", 15, WHITE, bold=True)

    # 3 — Solution
    p = d.slide("The solution")
    d.title(p, "One defensive pipeline. One operational view.", "Sentinel AI preserves identity, source, risk, and evidence as each signal moves through the platform.")
    labels = [("COLLECT",CYAN),("NORMALIZE",BLUE),("DETECT",RED),("PRIORITIZE",AMBER),("PREDICT",VIOLET),("RESPOND",GREEN)]
    x=850
    for i,(label,color) in enumerate(labels):
        d.node(p,x,4300,4300,label,color, f"STEP {i+1:02d}")
        if i < len(labels)-1: d.arrow(p,x+4300,4800,850,MUTED)
        x += 5200
    d.rect(p, 850, 6900, 31100, 3100, SURFACE_2, CYAN, 140)
    d.text(p, 1300, 7350, 7500, 400, "THE SENTINEL VALUE", 8, CYAN, bold=True)
    d.text(p, 1300, 8100, 29100, 850, "Faster understanding  •  Explainable risk  •  Predictive context  •  Auditable response", 17, WHITE, bold=True)
    d.text(p, 1300, 9250, 27000, 350, "A single security event remains traceable across logs, alerts, detections, paths, incidents, notifications, and reports.", 9, MUTED)

    # 4 — Verified proof
    p = d.slide("Live proof")
    d.title(p, "A threat story judges can see end-to-end", "The current implementation turns repeated authentication failures into visible, persisted security outcomes.")
    steps=[("01","LOGIN","Success and failure events capture user, IP, user agent, status, and time.",CYAN),("02","DETECT",">5 failures for the same username and IP inside five minutes.",AMBER),("03","SCORE","A transparent HIGH / 90 risk decision with behavior evidence.",RED),("04","RESPOND","Alert, threat, attack path, incident, notification, and report become visible.",GREEN)]
    y=3500
    for num,head,body,color in steps:
        d.ellipse(p,850,y,900,900,BG,color); d.text(p,1020,y+250,560,300,num,9,color,bold=True,align=1)
        d.line(p,1300,y+900,1300,y+1750,MUTED,30)
        d.text(p,2150,y+80,5000,400,head,11,WHITE,bold=True)
        d.text(p,2150,y+600,24500,550,body,9,MUTED)
        y += 2900
    d.pill(p, 27000, 3500, 4300, "Implemented + verified", GREEN)

    # 5 — Dashboard
    p = d.slide("SOC command center")
    d.title(p, "Built for the analyst's next decision", "The interface unifies monitoring, intelligence, detection, prediction, response, and reporting.")
    items=[("LIVE MONITORING","Authentication timeline, filters, status, device and source context.",CYAN),("THREAT INTELLIGENCE","Suspicious IPs, threat types, risk levels, and enrichment.",BLUE),("AI DETECTION","Risk score, confidence, and explainable behavior analysis.",AMBER),("ATTACK GRAPH","Possible progression from entry point to sensitive asset.",RED),("SOAR RESPONSE","Incident workflow, notifications, and defensive action state.",GREEN),("REPORTING","Live summary, archives, JSON and CSV exports.",CYAN)]
    for i,(head,body,color) in enumerate(items):
        col=i%3; row=i//3
        d.card(p,750+col*10800,3500+row*5100,9800,4300,"CAPABILITY",head,body,color)

    # 6 — Architecture
    p = d.slide("Architecture")
    d.title(p, "Modular by design. Integrated by a central security plane.", "Nine independently runnable phases keep domain ownership while the central API coordinates identity, data, and operations.")
    phases=[("P1","Foundation"),("P2","SOC UI"),("P3","Threat Intel"),("P4","AI Detection"),("P5","Attack Paths"),("P6","SOAR"),("P7","Integrations"),("P8","Operations"),("P9","AI Hunting")]
    for i,(num,label) in enumerate(phases):
        col=i%3; row=i//3; x=800+col*6900; y=3600+row*2600
        d.rect(p,x,y,6100,1900,SURFACE,SURFACE_2,120)
        d.text(p,x+260,y+250,900,300,num,7,CYAN,bold=True)
        d.text(p,x+260,y+850,5400,400,label,10,WHITE,bold=True)
    d.rect(p,22600,3600,9800,7100,SURFACE_2,BLUE,160)
    d.pill(p,23100,4100,3600,"Central security plane",BLUE)
    d.text(p,23100,5100,8300,700,"FastAPI Gateway",20,WHITE,bold=True)
    d.text(p,23100,6200,8000,2300,"Authentication + APIs\nDetection orchestration\nHealth + topology\nFault-tolerant aggregation\nPostgreSQL persistence",10,TEXT)
    d.pill(p,23100,9300,2200,"React",CYAN); d.pill(p,25600,9300,2600,"PostgreSQL",GREEN); d.pill(p,28500,9300,2400,"Docker",AMBER)

    # 7 — Trust boundary
    p = d.slide("Security by design")
    d.title(p, "The platform protects its own trust boundary", "Production-minded controls are implemented around identity, secrets, persistence, and defensive automation.")
    controls=[("PBKDF2","600,000 password-hashing iterations with a per-user salt.",CYAN),("TOKEN SAFETY","Random bearer tokens; only SHA-256 digests persist.",BLUE),("EXPIRY + LOGOUT","Expiring sessions and explicit server-side revocation.",VIOLET),("SECRET HYGIENE","Credentials supplied through environment configuration.",GREEN),("SAFE MIGRATION","Additive initialization preserves existing users and data.",AMBER),("AUDITABILITY","Success, failure, IP, user agent, reason, and time recorded.",RED)]
    for i,(head,body,color) in enumerate(controls):
        col=i%2; row=i//2
        d.card(p,800+col*16300,3500+row*3500,15300,2850,"CONTROL",head,body,color)

    # 8 — Detection
    p = d.slide("Detection engine")
    d.title(p, "Explainable detection before opaque automation", "Deterministic rules provide a testable baseline; AI modules extend analysis without hiding the evidence.")
    d.metric(p,800,3900,6500,"10 / 100","Normal activity",GREEN)
    d.metric(p,7900,3900,6500,"35–55","Suspicious pattern",AMBER)
    d.metric(p,15000,3900,6500,"90 / 100","Brute force",RED)
    d.rect(p,22500,3900,9800,6300,SURFACE_2,CYAN,160)
    d.text(p,23100,4450,8500,450,"WHY THIS SCORE?",8,CYAN,bold=True)
    d.text(p,23100,5300,8500,900,"Every decision keeps its evidence trail.",16,WHITE,bold=True)
    d.text(p,23100,6700,8200,2600,"• username and identity\n• source IP activity\n• attempt frequency\n• five-minute window\n• distinct usernames\n• failure reason",10,TEXT)
    d.text(p,800,11200,29000,550,"CURRENT VERIFIED RULE: same username + same IP + more than five failed attempts + five-minute window.",11,WHITE,bold=True)

    # 9 — Coverage
    p = d.slide("Detection coverage")
    d.title(p, "Honest coverage today. Extensible coverage tomorrow.", "Sentinel AI does not claim to detect every attack; it provides a modular path to broader evidence-based detection.")
    d.rect(p,800,3500,10500,10200,SURFACE,GREEN,160)
    d.pill(p,1300,4050,3600,"Implemented + verified",GREEN)
    d.text(p,1300,5200,9000,800,"Authentication threats",19,WHITE,bold=True)
    d.text(p,1300,6500,8700,4500,"• brute-force login\n• repeated failed attempts\n• suspicious login frequency\n• multiple usernames from one IP\n• identity/IP risk scoring\n• active-alert deduplication\n• threat and incident promotion",10,TEXT)
    d.rect(p,12150,3500,19900,10200,SURFACE,BLUE,160)
    d.pill(p,12650,4050,2800,"Roadmap modules",BLUE)
    columns=[("WEB","SQL injection\nXSS\ncommand injection\npath traversal\nSSRF\nmalicious upload",RED),("IDENTITY","credential stuffing\npassword spraying\nsession anomalies\nimpossible travel\nnew device/location",AMBER),("NETWORK + ENDPOINT","port scanning\nDDoS indicators\nDNS tunneling\nlateral movement\nransomware behavior\nC2 activity",VIOLET)]
    for i,(head,body,color) in enumerate(columns):
        x=12650+i*6250
        d.text(p,x,5400,5600,400,head,9,color,bold=True)
        d.text(p,x,6200,5500,4700,body,10,TEXT)
    d.text(p,12650,12400,18000,350,"ROADMAP ≠ CURRENT CLAIM",8,AMBER,bold=True)

    # 10 — Web blueprint
    p = d.slide("Web attack roadmap")
    d.title(p, "A safe blueprint for web-attack detection", "Sanitized server/WAF telemetry can extend the existing event pipeline without storing secrets or raw credentials.")
    flow=[("WEB / WAF","sanitized event",CYAN),("INGEST","validate schema",BLUE),("DETECT","rules + behavior",RED),("SCORE","confidence + risk",AMBER),("ALERT","evidence record",VIOLET),("RESPOND","approved action",GREEN)]
    x=700
    for i,(head,sub,color) in enumerate(flow):
        d.node(p,x,3900,4400,head,color,sub)
        if i<len(flow)-1:d.arrow(p,x+4400,4400,650,MUTED)
        x+=5050
    d.card(p,800,6900,9900,5800,"SQL INJECTION","Proposed signals","SQL operator anomalies, UNION patterns, comment markers, encoded payload attempts, database error bursts, abnormal parameter lengths.",RED)
    d.card(p,11900,6900,9900,5800,"CROSS-SITE SCRIPTING","Proposed signals","Script/event-handler patterns, encoded markup, repeated payload families, CSP/WAF evidence, and response anomalies.",AMBER)
    d.card(p,23000,6900,9900,5800,"OTHER WEB THREATS","Proposed signals","Traversal, command injection, SSRF, file inclusion, malicious upload, API abuse, XML-RPC abuse, and web-shell indicators.",VIOLET)

    # 11 — AI
    p = d.slide("AI + explainability")
    d.title(p, "AI augments evidence. It does not replace it.", "Phase 4 extends transparent rules with bounded anomaly analysis, classification, and confidence scoring.")
    d.ellipse(p,900,3800,7000,7000,SURFACE,VIOLET)
    d.ellipse(p,2250,5150,4300,4300,BG,CYAN)
    d.text(p,3000,6350,2800,650,"AI",28,VIOLET,bold=True,align=1)
    d.text(p,2400,7500,4000,350,"EXPLAINABLE CORE",8,CYAN,bold=True,align=1)
    ai=[("FEATURES","frequency • identity • IP • context",CYAN),("ANOMALY","deviation from known behavior",BLUE),("CLASSIFY","threat type + bounded severity",VIOLET),("EXPLAIN","human-readable reason + evidence",GREEN)]
    for i,(head,body,color) in enumerate(ai):
        d.card(p,9800+(i%2)*11200,3700+(i//2)*4300,10200,3600,"AI STAGE",head,body,color)
    d.text(p,9800,12600,22000,450,"Human-readable reasoning remains visible beside every score.",12,WHITE,bold=True)

    # 12 — Intel
    p = d.slide("Threat intelligence")
    d.title(p, "Detection becomes stronger when context travels with it", "Sentinel AI's modular intelligence services normalize external evidence and correlate it with internal events.")
    sources=[("IP","reputation",CYAN),("DOMAIN","reputation",BLUE),("URL","indicators",VIOLET),("HASH","malware IOC",RED),("CVE","exposure",AMBER)]
    x=850
    for i,(head,sub,color) in enumerate(sources):
        d.node(p,x,3800,5000,head,color,sub); x+=6250
    d.arrow(p,6200,6100,21000,CYAN)
    d.rect(p,9700,7000,14500,3300,SURFACE_2,CYAN,160)
    d.text(p,10300,7550,13300,500,"NORMALIZE  →  CORRELATE  →  ENRICH",17,WHITE,bold=True,align=1)
    d.text(p,10300,8550,13300,450,"IOC matching • reputation context • CVE intelligence • MITRE mapping",9,MUTED,align=1)
    d.pill(p,10700,11300,3100,"Evidence-led",GREEN); d.pill(p,14300,11300,3500,"Feed-aware",BLUE); d.pill(p,18300,11300,4100,"Fault tolerant",AMBER)

    # 13 — Attack path
    p = d.slide("Attack prediction")
    d.title(p, "Show what could happen next—not only what happened", "Attack-path context helps analysts connect an entry signal to possible privilege and asset exposure.")
    path=[("FAILED LOGINS",RED),("ACCOUNT RISK",AMBER),("PRIVILEGE RISK",VIOLET),("ASSET EXPOSURE",BLUE),("INCIDENT",GREEN)]
    x=850
    for i,(label,color) in enumerate(path):
        d.node(p,x,4800,5200,label,color,f"STAGE {i+1}")
        if i<len(path)-1:d.arrow(p,x+5200,5300,900,color)
        x+=6150
    d.rect(p,850,7400,29800,3500,SURFACE,SURFACE_2,160)
    d.text(p,1350,7900,8200,400,"ANALYST VALUE",8,CYAN,bold=True)
    d.text(p,1350,8750,28000,550,"Source identity  •  Possible progression  •  Risk propagation  •  Defensive recommendation",15,WHITE,bold=True)
    d.text(p,1350,9800,27500,350,"Prediction is presented as bounded context—not certainty—and remains linked to the originating evidence.",9,MUTED)

    # 14 — SOAR
    p = d.slide("SOAR response")
    d.title(p, "Automate the workflow. Keep control of the action.", "Sentinel AI records, prioritizes, and coordinates defensive response without blindly executing disruptive changes.")
    actions=[("CREATE","incident",CYAN),("PRIORITIZE","severity",AMBER),("NOTIFY","administrator",BLUE),("PREPARE","containment",VIOLET),("APPROVE","disruptive action",RED),("AUDIT","outcome",GREEN)]
    for i,(head,sub,color) in enumerate(actions):
        col=i%3; row=i//3
        d.card(p,800+col*10800,3500+row*4500,9800,3700,"WORKFLOW",head,sub,color)
    d.pill(p,800,13100,5100,"Human approval boundary",RED)
    d.text(p,6500,13100,25000,500,"Account locks, IP blocks, and other business-impacting actions require authorization.",11,WHITE,bold=True)

    # 15 — Reports
    p = d.slide("Reporting + data")
    d.title(p, "Security posture that is measurable and exportable", "Live summaries and generated reports reuse existing PostgreSQL evidence—without duplicate security tables.")
    d.metric(p,800,3600,5900,"LOGIN","total attempts",CYAN)
    d.metric(p,7200,3600,5900,"SUCCESS","authenticated",GREEN)
    d.metric(p,13600,3600,5900,"FAILED","denied",RED)
    d.metric(p,20000,3600,5900,"ALERTS","active",AMBER)
    d.metric(p,26400,3600,5900,"RISK","LOW–HIGH",VIOLET)
    d.rect(p,800,6700,30900,4400,SURFACE,SURFACE_2,160)
    d.text(p,1350,7200,5000,350,"REPORT CENTER",8,CYAN,bold=True)
    d.text(p,1350,8000,28000,550,"Daily Security  •  Threat Analysis  •  Incident Report  •  Archive",16,WHITE,bold=True)
    d.text(p,1350,9100,27000,450,"Authenticated API  →  PostgreSQL evidence  →  live cards  →  JSON / CSV exports",10,MUTED)
    d.pill(p,1350,10100,2200,"JSON",BLUE); d.pill(p,3900,10100,2200,"CSV",GREEN); d.pill(p,6450,10100,3200,"Auditable",CYAN)

    # 16 — Validation
    p = d.slide("Engineering evidence")
    d.title(p, "Validated as a working system—not a static concept", "The project includes executable services, persistence, protected APIs, a connected frontend, and repeatable tests.")
    proof=[("BUILD","React production bundle",CYAN),("COMPILE","FastAPI modules",BLUE),("TEST","report routes + summary",VIOLET),("RUN","Docker + PostgreSQL",AMBER),("VERIFY","authenticated 200 API",GREEN)]
    for i,(head,body,color) in enumerate(proof):
        d.card(p,700+i*6500,3900,5800,5000,"VERIFIED",head,body,color)
    d.rect(p,700,10200,31800,2300,SURFACE_2,GREEN,160)
    d.text(p,1200,10700,30000,400,"DEMO SUCCESS CRITERIA",8,GREEN,bold=True)
    d.text(p,1200,11400,30000,450,"Failed login → six attempts → HIGH alert → risk → attack path → notification → report",12,WHITE,bold=True)
    d.text(p,700,13700,30000,350,"No invented customer metrics. No unsupported accuracy claims. Every claim maps to code, API, database, or roadmap.",9,MUTED)

    # 17 — Roadmap
    p = d.slide("Roadmap")
    d.title(p, "A deliberate path from working prototype to broader defense", "Expand evidence sources and detections without rewriting the central architecture.")
    roadmap=[("NOW","HARDEN","RBAC • streaming • tests • observability • deployment",CYAN),("NEXT","EXPAND WEB","WordPress telemetry • SQLi • XSS • traversal • API abuse",BLUE),("SCALE","ENTERPRISE","IDS/EDR • multi-tenancy • HA • compliance • collaboration",GREEN)]
    for i,(tag,head,body,color) in enumerate(roadmap):
        x=800+i*10800
        d.rect(p,x,3900,9800,7500,SURFACE,color,180)
        d.pill(p,x+500,4400,1900,tag,color)
        d.text(p,x+500,5700,8500,700,head,19,WHITE,bold=True)
        d.text(p,x+500,7000,8500,2300,body,11,MUTED)
        d.ellipse(p,x+4400,12300,600,600,color,color)
    d.line(p,5200,12600,27000,12600,MUTED,35)

    # 18 — Closing
    p = d.slide("Closing")
    d.pill(p,760,1500,2200,"The mission",CYAN)
    d.text(p,760,3000,20500,2600,"Turn every security signal\ninto a confident response.", 34, WHITE, bold=True)
    d.text(p,780,6400,18200,1000,"Sentinel AI connects detection, understanding, prediction, and controlled response in one explainable SOC workflow.",13,MUTED)
    d.rect(p,23300,2900,7200,7500,SURFACE_2,CYAN,180)
    stages=[("DETECT",CYAN),("UNDERSTAND",BLUE),("PREDICT",AMBER),("RESPOND",GREEN)]
    y=3700
    for label,color in stages:
        d.text(p,24400,y,5000,450,label,11,color,bold=True,align=1)
        if y<8200:d.text(p,26300,y+650,1200,350,"↓",16,MUTED,bold=True,align=1)
        y+=1600
    d.text(p,760,H-1900,16500,400,"DETECT  •  UNDERSTAND  •  PREDICT  •  RESPOND",8,CYAN,bold=True)
    d.text(p,760,H-1200,9000,450,"Thank you  /  Questions",12,WHITE,bold=True)


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
