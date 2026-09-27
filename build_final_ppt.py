#!/usr/bin/env python3
"""Build BHOOMI_SIH_2026_Final.pptx — 6-slide official SIH 2026 format."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
import os

# ------------------------------------------------------------------
# Constants — design system
# ------------------------------------------------------------------
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

# Palette
PRIMARY = RGBColor(27, 58, 42)      # deep institutional green #1B3A2A
SECONDARY = RGBColor(15, 40, 54)    # dark navy #0F2847
ACCENT = RGBColor(191, 161, 95)     # warm gold #BFA15F
LIGHT_BG = RGBColor(240, 245, 240)  # very light green-gray
WHITE = RGBColor(255, 255, 255)
BLACK = RGBColor(30, 35, 38)
GRAY = RGBColor(120, 128, 132)
ALERT = RGBColor(180, 65, 45)        # discrepancy red
SUCCESS = RGBColor(46, 125, 75)     # success green

FONT = "Calibri"

def add_textbox(slide, left, top, width, height, text, font_size, bold=False,
                color=BLACK, align=PP_ALIGN.LEFT, font_name=FONT):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = font_name
    p.alignment = align
    return txBox

def add_rounded_rect(slide, left, top, width, height, fill_color, line_color=SECONDARY, line_width=Pt(0.5)):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.color.rgb = line_color
    shape.line.width = line_width
    shape.adjustments[0] = 0.08  # corner radius
    return shape

def add_rect(slide, left, top, width, height, fill_color, line_color=SECONDARY, line_width=Pt(0.5)):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.color.rgb = line_color
    shape.line.width = line_width
    return shape

def add_circle(slide, left, top, diameter, fill_color, line_color=SECONDARY):
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, diameter, diameter)
    shape.fill.solid(); shape.fill.fore_color.rgb = fill_color
    shape.line.color.rgb = line_color; shape.line.width = Pt(1)
    return shape

def add_arrow(slide, left, top, width=Inches(0.6), height=Inches(0.08), color=ACCENT):
    # simple horizontal arrow using thin rounded rect
    s = add_rounded_rect(slide, left, top, width, height, color, color, Pt(0))
    return s

def add_icon_circle(slide, left, top, d, fill, icon_text, font_size=8):
    c = add_circle(slide, left, top, d, fill, PRIMARY)
    add_textbox(slide, left, top, d, d, icon_text, font_size, bold=True,
                color=WHITE, align=PP_ALIGN.CENTER)
    return c

# ------------------------------------------------------------------
# Presentation setup
# ------------------------------------------------------------------
prs = Presentation()
prs.slide_width = SLIDE_WIDTH
prs.slide_height = SLIDE_HEIGHT

# ------------------------------------------------------------------
# Helper: page header bar (consistent across all slides except title)
# ------------------------------------------------------------------
def add_header_bar(slide, title_text, subtitle_text=""):
    # Dark green top bar spanning full width, ~0.85 in height
    bar = add_rect(slide, Inches(0), Inches(0), SLIDE_WIDTH, Inches(0.85), PRIMARY, PRIMARY)
    # Small gold accent line at bottom of bar
    accent = add_rect(slide, Inches(0), Inches(0.85), SLIDE_WIDTH, Inches(0.06), ACCENT, ACCENT)
    # Title text inside bar
    add_textbox(slide, Inches(0.35), Inches(0.15), Inches(9.5), Inches(0.35),
                title_text, 20, bold=True, color=WHITE)
    if subtitle_text:
        add_textbox(slide, Inches(0.35), Inches(0.52), Inches(9.5), Inches(0.25),
                    subtitle_text, 9, color=RGBColor(210, 215, 208))
    # Right side: official format marker
    add_textbox(slide, Inches(11.2), Inches(0.28), Inches(2.0), Inches(0.35),
                "SIH 2026  ·  SIH26018  ·  Smart Automation", 7, bold=False,
                color=RGBColor(190, 200, 195), align=PP_ALIGN.RIGHT)

# ===================================================================
# SLIDE 1 — TITLE (Official SIH Format)
# ===================================================================
slide1 = prs.slides.add_slide(prs.slide_layouts[6])  # blank

# Background subtle gradient feel — large light green shape at bottom-right
bg_shape = add_rounded_rect(slide1, Inches(8.5), Inches(4.2), Inches(5.0), Inches(3.5),
                            LIGHT_BG, LIGHT_BG, Pt(0))

# Large deep green header band at top (~1.6 in)
header_bg = add_rect(slide1, Inches(0), Inches(0), SLIDE_WIDTH, Inches(1.7), PRIMARY, PRIMARY)
# Gold thin line under header
add_rect(slide1, Inches(0), Inches(1.7), SLIDE_WIDTH, Inches(0.08), ACCENT, ACCENT)

# Left decorative vertical strip
strip = add_rect(slide1, Inches(0.35), Inches(2.2), Inches(0.06), Inches(4.2), ACCENT, ACCENT)

# Main title block (left-aligned in the white space below header)
add_textbox(slide1, Inches(0.6), Inches(2.0), Inches(10.5), Inches(0.8),
            "BHOOMI  ·  BhuSure", 32, bold=True, color=PRIMARY)
add_textbox(slide1, Inches(0.6), Inches(2.75), Inches(10.5), Inches(0.5),
            "Intelligent Land Record Digitization & Validation System", 16,
            bold=False, color=SECONDARY)

# Subtitle with problem info
subtitle_box = add_rounded_rect(slide1, Inches(0.6), Inches(3.35), Inches(9.5), Inches(0.9), LIGHT_BG, LIGHT_BG)
add_textbox(slide1, Inches(0.85), Inches(3.45), Inches(9.0), Inches(0.35),
            "Problem Statement ID  SIH26018   ·   Theme: Smart Automation   ·   Category: Software", 10, color=SECONDARY)
add_textbox(slide1, Inches(0.85), Inches(3.72), Inches(9.0), Inches(0.45),
            "Converts scanned registers, handwritten pages, PDFs and cadastral maps into structured, validated, GIS-linked digital records — with government reviewers holding final authority.", 9, color=GRAY)

# Three transformation icons horizontally centered in lower area
icons_y = Inches(4.9)
icons_d = Inches(0.9)
labels = [
    ("LEGACY\nRECORD", "Scanned / Handwritten / PDF / Image"),
    ("BHOOMI\nINTELLIGENCE", "AI OCR · Validation · GIS · Audit"),
    ("VERIFIED\nDIGITAL RECORD", "Structured · Searchable · Auditable")
]
icons_fill = [SECONDARY, PRIMARY, SUCCESS]
start_x = Inches(1.0)
spacing = Inches(3.9)
for i, (label, desc) in enumerate(labels):
    cx = start_x + i * spacing
    # Circle icon
    c = add_circle(slide1, cx, icons_y, icons_d, icons_fill[i], PRIMARY)
    # Small white icon text in circle
    add_textbox(slide1, cx, icons_y + Inches(0.22), icons_d, Inches(0.3),
                label, 8, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    # Arrow between icons
    if i < 2:
        arrow_x = cx + icons_d + Inches(0.15)
        add_rounded_rect(slide1, arrow_x, icons_y + icons_d/2 - Inches(0.06),
                         Inches(0.7), Inches(0.12), ACCENT, ACCENT)
        # Arrow head triangle using small shape (simplified as circle)
        add_circle(slide1, arrow_x + Inches(0.55), icons_y + icons_d/2, Inches(0.22), ACCENT, ACCENT)
    # Description below
    add_textbox(slide1, cx - Inches(0.7), icons_y + icons_d + Inches(0.15),
                Inches(1.8), Inches(0.55), desc, 8, color=GRAY, align=PP_ALIGN.CENTER)

# Team / footer info
add_textbox(slide1, Inches(0.6), Inches(6.95), Inches(12), Inches(0.35),
            "Team Shadow Slayers  ·  Ministry of Rural Development  ·  Repository: github.com/fresherscomputersc-hash/BHOOMI",
            8, color=GRAY, align=PP_ALIGN.CENTER)

# Small badge top-right
badge = add_rounded_rect(slide1, Inches(11.8), Inches(1.9), Inches(1.25), Inches(0.35), ACCENT, ACCENT)
add_textbox(slide1, Inches(11.8), Inches(2.0), Inches(1.25), Inches(0.3),
            "SIH 2026", 10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

# ------------------------------------------------------------------
# SLIDE 2 — IDEA TITLE / PROPOSED SOLUTION (Official Section 2)
# ------------------------------------------------------------------
slide2 = prs.slides.add_slide(prs.slide_layouts[6])
add_header_bar(slide2, "PROPOSED SOLUTION  ·  IDEA TITLE",
               "What BHOOMI does · How it transforms legacy land records · Key innovations")

# Background card area (light green)
main_bg = add_rounded_rect(slide2, Inches(0.35), Inches(1.05), Inches(12.65), Inches(5.85), LIGHT_BG, LIGHT_BG)

# LEFT: Legacy Sources (vertical column of cards)
left_cards = [
    ("SCANNED REGISTER", "Odisha 39-A, UP Khatauni, MP Khasra, Bihar Khatiyan"),
    ("HANDWRITTEN PAGE", "Hindi · Odia · English mixed-script pages"),
    ("PDF / IMAGE", "Multi-page documents, stamps, maps"),
    ("CADASTRAL MAP", "GeoJSON parcel polygons, survey sheets"),
]
y_start = Inches(1.35)
card_h = Inches(0.92)
card_gap = Inches(0.12)
for i, (title, desc) in enumerate(left_cards):
    y = y_start + i * (card_h + card_gap)
    card = add_rounded_rect(slide2, Inches(0.6), y, Inches(2.6), card_h, PRIMARY, PRIMARY)
    # Small gold left border
    add_rect(slide2, Inches(0.6), y, Inches(0.06), card_h, ACCENT, ACCENT)
    add_textbox(slide2, Inches(0.85), y + Inches(0.1), Inches(2.25), Inches(0.3),
                title, 10, bold=True, color=WHITE)
    add_textbox(slide2, Inches(0.85), y + Inches(0.45), Inches(2.25), Inches(0.4),
                desc, 7, color=RGBColor(200, 210, 205))

# CENTER: Large pipeline visual
pipe_title = add_textbox(slide2, Inches(3.4), Inches(1.25), Inches(5.5), Inches(0.35),
                         "BHOOMI END-TO-END PIPELINE", 14, bold=True, color=PRIMARY, align=PP_ALIGN.CENTER)

# Pipeline stages (vertical flow with connecting arrows)
stages = [
    ("DOCUMENT\nUPLOAD", "PDF / Image / Scan"),
    ("CV PREPROCESS", "Deskew · Denoise · CLAHE"),
    ("OCR / HTR", "Tesseract 5.5  ·  eng+hin+ori"),
    ("FIELD EXTRACTION", "17 fields · 5 doc profiles"),
    ("CONFIDENCE FUSION", "0.45·OCR + 0.30·Pat + 0.15·Prox + 0.10·Cons"),
    ("VALIDATION ENGINE", "BR-1…BR-10 · GIS · Cross-DB"),
    ("HUMAN REVIEW", "Approve / Reject / Escalate"),
    ("AUDIT TRAIL", "SHA-256 chain · Immutable"),
]
pipe_start_y = Inches(1.75)
pipe_box_w = Inches(2.6)
pipe_box_h = Inches(0.42)
for i, (label, desc) in enumerate(stages):
    y = pipe_start_y + i * Inches(0.55)
    fill = PRIMARY if i % 2 == 0 else SECONDARY
    # Stage box
    box = add_rounded_rect(slide2, Inches(4.0), y, pipe_box_w, pipe_box_h, fill, fill)
    # Small gold left border
    add_rect(slide2, Inches(4.0), y, Inches(0.05), pipe_box_h, ACCENT, ACCENT)
    add_textbox(slide2, Inches(4.15), y + Inches(0.04), pipe_box_w - Inches(0.15), Inches(0.2),
                label, 9, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    # Description below box (small)
    add_textbox(slide2, Inches(4.05), y + pipe_box_h + Inches(0.01), pipe_box_w, Inches(0.13),
                desc, 6, color=GRAY, align=PP_ALIGN.CENTER)
    # Connector line to next stage
    if i < len(stages) - 1:
        conn_y = y + pipe_box_h + Inches(0.01)
        add_rect(slide2, Inches(5.28), conn_y, Inches(0.03), Inches(0.11), ACCENT, ACCENT)

# Small embedded image of clean document at bottom center
img1_path = "data/samples/sample_01_ror_clean.png"
if os.path.exists(img1_path):
    slide2.shapes.add_picture(img1_path, Inches(4.2), Inches(6.55), Inches(1.6), Inches(0.7))
    add_textbox(slide2, Inches(4.2), Inches(7.18), Inches(1.6), Inches(0.2),
                "Real document: Odisha RoR  ·  Clean scan", 7, color=GRAY, align=PP_ALIGN.CENTER)

# RIGHT COLUMN: Key innovation cards (4 cards stacked)
right_x = Inches(7.2)
innovations = [
    ("MULTILINGUAL OCR", "English · Hindi · Odia  ·  Script-routed second pass (39-A → Oriya)", ACCENT),
    ("FIELD CONFIDENCE", "Per-word confidence · Fusion formula · Auto-review routing < 70%", SUCCESS),
    ("GIS VERIFICATION", "Cadastral polygon matching · Area reconciliation · Discrepancy BR-9", PRIMARY),
    ("HUMAN-IN-THE-LOOP", "Government reviewer holds final authority · HTTP 409 blocks approval with open findings", ALERT),
]
for i, (title, desc, col) in enumerate(innovations):
    y = Inches(1.35) + i * Inches(1.18)
    card = add_rounded_rect(slide2, right_x, y, Inches(3.4), Inches(0.95), LIGHT_BG, LIGHT_BG)
    # Left color stripe
    add_rect(slide2, right_x, y, Inches(0.06), Inches(0.95), col, col)
    # Title with same color
    add_textbox(slide2, right_x + Inches(0.2), y + Inches(0.08), Inches(3.0), Inches(0.3),
                title, 11, bold=True, color=col)
    add_textbox(slide2, right_x + Inches(0.2), y + Inches(0.4), Inches(3.0), Inches(0.5),
                desc, 8, color=BLACK)

# Bottom summary line
add_textbox(slide2, Inches(0.6), Inches(7.05), Inches(12), Inches(0.3),
            "NOT AN OCR WRAPPER — the complete value chain: Document → Intelligence → Validation → GIS → Human Review → Auditable Record",
            9, bold=True, color=SECONDARY, align=PP_ALIGN.CENTER)

# ------------------------------------------------------------------
# SLIDE 3 — TECHNICAL APPROACH (Official Section 3)
# ------------------------------------------------------------------
slide3 = prs.slides.add_slide(prs.slide_layouts[6])
add_header_bar(slide3, "TECHNICAL APPROACH  ·  ARCHITECTURE & PIPELINE",
               "Native architecture diagram · AI pipeline · Real screenshots · Technology stack")

# Main content area split: top = system architecture, bottom = AI pipeline + screenshots
# ------------------------------------------------------------------
# TOP HALF — System Architecture (visual diagram, NOT text boxes)
arch_title = add_textbox(slide3, Inches(0.35), Inches(1.0), Inches(6), Inches(0.3),
                         "BHOOMI SYSTEM ARCHITECTURE", 13, bold=True, color=PRIMARY)

# Architecture nodes arranged in layers
# Layer labels on left
layers = [
    ("SOURCES", "RoR · PATA · PDF · Image · Map"),
    ("INGESTION", "Upload · Hashing · Dedup · Quality"),
    ("DOCUMENT\nINTELLIGENCE", "CV Preprocess · OCR/HTR · Layout · Extraction"),
    ("VALIDATION", "BR-1…BR-10 · Confidence · Cross-DB · GIS"),
    ("REVIEW", "Government Official · Approve / Reject"),
    ("OUTPUT", "Verified Record · Audit Chain · MIS"),
]

# We'll draw nodes as rounded rectangles in a vertical stack, with horizontal flow arrows
node_colors = [SECONDARY, SECONDARY, PRIMARY, PRIMARY, ACCENT, SUCCESS]
node_w, node_h = Inches(2.8), Inches(0.55)
start_x = Inches(3.0)
start_y = Inches(1.35)

# Draw layer cards vertically but offset for flow
for i, (label, desc) in enumerate(layers):
    y = start_y + i * Inches(0.62)
    # Main node
    node = add_rounded_rect(slide3, start_x, y, node_w, node_h, node_colors[i], node_colors[i])
    # Small gold left accent
    add_rect(slide3, start_x, y, Inches(0.05), node_h, ACCENT, ACCENT)
    # Label (bold, white)
    add_textbox(slide3, start_x + Inches(0.15), y + Inches(0.06), node_w - Inches(0.25), Inches(0.22),
                label, 9, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_textbox(slide3, start_x + Inches(0.15), y + Inches(0.28), node_w - Inches(0.25), Inches(0.2),
                desc, 6, color=RGBColor(210, 215, 210), align=PP_ALIGN.CENTER)
    # Connector arrow down to next (small vertical line + arrowhead)
    if i < len(layers) - 1:
        arrow_y = y + node_h + Inches(0.01)
        add_rect(slide3, start_x + node_w/2 - Inches(0.03), arrow_y, Inches(0.06), Inches(0.10), ACCENT, ACCENT)
        # Arrowhead circle
        add_circle(slide3, start_x + node_w/2 - Inches(0.1), arrow_y + Inches(0.10), Inches(0.2), ACCENT, ACCENT)

# Right side of architecture — user roles and database
users_box = add_rounded_rect(slide3, Inches(6.6), Inches(1.35), Inches(2.5), Inches(3.2), LIGHT_BG, LIGHT_BG)
add_textbox(slide3, Inches(6.75), Inches(1.45), Inches(2.2), Inches(0.3),
            "USER ROLES & DATA", 11, bold=True, color=PRIMARY)
# User roles as small cards
roles = [
    ("OPERATOR", "Upload · Queue view"),
    ("REVIEWER", "Correct · Approve · Block"),
    ("SUPERVISOR", "Dashboard · Assign · Export"),
    ("AUDITOR", "Audit trail · Reports"),
]
for i, (r, d) in enumerate(roles):
    y = Inches(1.9) + i * Inches(0.55)
    rcard = add_rounded_rect(slide3, Inches(6.75), y, Inches(2.2), Inches(0.4), SECONDARY, SECONDARY)
    add_textbox(slide3, Inches(6.9), y + Inches(0.06), Inches(0.9), Inches(0.2), r, 9, bold=True, color=WHITE)
    add_textbox(slide3, Inches(7.55), y + Inches(0.08), Inches(1.2), Inches(0.2), d, 7, color=RGBColor(210, 215, 210))

# Database cylinder symbol (simple vertical rounded rect)
db_shape = add_rounded_rect(slide3, Inches(9.45), Inches(1.55), Inches(0.8), Inches(2.4), PRIMARY, PRIMARY)
add_textbox(slide3, Inches(9.45), Inches(2.05), Inches(0.8), Inches(0.35),
            "SQLITE /\nPOSTGRES", 7, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_textbox(slide3, Inches(9.45), Inches(2.6), Inches(0.8), Inches(0.8),
            "14 Tables\nAudit Chain\nRecord Store\nGIS Layer", 6, color=RGBColor(200, 210, 205), align=PP_ALIGN.CENTER)

# Security boundary line (dashed feel using small dashes) — simplified as thin rectangle
security_line = add_rect(slide3, Inches(12.2), Inches(1.35), Inches(0.05), Inches(3.6), ACCENT, ACCENT)
security_text = add_textbox(slide3, Inches(12.25), Inches(5.05), Inches(0.7), Inches(0.3),
                           "SECURITY\nRBAC · Argon2", 6, bold=True, color=ACCENT, align=PP_ALIGN.CENTER)

# ------------------------------------------------------------------
# BOTTOM HALF — AI Processing Pipeline + Evidence Screenshots
# ------------------------------------------------------------------
# Pipeline header
pipe_header = add_textbox(slide3, Inches(0.35), Inches(4.75), Inches(6), Inches(0.25),
                          "AI DOCUMENT PROCESSING PIPELINE", 12, bold=True, color=PRIMARY)

# Pipeline stages (horizontal flow with arrows)
pipeline_stages = [
    ("DOCUMENT", "Scanned page / PDF"),
    ("PREPROCESS", "OpenCV: deskew, denoise"),
    ("LAYOUT", "Region detection"),
    ("OCR / HTR", "Tesseract 5.5 · eng+hin+ori"),
    ("EXTRACTION", "17 canonical fields"),
    ("CONFIDENCE", "Per-field scoring"),
    ("VALIDATION", "BR rules + GIS"),
    ("VERIFIED", "Auditable record"),
]

# Place pipeline stages in a row with small rounded rects
pipe_y = Inches(5.15)
pipe_box_w = Inches(1.35)
pipe_box_h = Inches(0.55)
for i, (label, desc) in enumerate(pipeline_stages):
    x = Inches(0.4) + i * Inches(1.55)
    fill = PRIMARY if i % 2 == 0 else SECONDARY
    box = add_rounded_rect(slide3, x, pipe_y, pipe_box_w, pipe_box_h, fill, fill)
    add_rect(slide3, x, pipe_y, Inches(0.05), pipe_box_h, ACCENT, ACCENT)
    add_textbox(slide3, x + Inches(0.08), pipe_y + Inches(0.05), pipe_box_w - Inches(0.1), Inches(0.2),
                label, 7, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_textbox(slide3, x, pipe_y + pipe_box_h + Inches(0.02), pipe_box_w, Inches(0.15),
                desc, 6, color=GRAY, align=PP_ALIGN.CENTER)
    # Small arrow between stages
    if i < len(pipeline_stages) - 1:
        arrow_x = x + pipe_box_w + Inches(0.01)
        add_rounded_rect(slide3, arrow_x, pipe_y + pipe_box_h/2 - Inches(0.04), Inches(0.18), Inches(0.08), ACCENT, ACCENT)

# Embedded screenshot / evidence area at bottom right
# Show clean document + annotated result side by side
img1_path = "data/samples/sample_01_ror_clean.png"
img2_path = "data/processed/page_annotated.png"
if os.path.exists(img1_path):
    slide3.shapes.add_picture(img1_path, Inches(8.2), Inches(5.85), Inches(1.9), Inches(1.05))
    add_textbox(slide3, Inches(8.2), Inches(6.92), Inches(1.9), Inches(0.18),
                "CLEAN SCAN — Real Odisha RoR", 7, bold=True, color=SECONDARY, align=PP_ALIGN.CENTER)
if os.path.exists(img2_path):
    slide3.shapes.add_picture(img2_path, Inches(10.15), Inches(5.85), Inches(2.0), Inches(1.05))
    add_textbox(slide3, Inches(10.15), Inches(6.92), Inches(2.0), Inches(0.18),
                "ANNOTATED — OCR detection results", 7, bold=True, color=SECONDARY, align=PP_ALIGN.CENTER)

# Technology stack footer (small cards)
tech_stack = [
    "FastAPI · SQLAlchemy", "OpenCV · Tesseract 5.5", "Shapely · rapidfuzz",
    "spaCy · HF XLM-R (pilot)", "Argon2 · RBAC", "Vanilla JS · Inline SVG"
]
tech_y = Inches(7.0)
tech_h = Inches(0.35)
for i, tech in enumerate(tech_stack):
    tx = Inches(0.4) + i * Inches(2.1)
    # Small rounded tech chip
    chip = add_rounded_rect(slide3, tx, tech_y, Inches(2.0), tech_h, LIGHT_BG, LIGHT_BG)
    add_textbox(slide3, tx + Inches(0.1), tech_y + Inches(0.08), Inches(1.8), Inches(0.2),
                tech, 7, bold=False, color=SECONDARY, align=PP_ALIGN.CENTER)

# ------------------------------------------------------------------
# SLIDE 4 — FEASIBILITY & VIABILITY (Official Section 4)
# ------------------------------------------------------------------
slide4 = prs.slides.add_slide(prs.slide_layouts[6])
add_header_bar(slide4, "FEASIBILITY & VIABILITY  ·  EVIDENCE & RISK",
               "Measured results · Real documents · Tested rules · Security · Human-in-the-loop")

# LEFT: Evidence metrics (structured cards in a column)
ev_title = add_textbox(slide4, Inches(0.35), Inches(1.0), Inches(3.5), Inches(0.3),
                       "MEASURED EVIDENCE  ·  PROTOTYPE", 12, bold=True, color=PRIMARY)

evidence_cards = [
    ("165 TESTS", "Local / 168 on EC2  ·  All green", SUCCESS),
    ("26 DOCUMENTS", "6 demo + 5 stress + 5 Hindi + 5 English + 5 real Bhulekh RoRs", PRIMARY),
    ("79–84% OCR", "Real Odisha scans · Multi-script pages", ACCENT),
    ("15/15 BYTE-ID", "Deterministic reruns · No drift (Groq-off core)", SECONDARY),
    ("< 1 s/RECORD", "Validation latency · 15–127 s/doc (2 vCPU)", ALERT),
]
for i, (label, desc, col) in enumerate(evidence_cards):
    y = Inches(1.35) + i * Inches(0.95)
    card = add_rounded_rect(slide4, Inches(0.35), y, Inches(3.4), Inches(0.75), LIGHT_BG, LIGHT_BG)
    add_rect(slide4, Inches(0.35), y, Inches(0.08), Inches(0.75), col, col)
    # Large metric number
    add_textbox(slide4, Inches(0.6), y + Inches(0.1), Inches(2.0), Inches(0.25),
                label, 13, bold=True, color=col)
    # Description
    add_textbox(slide4, Inches(0.6), y + Inches(0.38), Inches(2.9), Inches(0.3),
                desc, 7, color=BLACK)

# CENTER LEFT: Real screenshot of clean document (larger)
img_path = "data/samples/sample_01_ror_clean.png"
if os.path.exists(img_path):
    slide4.shapes.add_picture(img_path, Inches(4.0), Inches(1.3), Inches(2.2), Inches(3.3))
    add_textbox(slide4, Inches(4.0), Inches(4.65), Inches(2.2), Inches(0.2),
                "REAL DOCUMENT  ·  Odisha RoR (Clean)", 8, bold=True, color=SECONDARY, align=PP_ALIGN.CENTER)
    # Small annotation callouts (text only)
    add_textbox(slide4, Inches(6.3), Inches(2.0), Inches(1.6), Inches(0.25),
                "District: Khordha  ·  Khasra: 118/2", 7, color=GRAY)
    add_textbox(slide4, Inches(6.3), Inches(2.25), Inches(1.6), Inches(0.25),
                "Area: 1.14 acre  ·  Owner: Prafulla Kumar Sahoo", 7, color=GRAY)

# CENTER RIGHT: Human-in-the-loop workflow (visual diagram)
hit_title = add_textbox(slide4, Inches(6.45), Inches(1.3), Inches(3.0), Inches(0.3),
                        "HUMAN-IN-THE-LOOP WORKFLOW", 11, bold=True, color=PRIMARY)
# Workflow stages vertically
hit_stages = [
    ("AI EXTRACTION", "Field confidence calculated"),
    ("CONFIDENCE CHECK", "Low < 70% → Mandatory review"),
    ("REVIEWER QUEUE", "Government officer assigned"),
    ("VERIFY / CORRECT", "Evidence shown; corrections captured"),
    ("APPROVE / REJECT", "Server refuses (HTTP 409) if critical open"),
    ("AUDIT LOG", "Old + new value · Hash added"),
]
hit_colors = [SECONDARY, ACCENT, PRIMARY, SUCCESS, ALERT, SECONDARY]
for i, (label, desc) in enumerate(hit_stages):
    y = Inches(1.8) + i * Inches(0.55)
    # Small rounded rect
    node = add_rounded_rect(slide4, Inches(6.6), y, Inches(2.3), Inches(0.4), hit_colors[i], hit_colors[i])
    add_rect(slide4, Inches(6.6), y, Inches(0.05), Inches(0.4), ACCENT, ACCENT)
    add_textbox(slide4, Inches(6.75), y + Inches(0.05), Inches(2.0), Inches(0.18),
                label, 9, bold=True, color=WHITE)
    add_textbox(slide4, Inches(6.75), y + Inches(0.22), Inches(2.0), Inches(0.15),
                desc, 6, color=RGBColor(210, 215, 210))
    if i < len(hit_stages) - 1:
        arrow_y = y + Inches(0.4) + Inches(0.005)
        add_rect(slide4, Inches(7.8), arrow_y, Inches(0.03), Inches(0.1), ACCENT, ACCENT)
        add_circle(slide4, Inches(7.8) - Inches(0.08), arrow_y + Inches(0.10), Inches(0.16), ACCENT, ACCENT)

# RIGHT COLUMN: Security & Audit visual + Risk cards
security_title = add_textbox(slide4, Inches(9.6), Inches(1.3), Inches(3.3), Inches(0.3),
                             "SECURITY  ·  AUDIT  ·  RISK", 12, bold=True, color=PRIMARY)

# Audit chain visual (3 linked boxes with hash connections)
chain_start_x = Inches(9.75)
chain_y = Inches(1.8)
chain_w = Inches(0.85)
chain_h = Inches(0.45)
chain_items = [
    ("RECORD 01", "SHA-256"),
    ("RECORD 02", "Prev Hash"),
    ("RECORD 03", "Tamper Detected?"),
]
for i, (label, sub) in enumerate(chain_items):
    x = chain_start_x + i * Inches(0.95)
    box = add_rounded_rect(slide4, x, chain_y, chain_w, chain_h, PRIMARY, PRIMARY)
    add_textbox(slide4, x, chain_y + Inches(0.04), chain_w, Inches(0.2),
                label, 7, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_textbox(slide4, x, chain_y + Inches(0.24), chain_w, Inches(0.15),
                sub, 6, color=RGBColor(190, 200, 195), align=PP_ALIGN.CENTER)
    if i < 2:
        conn_x = x + chain_w + Inches(0.01)
        add_rounded_rect(slide4, conn_x, chain_y + chain_h/2 - Inches(0.02),
                         Inches(0.15), Inches(0.04), ACCENT, ACCENT)

# Audit explanation below chain
audit_desc = add_rounded_rect(slide4, Inches(9.6), Inches(2.65), Inches(3.3), Inches(0.55), LIGHT_BG, LIGHT_BG)
add_textbox(slide4, Inches(9.75), Inches(2.7), Inches(3.0), Inches(0.45),
            "Every AI decision and every human correction writes one append-only row. Each row stores SHA-256 of previous row — tampering breaks the chain, detectable via verify_chain() (FR-12).", 7, color=BLACK)

# Risk cards (2 cards stacked) — show only implemented risks clearly
risk_cards = [
    ("RISK: INVENTED DATA", "Anti-hallucination contracts per doc type (e.g., plot 417 is NOT a khasra; khatiyan 18 is NOT a khata). AI never writes back without reviewer approval.", SUCCESS),
    ("RISK: GARBLAGED OCR", "Script-routed second pass + confidence bands. Any result < 70% is routed to mandatory human review. Zero crashes on adversarial set (36.8% accuracy, 100% routed to review).", ALERT),
]
for i, (title, desc, col) in enumerate(risk_cards):
    y = Inches(3.35) + i * Inches(1.0)
    card = add_rounded_rect(slide4, Inches(9.6), y, Inches(3.3), Inches(0.85), LIGHT_BG, LIGHT_BG)
    add_rect(slide4, Inches(9.6), y, Inches(0.08), Inches(0.85), col, col)
    add_textbox(slide4, Inches(9.8), y + Inches(0.08), Inches(2.9), Inches(0.25),
                title, 9, bold=True, color=col)
    add_textbox(slide4, Inches(9.8), y + Inches(0.35), Inches(2.9), Inches(0.45),
                desc, 7, color=BLACK)

# ------------------------------------------------------------------
# SLIDE 5 — IMPACT & BENEFITS (Official Section 5)
# ------------------------------------------------------------------
slide5 = prs.slides.add_slide(prs.slide_layouts[6])
add_header_bar(slide5, "IMPACT & BENEFITS  ·  BEFORE → AFTER · SCALE",
               "Revenue officers · Auditors · Governance · Scalability path · Real impact metrics")

# LEFT: Before vs After comparison (visual columns)
before_title = add_textbox(slide5, Inches(0.35), Inches(1.05), Inches(5.0), Inches(0.25),
                           "BEFORE  →  AFTER  ·  THE TRANSFORMATION", 12, bold=True, color=PRIMARY)

# Before column
before_col = add_rounded_rect(slide5, Inches(0.35), Inches(1.35), Inches(2.6), Inches(4.4), LIGHT_BG, LIGHT_BG)
add_textbox(slide5, Inches(0.5), Inches(1.45), Inches(2.3), Inches(0.25),
            "LEGACY PROCESS", 11, bold=True, color=ALERT, align=PP_ALIGN.CENTER)
before_items = [
    "Paper registers / handwritten pages",
    "Manual reading & entry",
    "No structured fields",
    "No cross-database check",
    "No GIS verification",
    "No audit trail",
    "Inconsistent formats across states",
    "High error rate · Slow review",
]
for i, item in enumerate(before_items):
    y = Inches(1.85) + i * Inches(0.4)
    # Small red dot
    add_circle(slide5, Inches(0.6), y + Inches(0.05), Inches(0.15), ALERT, ALERT)
    add_textbox(slide5, Inches(0.85), y, Inches(2.0), Inches(0.35),
                item, 8, color=GRAY)

# Arrow between columns
arrow_center_x = Inches(3.15)
arrow_center_y = Inches(3.5)
add_rounded_rect(slide5, arrow_center_x, arrow_center_y - Inches(0.03), Inches(0.8), Inches(0.06), ACCENT, ACCENT)
add_circle(slide5, arrow_center_x + Inches(0.65), arrow_center_y, Inches(0.18), ACCENT, ACCENT)

# After column
after_col = add_rounded_rect(slide5, Inches(3.55), Inches(1.35), Inches(2.6), Inches(4.4), LIGHT_BG, LIGHT_BG)
add_textbox(slide5, Inches(3.7), Inches(1.45), Inches(2.3), Inches(0.25),
            "BHOOMI PROCESS", 11, bold=True, color=SUCCESS, align=PP_ALIGN.CENTER)
after_items = [
    "AI OCR / HTR extraction",
    "17 structured canonical fields",
    "Field-level confidence scoring",
    "Automated validation (BR-1…BR-10)",
    "GIS cadastral verification",
    "Government reviewer approval",
    "Immutable SHA-256 audit chain",
    "Searchable · Exportable · Auditable",
]
for i, item in enumerate(after_items):
    y = Inches(1.85) + i * Inches(0.4)
    add_circle(slide5, Inches(3.8), y + Inches(0.05), Inches(0.15), SUCCESS, SUCCESS)
    add_textbox(slide5, Inches(4.05), y, Inches(2.0), Inches(0.35),
                item, 8, color=BLACK)

# RIGHT: Impact dimensions + Scalability
impact_title = add_textbox(slide5, Inches(6.5), Inches(1.05), Inches(6.0), Inches(0.25),
                          "IMPACT DIMENSIONS  ·  SCALABILITY", 12, bold=True, color=PRIMARY)

# Four impact cards in a 2x2 grid
impact_items = [
    ("REVENUE OFFICERS", "Reviewer queue · One-click corrections captured as training data · Approve/reject/escalate with full evidence.", PRIMARY),
    ("AUDITORS & SUPERVISORS", "Tamper-evident hash-chained trail · MIS dashboard (accuracy, pendency, errors, state-wise) · CSV export.", SECONDARY),
    ("ADMINISTRATION", "Digitization % tracked live · Review completion rates · Discrepancies flagged, never silently resolved.", SUCCESS),
    ("GOVERNANCE", "Reliable digital records from legacy pages · Multilingual access · Transparent, data-driven land administration.", ACCENT),
]
for i, (title, desc, col) in enumerate(impact_items):
    row = i // 2
    col_idx = i % 2
    x = Inches(6.5) + col_idx * Inches(3.0)
    y = Inches(1.5) + row * Inches(1.8)
    card = add_rounded_rect(slide5, x, y, Inches(2.8), Inches(1.5), LIGHT_BG, LIGHT_BG)
    add_rect(slide5, x, y, Inches(0.06), Inches(1.5), col, col)
    add_textbox(slide5, x + Inches(0.2), y + Inches(0.12), Inches(2.4), Inches(0.25),
                title, 9, bold=True, color=col)
    # Small icon circle
    icon_d = Inches(0.35)
    add_circle(slide5, x + Inches(0.2), y + Inches(0.45), icon_d, col, col)
    add_textbox(slide5, x + Inches(0.2), y + Inches(0.45), icon_d, icon_d,
                ["★", "◆", "●", "■"][i], 10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_textbox(slide5, x + Inches(0.7), y + Inches(0.45), Inches(2.0), Inches(0.3),
                desc, 7, color=BLACK)

# Scalability timeline at bottom
scal_title = add_textbox(slide5, Inches(6.5), Inches(5.2), Inches(6.0), Inches(0.25),
                         "SCALABILITY PATH  ·  PROTOTYPE → PRODUCTION", 10, bold=True, color=SECONDARY)
scal_items = [
    ("PHASE 1", "Prototype · 26 docs · SQLite"),
    ("PHASE 2", "District Pilot · Live adapters"),
    ("PHASE 3", "Government Integration · PostGIS"),
    ("PHASE 4", "Multi-district · Multi-state"),
]
for i, (label, desc) in enumerate(scal_items):
    x = Inches(6.5) + i * Inches(1.4)
    y = Inches(5.55)
    card = add_rounded_rect(slide5, x, y, Inches(1.3), Inches(0.7), LIGHT_BG, LIGHT_BG)
    add_rect(slide5, x, y, Inches(1.3), Inches(0.05), ACCENT, ACCENT)
    add_textbox(slide5, x, y + Inches(0.12), Inches(1.3), Inches(0.2),
                label, 9, bold=True, color=SECONDARY, align=PP_ALIGN.CENTER)
    add_textbox(slide5, x, y + Inches(0.35), Inches(1.3), Inches(0.3),
                desc, 6, color=GRAY, align=PP_ALIGN.CENTER)

# ------------------------------------------------------------------
# SLIDE 6 — RESEARCH & REFERENCES (Official Section 6)
# ------------------------------------------------------------------
slide6 = prs.slides.add_slide(prs.slide_layouts[6])
add_header_bar(slide6, "RESEARCH  ·  REFERENCES  ·  ROADMAP",
               "Verified sources · Adapter contracts · Production swap path · Next phases")

# Main layout: left = references, center = adapter architecture, right = roadmap

# LEFT: References (structured cards)
ref_title = add_textbox(slide6, Inches(0.35), Inches(1.05), Inches(4.0), Inches(0.25),
                        "REFERENCES & SOURCES", 12, bold=True, color=PRIMARY)
refs = [
    ("SIH PROBLEM STATEMENT", "SIH26018 · Ministry of Rural Development · Smart Automation Theme"),
    ("CODE & REPO", "github.com/fresherscomputersc-hash/BHOOMI · FastAPI · SQLAlchemy · Vanilla JS"),
    ("DOCUMENT INTELLIGENCE", "OpenCV · Tesseract 5.5 · spaCy NER · Hugging Face XLM-R · TrOCR (trialed)"),
    ("GIS & CADASTRAL", "Shapely · Sample GeoJSON layer · BhuNaksha integration (adapter-ready)"),
    ("GOVERNMENT SYSTEMS", "Bhulekh / RoR · BhuNaksha · IGR · LGD · DILRMP / LRMS — mock adapters, live-ready contracts"),
    ("SECURITY & AUDIT", "SHA-256 chain · Argon2 hashing · RBAC · Audit trail with re-verify"),
]
for i, (label, desc) in enumerate(refs):
    y = Inches(1.45) + i * Inches(0.7)
    card = add_rounded_rect(slide6, Inches(0.35), y, Inches(4.0), Inches(0.55), LIGHT_BG, LIGHT_BG)
    add_rect(slide6, Inches(0.35), y, Inches(0.06), Inches(0.55), ACCENT, ACCENT)
    add_textbox(slide6, Inches(0.65), y + Inches(0.06), Inches(3.6), Inches(0.2),
                label, 9, bold=True, color=SECONDARY)
    add_textbox(slide6, Inches(0.65), y + Inches(0.28), Inches(3.6), Inches(0.22),
                desc, 7, color=GRAY)

# CENTER: Adapter architecture diagram (visual flow showing mock/live contracts)
adapter_title = add_textbox(slide6, Inches(4.7), Inches(1.05), Inches(4.0), Inches(0.25),
                            "GOVERNMENT ADAPTER LAYER", 11, bold=True, color=PRIMARY)

# Central adapter node
adapter_center = add_rounded_rect(slide6, Inches(5.4), Inches(2.1), Inches(2.5), Inches(0.6), PRIMARY, PRIMARY)
add_textbox(slide6, Inches(5.4), Inches(2.25), Inches(2.5), Inches(0.2),
            "BHOOMI ADAPTER LAYER", 10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_textbox(slide6, Inches(5.4), Inches(2.45), Inches(2.5), Inches(0.2),
            "Live-ready contracts · Mock data now", 7, color=RGBColor(200, 210, 205), align=PP_ALIGN.CENTER)

# Adapter connections to government systems
systems = [
    ("BHULEKH / RoR", "Ownership verification"),
    ("BHU NAKSHA", "Cadastral map reference"),
    ("IGR", "Registration / deed"),
    ("LRMS / DILRMP", "Downstream status"),
    ("LGD MASTER", "Village / tehsil check"),
]
# Place systems around adapter in a semi-circle / vertical list
sys_colors = [SECONDARY, SECONDARY, PRIMARY, PRIMARY, ACCENT]
for i, (sys_name, desc) in enumerate(systems):
    y = Inches(2.95) + i * Inches(0.55)
    # Small rounded card
    card = add_rounded_rect(slide6, Inches(5.5), y, Inches(2.3), Inches(0.4), LIGHT_BG, LIGHT_BG)
    # Left stripe
    add_rect(slide6, Inches(5.5), y, Inches(0.05), Inches(0.4), sys_colors[i], sys_colors[i])
    # Connection line from adapter center to card
    conn_line = add_rect(slide6, Inches(6.8), y + Inches(0.2) - Inches(0.01), Inches(0.6), Inches(0.02), ACCENT, ACCENT)
    # Arrowhead circle at adapter side (simplified)
    # System info
    add_textbox(slide6, Inches(5.7), y + Inches(0.05), Inches(1.0), Inches(0.2),
                sys_name, 8, bold=True, color=sys_colors[i])
    # Mode label
    mode_text = "MOCK  ·  LIVE CONTRACT READY"
    add_textbox(slide6, Inches(6.7), y + Inches(0.05), Inches(1.0), Inches(0.2),
                mode_text, 6, bold=False, color=GRAY)
    add_textbox(slide6, Inches(5.7), y + Inches(0.22), Inches(2.0), Inches(0.15),
                desc, 7, color=BLACK)

# RIGHT: Production swap path + Roadmap
prod_title = add_textbox(slide6, Inches(8.6), Inches(1.05), Inches(4.0), Inches(0.25),
                         "PRODUCTION SWAP  ·  ROADMAP", 11, bold=True, color=PRIMARY)

# Production swap table (visual cards, not text table)
swap_items = [
    ("DATABASE", "SQLite → PostgreSQL + PostGIS"),
    ("QUEUE", "In-process → Redis / Celery"),
    ("HTR ENGINE", "Tesseract → TrOCR / IndicHTR"),
    ("LAYOUT", "OpenCV heuristics → YOLO / Detectron2"),
    ("AUTH", "Seeded + Argon2 → Department SSO + MFA"),
    ("GIS SERVING", "Sample GeoJSON → GeoServer"),
]
for i, (concern, swap) in enumerate(swap_items):
    y = Inches(1.45) + i * Inches(0.55)
    card = add_rounded_rect(slide6, Inches(8.6), y, Inches(4.0), Inches(0.42), LIGHT_BG, LIGHT_BG)
    add_rect(slide6, Inches(8.6), y, Inches(0.06), Inches(0.42), ACCENT, ACCENT)
    add_textbox(slide6, Inches(8.85), y + Inches(0.05), Inches(1.4), Inches(0.15),
                concern, 9, bold=True, color=SECONDARY)
    add_textbox(slide6, Inches(10.3), y + Inches(0.05), Inches(2.2), Inches(0.3),
                swap, 7, color=BLACK)

# Roadmap timeline at bottom right
road_title = add_textbox(slide6, Inches(8.6), Inches(4.85), Inches(4.0), Inches(0.2),
                         "ROADMAP", 10, bold=True, color=SECONDARY)
road_items = [
    ("PHASE 1", "Prototype  ·  26 docs"),
    ("PHASE 2", "District Pilot  ·  Live adapters"),
    ("PHASE 3", "Govt Integration  ·  PostGIS"),
    ("PHASE 4", "Multi-state Scale"),
]
for i, (label, desc) in enumerate(road_items):
    x = Inches(8.7) + i * Inches(1.0)
    y = Inches(5.15)
    # Timeline node
    circle = add_circle(slide6, x + Inches(0.3), y, Inches(0.35), PRIMARY, PRIMARY)
    add_textbox(slide6, x + Inches(0.3), y + Inches(0.05), Inches(0.35), Inches(0.25),
                str(i+1), 9, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    # Phase card below
    card = add_rounded_rect(slide6, x, y + Inches(0.45), Inches(0.95), Inches(0.7), LIGHT_BG, LIGHT_BG)
    add_textbox(slide6, x, y + Inches(0.48), Inches(0.95), Inches(0.2),
                label, 7, bold=True, color=SECONDARY, align=PP_ALIGN.CENTER)
    add_textbox(slide6, x, y + Inches(0.7), Inches(0.95), Inches(0.35),
                desc, 6, color=GRAY, align=PP_ALIGN.CENTER)
    # Connector line
    if i < 3:
        conn_x = x + Inches(0.95) + Inches(0.02)
        add_rect(slide6, conn_x, y + Inches(0.15), Inches(0.1), Inches(0.05), ACCENT, ACCENT)

# Footer note
add_textbox(slide6, Inches(0.35), Inches(6.95), Inches(12.7), Inches(0.35),
            "BhuSure is decision support — it does not adjudicate disputes, change ownership, or write back to government systems without formal approval. Every claim backed by repository evidence (tests, code, demo data, measured metrics).",
            7, bold=False, color=GRAY, align=PP_ALIGN.CENTER)

# ------------------------------------------------------------------
# SAVE
# ------------------------------------------------------------------
output_path = "BHOOMI_SIH_2026_Final.pptx"
prs.save(output_path)
print(f"Saved: {output_path}  ({len(prs.slides)} slides)")
