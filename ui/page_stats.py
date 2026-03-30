# ui/page_stats.py
import streamlit as st
from utils.models import Assignment, ScheduleResult
from ui.components import (render_metric_row, render_pruning_bars,
                            render_agent_console, render_violation_log)

MOCK_RESULT = ScheduleResult(
    assignments=[
        Assignment('S01','R02','MON-09:00'),
        Assignment('S02','R03','MON-10:00'),
        Assignment('S03','R01','TUE-09:00'),
    ],
    stats={
        'nodes_explored': 42, 'backtracks': 3, 'time_ms': 18.4,
        'pruning_per_step': [5,3,1],
        'teacher_clash_pruned': 312,
        'room_clash_pruned':    234,
        'slot_overlap_pruned':  196,
    },
    is_complete=True
)


def render():
    st.markdown(
        '<h2 style="font-family:\'Syne\',sans-serif;font-weight:800;'
        'color:#e6edf3;margin-bottom:4px;">📊 Statistics</h2>'
        '<p style="color:#484f58;font-size:13px;margin-bottom:20px;">'
        'CSP engine performance and agent monitor output.</p>',
        unsafe_allow_html=True
    )

    result = st.session_state.get('result', MOCK_RESULT)
    stats  = result.stats

    # ── Metric cards ──────────────────────────────────────────────────────────
    render_metric_row([
        {'label': 'Nodes Explored', 'value': str(stats.get('nodes_explored','-')),
         'icon': '🔍', 'color': '#58a6ff'},
        {'label': 'Backtracks',     'value': str(stats.get('backtracks','-')),
         'icon': '↩️', 'color': '#f85149'},
        {'label': 'Time Taken',     'value': f"{stats.get('time_ms','-')} ms",
         'icon': '⏱️', 'color': '#3fb950'},
        {'label': 'Sessions Placed','value': str(len(result.assignments)),
         'icon': '📌', 'color': '#d29922'},
    ])

    st.markdown('<br>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # ── AI Engine Performance block ───────────────────────────────────
        render_pruning_bars(
            teacher_clash = stats.get('teacher_clash_pruned', 312),
            room_clash    = stats.get('room_clash_pruned',    234),
            slot_overlap  = stats.get('slot_overlap_pruned',  196),
        )

    with col2:
        # ── Agent console ─────────────────────────────────────────────────
        logs = st.session_state.get('agent_logs', [
            "[BOOT] TimetableAgent v2.1 initialized...",
            "[INFO] Awaiting solver run...",
        ])
        render_agent_console(logs, height=220)

    st.markdown('<br>', unsafe_allow_html=True)

    # ── Algorithm config used ─────────────────────────────────────────────────
    st.markdown(
        '<p style="font-family:\'Syne\',sans-serif;font-weight:700;'
        'font-size:14px;color:#8b949e;margin-bottom:8px;">ALGORITHM CONFIG</p>',
        unsafe_allow_html=True
    )
    c1, c2, c3 = st.columns(3)
    mrv_on = st.session_state.get('use_mrv', True)
    fc_on  = st.session_state.get('use_fc',  True)
    c1.info(f"MRV: {'✅ ON' if mrv_on else '❌ OFF'}")
    c2.info(f"Forward Checking: {'✅ ON' if fc_on else '❌ OFF'}")
    c3.info(f"Status: {'✅ Complete' if result.is_complete else '❌ Incomplete'}")

    # ── Violation log ─────────────────────────────────────────────────────────
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown(
        '<p style="font-family:\'Syne\',sans-serif;font-weight:700;'
        'font-size:14px;color:#8b949e;margin-bottom:8px;">CONSTRAINT VIOLATIONS</p>',
        unsafe_allow_html=True
    )
    all_logs  = st.session_state.get('agent_logs', [])
    violations = [v for v in all_logs if '[ERR]' in v or 'clash' in v.lower()]
    render_violation_log(violations)