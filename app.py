import streamlit as st
import sys
import os
import base64
from pathlib import Path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.components import inject_global_styles, render_status_bar, render_background

try:
    from data.db import load_data, init_db
    from engine.solver import solve
    from agent.monitor import ScheduleMonitor
    from utils.csv_parser import load_from_csv
    BACKEND_AVAILABLE = True
except ImportError:
    BACKEND_AVAILABLE = False

st.set_page_config(
    page_title='AI Timetable Scheduler',
    page_icon='🗓️',
    layout='wide',
    initial_sidebar_state='expanded'
)

if 'db_path' not in st.session_state:
    st.session_state['db_path'] = 'timetable.db'
    if BACKEND_AVAILABLE:
        init_db(st.session_state['db_path'])

inject_global_styles()
render_background()

conflicts = len(st.session_state.get('agent_logs', []))
render_status_bar(title="AI-Powered College Timetable Scheduler", conflicts=conflicts)

def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None

logo_b64 = get_image_base64("assets/SRM_logo.png")
if logo_b64:
    st.sidebar.markdown(
        f'<img src="data:image/png;base64,{logo_b64}" '
        f'style="width:100%; max-width:140px; display:block; '
        f'margin: 0 auto 8px auto; background:transparent; border-radius:8px;">',
        unsafe_allow_html=True
    )

st.sidebar.markdown(
    '<p style="font-family:\'Syne\',sans-serif;font-size:11px;'
    'color:#484f58;letter-spacing:0.1em;margin-bottom:4px;">'
    'SRM UNIVERSITY · KTR</p>',
    unsafe_allow_html=True
)

page = st.sidebar.radio('', [
    '📥 Input Data',
    '⚙️ Run Solver',
    '📅 View Schedule',
    '📊 Statistics',
], label_visibility='collapsed')

st.sidebar.divider()

if not BACKEND_AVAILABLE:
    st.sidebar.warning('⚠️ Backend not connected — showing mock data')

st.sidebar.markdown(
    '<p style="font-family:\'JetBrains Mono\',monospace;font-size:10px;'
    'color:#484f58;">CSP · MRV · Forward Checking</p>',
    unsafe_allow_html=True
)

if   page == '📥 Input Data':    from ui import page_input    as p
elif page == '⚙️ Run Solver':    from ui import page_solver   as p
elif page == '📅 View Schedule': from ui import page_schedule as p
else:                             from ui import page_stats    as p

p.render()
