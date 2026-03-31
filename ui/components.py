# ui/components.py
# All custom HTML/CSS components injected via st.components.v1.html
# Import and call these from any page file.

import streamlit as st
import streamlit.components.v1 as components
import base64
from pathlib import Path


# ── Background image loader ───────────────────────────────────────────────────
def get_bg_base64():
    """Load background image as base64 string."""
    try:
        with open("assets/bg.png", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None


# ── Global dark theme injected once in app.py ─────────────────────────────────
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Syne:wght@400;600;700;800&display=swap');

/* Override Streamlit chrome */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0d1117 !important;
    color: #e6edf3 !important;
    font-family: 'Syne', sans-serif !important;
}
[data-testid="stSidebar"] {
    background-color: #10181f !important;
    border-right: 1px solid #1e2d3d !important;
}
[data-testid="stSidebar"] * { color: #c9d1d9 !important; }
section[data-testid="stSidebar"] .stRadio label { color: #8b949e !important; }
.stButton > button {
    background: linear-gradient(135deg, #00c896, #0077ff) !important;
    color: #000 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 6px !important;
    letter-spacing: 0.05em !important;
}
.stButton > button:hover { opacity: 0.85 !important; }
[data-testid="stFileUploader"] {
    background: #161b22 !important;
    border: 2px dashed #30363d !important;
    border-radius: 10px !important;
}
.stToggle label { color: #8b949e !important; }
div[data-testid="metric-container"] {
    background: #161b22 !important;
    border: 1px solid #1e2d3d !important;
    border-radius: 10px !important;
    padding: 16px !important;
}
.stDataFrame { background: #161b22 !important; }

/* Hide Streamlit default toolbar and header */
#MainMenu {visibility: hidden !important;}
header[data-testid="stHeader"] {display: none !important;}
.stDeployButton {display: none !important;}
[data-testid="stToolbar"] {display: none !important;}

/* Hide Gemini/Streamlit badge at the bottom */
.viewerBadge_container__1QSob {display: none !important;}
.viewerBadge_link__qRIco {display: none !important;}
#stDecoration {display: none !important;}
[data-testid="stDecoration"] {display: none !important;}
footer {display: none !important;}
footer:after {display: none !important;}

/* Improve font clarity */
/* Main page heading */
h1 {
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    text-shadow: 0 0 20px rgba(0,0,0,1), 
                 2px 2px 8px rgba(0,0,0,1) !important;
    letter-spacing: 0.02em !important;
}

/* Subtext and labels */
p, label, span, .stMarkdown p {
    color: #e6edf3 !important;
    font-weight: 500 !important;
    text-shadow: 1px 1px 6px rgba(0,0,0,1) !important;
    font-size: 0.95rem !important;
}

/* Tab labels */
.stTabs [data-baseweb="tab"] p {
    font-weight: 600 !important;
    color: #ffffff !important;
    text-shadow: 1px 1px 6px rgba(0,0,0,1) !important;
}

/* CSV labels above uploaders */
.stMarkdown h3, .stMarkdown strong {
    color: #ffffff !important;
    text-shadow: 0 0 10px rgba(0,0,0,1) !important;
    font-weight: 700 !important;
}

/* Keep file uploader box text dark */
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] span {
    color: #333333 !important;
    text-shadow: none !important;
    font-weight: 400 !important;
}

/* ─────────────────────────────────────────────────────────────────────────── */
/* ENHANCED: Sidebar semi-transparency, bold fonts, and background overlay */
/* ─────────────────────────────────────────────────────────────────────────── */

/* Sidebar: 80% opacity with backdrop blur */
[data-testid="stSidebar"] {
    background: rgba(16, 24, 31, 0.8) !important;
    backdrop-filter: blur(2px) !important;
}

/* Main content area: Dark overlay for readability */
[data-testid="stAppViewContainer"] {
    background: rgba(0, 0, 0, 0.25) !important;
}

[data-testid="stAppViewContainer"] > .main {
    background: rgba(13, 17, 23, 0.7) !important;
    backdrop-filter: blur(1px) !important;
}

/* Global bold fonts: font-weight 700 */
h2, h3, h4, h5, h6 {
    font-weight: 700 !important;
}

input, select, textarea {
    font-weight: 700 !important;
}

.stTabs [data-baseweb="tab"] {
    font-weight: 700 !important;
}

div[data-testid="metric-container"] {
    background: rgba(22, 27, 34, 0.9) !important;
    font-weight: 700 !important;
}
</style>
"""


def inject_global_styles():
    """Call once in app.py — injects dark theme overrides."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def render_background():
    """Inject background image CSS with dark overlay."""
    bg_b64 = get_bg_base64()
    if not bg_b64:
        return
    
    bg_css = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/png;base64,{bg_b64}") !important;
    background-size: cover !important;
    background-position: center !important;
    background-repeat: no-repeat !important;
    background-attachment: fixed !important;
}}

[data-testid="stAppViewContainer"] > .main {{
    background: rgba(13, 17, 23, 0.88) !important;
}}

[data-testid="stSidebar"] {{
    background: rgba(13, 17, 23, 1.0) !important;
}}

section[data-testid="stAppViewContainer"] > div:first-child {{
    background: transparent !important;
}}
</style>
"""
    st.markdown(bg_css, unsafe_allow_html=True)


# ── Top status bar ────────────────────────────────────────────────────────────
def render_status_bar(title: str = "AI-Powered College Timetable Scheduler",
                      conflicts: int = 0):
    status_text  = f"✅ Status: {conflicts} Conflicts Detected ({'System Optimized' if conflicts == 0 else 'Action Required'})"
    status_color = "#00c896" if conflicts == 0 else "#f85149"
    html = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@700&family=Syne:wght@800&display=swap');
    .status-bar {{
        display: flex; align-items: flex-start; justify-content: space-between;
        padding: 12px 20px;
        background: #0d1117;
        border-bottom: 1px solid #1e2d3d;
        margin-bottom: 4px;
        gap: 16px;
    }}
    .status-bar h1 {{
        font-family: 'Syne', sans-serif;
        font-size: 14px; font-weight: 800;
        color: #e6edf3; margin: 0; padding: 0;
        letter-spacing: -0.02em;
        flex: 1; min-width: 0;
        word-wrap: break-word; white-space: normal;
        line-height: 1.3;
    }}
    .status-pill {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px; font-weight: 700;
        color: {status_color};
        background: {status_color}18;
        border: 1px solid {status_color}44;
        padding: 6px 14px; border-radius: 20px;
        display: flex; align-items: center; gap: 6px;
    }}
    .dot {{ width:8px; height:8px; border-radius:50%; background:{status_color};
            box-shadow: 0 0 6px {status_color}; }}
    </style>
    <div class="status-bar">
        <h1>🗓 {title}</h1>
        <div class="status-pill"><span class="dot"></span>{status_text}</div>
    </div>
    """
    components.html(html, height=60)


# ── Section card wrapper ──────────────────────────────────────────────────────
def card_start(title: str, icon: str = ""):
    st.markdown(f"""
    <div style="background:#161b22;border:1px solid #1e2d3d;border-radius:12px;
                padding:20px 24px;margin-bottom:16px;">
        <div style="font-family:'Syne',sans-serif;font-size:16px;font-weight:700;
                    color:#e6edf3;margin-bottom:14px;letter-spacing:-0.01em;">
            {icon} {title}
        </div>
    """, unsafe_allow_html=True)


def card_end():
    st.markdown("</div>", unsafe_allow_html=True)


# ── Timetable calendar grid ───────────────────────────────────────────────────
TEACHER_COLORS = {
    "Dr. Smith":   {"bg": "#1a3a5c", "accent": "#58a6ff"},
    "Prof. Jones": {"bg": "#2d1f4e", "accent": "#bc8cff"},
    "Dr. Alice":   {"bg": "#4a1a2e", "accent": "#f778ba"},
    "Mr. Kumar":   {"bg": "#3d2600", "accent": "#d29922"},
    "Ms. Patel":   {"bg": "#0d3320", "accent": "#3fb950"},
}
DEFAULT_COLOR = {"bg": "#1c2128", "accent": "#8b949e"}


def render_timetable_grid(assignments: list, session_info: dict,
                           days=None, hours=None):
    """
    assignments : list[Assignment]  — from ScheduleResult
    session_info: dict mapping session_id ->
                  { 'subject', 'teacher', 'room', 'group' }
    """
    if days  is None: days  = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
    if hours is None: hours = ["09:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00"]

    # Build lookup: (day_abbr, HH:MM) -> assignment info
    DAY_MAP = {"MON":"Monday","TUE":"Tuesday","WED":"Wednesday",
               "THU":"Thursday","FRI":"Friday","SAT":"Saturday"}
    grid = {}
    for a in assignments:
        parts = a.time_slot.split("-")   # e.g. MON-09:00
        if len(parts) == 2:
            day_full = DAY_MAP.get(parts[0], parts[0])
            hour     = parts[1]
            info     = session_info.get(a.session_id, {})
            grid[(day_full, hour)] = {
                "subject": info.get("subject",  a.session_id),
                "teacher": info.get("teacher",  ""),
                "room":    info.get("room",     a.room_id),
                "group":   info.get("group",    ""),
            }

    # Build legend HTML
    legend_items = ""
    for teacher, colors in TEACHER_COLORS.items():
        legend_items += f"""
        <span style="display:inline-flex;align-items:center;gap:6px;margin-right:18px;">
            <span style="width:12px;height:12px;border-radius:50%;
                         background:{colors['accent']};"></span>
            <span style="font-size:12px;color:#8b949e;">{teacher}</span>
        </span>"""

    # Build grid rows
    col_width = f"{100 / (len(days)+1):.1f}%"
    header_cells = "".join(
        f'<th style="background:#1a7f5a22;color:#3fb950;padding:10px 8px;'
        f'font-weight:700;font-size:13px;letter-spacing:0.04em;'
        f'border:1px solid #1e2d3d;text-align:center;">{d}</th>'
        for d in days
    )

    rows_html = ""
    for hour in hours:
        if hour == "12:00":
            rows_html += f"""
            <tr><td colspan="{len(days)+1}"
                style="text-align:center;padding:8px;color:#484f58;
                       font-size:11px;font-family:'JetBrains Mono',monospace;
                       border:1px solid #1e2d3d;background:#0d1117;
                       letter-spacing:0.08em;">
                — Lunch Break — 12:00 to 13:00 —
            </td></tr>"""
            continue

        cells = f"""<td style="padding:8px;font-family:'JetBrains Mono',monospace;
                               font-size:12px;color:#484f58;vertical-align:top;
                               border:1px solid #1e2d3d;white-space:nowrap;">
                       {hour}
                    </td>"""
        for day in days:
            entry = grid.get((day, hour))
            if entry:
                colors = DEFAULT_COLOR
                for t, c in TEACHER_COLORS.items():
                    if t.lower() in entry["teacher"].lower():
                        colors = c; break
                cells += f"""
                <td style="border:1px solid #1e2d3d;padding:5px;vertical-align:top;">
                    <div style="background:{colors['bg']};
                                border-left:3px solid {colors['accent']};
                                border-radius:6px;padding:8px 10px;
                                min-height:64px;">
                        <div style="font-family:'Syne',sans-serif;
                                    font-weight:700;font-size:13px;
                                    color:{colors['accent']};margin-bottom:3px;">
                            {entry['subject']}
                        </div>
                        <div style="font-size:11px;color:#8b949e;">{entry['teacher']}</div>
                        <div style="font-size:10px;color:#484f58;margin-top:3px;">
                            🏛 {entry['room']}
                        </div>
                    </div>
                </td>"""
            else:
                cells += f'<td style="border:1px solid #1e2d3d;background:#0d1117;"></td>'

        rows_html += f"<tr>{cells}</tr>"

    html = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Syne:wght@700;800&display=swap');
    .timetable-wrap {{ background:#0d1117; padding:4px 0 12px; }}
    table.tt {{ width:100%; border-collapse:collapse; }}
    </style>
    <div class="timetable-wrap">
        <table class="tt">
            <thead>
                <tr>
                    <th style="border:1px solid #1e2d3d;padding:10px;width:70px;"></th>
                    {header_cells}
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
        <div style="margin-top:14px;padding-top:10px;border-top:1px solid #1e2d3d;">
            <span style="font-size:12px;color:#484f58;margin-right:12px;
                         font-family:'JetBrains Mono',monospace;">Teacher Legend:</span>
            {legend_items}
        </div>
    </div>
    """
    # Height: roughly 70px per hour row + legend
    height = len(hours) * 78 + 80
    components.html(html, height=height, scrolling=True)


# ── Pruning stats bars ────────────────────────────────────────────────────────
def render_pruning_bars(teacher_clash: int, room_clash: int, slot_overlap: int):
    total = max(teacher_clash + room_clash + slot_overlap, 1)

    def bar(label, value, color):
        pct = int(value / total * 100)
        return f"""
        <div style="margin-bottom:14px;">
            <div style="display:flex;justify-content:space-between;
                        margin-bottom:5px;">
                <span style="font-size:12px;color:#8b949e;">{label}</span>
                <span style="font-family:'JetBrains Mono',monospace;
                             font-size:12px;color:#e6edf3;">{value}</span>
            </div>
            <div style="background:#1c2128;border-radius:4px;height:10px;">
                <div style="width:{pct}%;background:{color};
                            border-radius:4px;height:10px;
                            transition:width 0.6s ease;"></div>
            </div>
        </div>"""

    html = f"""
    <style>@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono&family=Syne:wght@700&display=swap');</style>
    <div style="background:#161b22;border:1px solid #1e2d3d;border-radius:12px;padding:20px;">
        <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:15px;
                    color:#e6edf3;margin-bottom:18px;">
            📊 Pruning Stats (Forward Checking)
        </div>
        {bar("Teacher clash",  teacher_clash,  "#3fb950")}
        {bar("Room clash",     room_clash,     "#bc8cff")}
        {bar("Slot overlap",   slot_overlap,   "#d29922")}
        <div style="margin-top:14px;font-family:'JetBrains Mono',monospace;
                    font-size:11px;color:#484f58;">
            Total: <strong style="color:#8b949e;">{total}</strong>
            invalid combinations skipped before evaluation
        </div>
    </div>
    """
    components.html(html, height=220)


# ── Intelligent Agent Console (terminal log) ──────────────────────────────────
def render_agent_console(logs: list[str], height: int = 220):
    """
    logs: list of strings. Prefix with [OK], [INFO], [WARN], [ERR] for colors.
    """
    COLOR_MAP = {
        "[OK]":   "#3fb950",
        "[INFO]": "#58a6ff",
        "[WARN]": "#d29922",
        "[ERR]":  "#f85149",
        "[BOOT]": "#bc8cff",
    }

    lines_html = ""
    for log in logs:
        color = "#8b949e"
        for prefix, c in COLOR_MAP.items():
            if log.startswith(prefix):
                color = c; break
        lines_html += f'<div style="color:{color};margin-bottom:3px;">{log}</div>'

    html = f"""
    <style>@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Syne:wght@700&display=swap');</style>
    <div style="background:#161b22;border:1px solid #1e2d3d;border-radius:12px;padding:20px;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
            <div style="font-family:'Syne',sans-serif;font-weight:700;
                        font-size:15px;color:#e6edf3;">🤖 Intelligent Agent Console</div>
        </div>
        <div style="background:#0d1117;border-radius:8px;padding:14px;
                    font-family:'JetBrains Mono',monospace;font-size:12px;
                    line-height:1.7;height:{height-100}px;overflow-y:auto;">
            {lines_html if lines_html else
             '<span style="color:#484f58;">[IDLE] Awaiting solver run...</span>'}
        </div>
    </div>
    """
    components.html(html, height=height)


# ── Metric card row ───────────────────────────────────────────────────────────
def render_metric_row(metrics: list[dict]):
    """
    metrics: list of { 'label': str, 'value': str, 'icon': str, 'color': str }
    """
    cards = ""
    for m in metrics:
        color = m.get("color", "#58a6ff")
        cards += f"""
        <div style="background:#161b22;border:1px solid #1e2d3d;border-radius:12px;
                    padding:20px 24px;flex:1;min-width:0;">
            <div style="font-size:22px;margin-bottom:6px;">{m.get('icon','')}</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:28px;
                        font-weight:700;color:{color};letter-spacing:-0.02em;">
                {m['value']}
            </div>
            <div style="font-size:12px;color:#8b949e;margin-top:4px;">{m['label']}</div>
        </div>"""

    html = f"""
    <style>@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@700&family=Syne&display=swap');</style>
    <div style="display:flex;gap:14px;flex-wrap:wrap;">{cards}</div>
    """
    components.html(html, height=130)


# ── Violation log (agent output) ──────────────────────────────────────────────
def render_violation_log(violations: list[str]):
    if not violations:
        html = """
        <div style="background:#0d2918;border:1px solid #1a7f5a44;border-radius:10px;
                    padding:14px 18px;font-family:'JetBrains Mono',monospace;
                    font-size:13px;color:#3fb950;">
            ✅ No constraint violations — schedule is clean.
        </div>"""
        components.html(html, height=58)
        return

    items = "".join(
        f'<div style="padding:8px 0;border-bottom:1px solid #1e2d3d;color:#f85149;">'
        f'⚠ {v}</div>'
        for v in violations
    )
    html = f"""
    <style>@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono&display=swap');</style>
    <div style="background:#2d1215;border:1px solid #f8514944;border-radius:10px;padding:16px 20px;">
        <div style="font-family:'JetBrains Mono',monospace;font-size:13px;
                    font-weight:700;color:#f85149;margin-bottom:10px;">
            ❌ {len(violations)} Violation(s) Detected
        </div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:12px;">{items}</div>
    </div>"""
    components.html(html, height=60 + len(violations) * 38)


# ── Badge pill ────────────────────────────────────────────────────────────────
def render_badge(label: str, color: str = "#3fb950"):
    st.markdown(
        f'<span style="background:{color}22;color:{color};border:1px solid {color}44;'
        f'padding:3px 10px;border-radius:12px;font-size:12px;font-weight:700;'
        f'font-family:\'JetBrains Mono\',monospace;">{label}</span>',
        unsafe_allow_html=True
    )


# ── CSP constraint checklist ──────────────────────────────────────────────────
def render_constraint_checklist(use_mrv: bool, use_fc: bool):
    constraints = [
        ("No teacher double-booking", True),
        ("No room double-booking",    True),
        ("MRV Heuristic (Fast)",      use_mrv),
        ("Forward Checking",          use_fc),
    ]
    items = ""
    for label, active in constraints:
        color  = "#3fb950" if active else "#484f58"
        icon   = "✓" if active else "○"
        items += f"""
        <div style="display:flex;align-items:center;gap:10px;
                    padding:6px 0;border-bottom:1px solid #1e2d3d1a;">
            <span style="color:{color};font-weight:700;font-size:14px;">{icon}</span>
            <span style="color:{'#c9d1d9' if active else '#484f58'};font-size:13px;">{label}</span>
        </div>"""

    html = f"""
    <style>@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono&family=Syne:wght@700&display=swap');</style>
    <div style="background:#161b22;border:1px solid #1e2d3d;border-radius:12px;padding:18px 20px;">
        <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:14px;
                    color:#8b949e;letter-spacing:0.06em;margin-bottom:12px;">
            ⚙ CSP CONSTRAINTS
        </div>
        {items}
    </div>"""
    components.html(html, height=185)