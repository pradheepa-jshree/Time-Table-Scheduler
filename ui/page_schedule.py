# ui/page_schedule.py
import streamlit as st
from utils.models import Assignment, ScheduleResult
from ui.components import render_timetable_grid, render_violation_log

# ── Mock session info (replace on Day 8 with DB lookup) ──────────────────────
MOCK_SESSION_INFO = {
    'S01': {'subject': 'Math',      'teacher': 'Dr. Smith',  'room': 'Rm 101', 'group': 'CS-A'},
    'S02': {'subject': 'Physics',   'teacher': 'Prof. Jones','room': 'Lab A',  'group': 'CS-B'},
    'S03': {'subject': 'CS 101',    'teacher': 'Dr. Alice',  'room': 'Lab B',  'group': 'EC-A'},
    'S04': {'subject': 'Chemistry', 'teacher': 'Mr. Kumar',  'room': 'Rm 102', 'group': 'CS-A'},
    'S05': {'subject': 'Biology',   'teacher': 'Ms. Patel',  'room': 'Lab A',  'group': 'CS-B'},
}

MOCK_RESULT = ScheduleResult(
    assignments=[
        Assignment('S01','R02','MON-09:00'),
        Assignment('S02','R03','MON-10:00'),
        Assignment('S03','R01','MON-11:00'),
        Assignment('S04','R02','TUE-09:00'),
        Assignment('S05','R03','TUE-10:00'),
        Assignment('S01','R01','WED-09:00'),
        Assignment('S03','R02','WED-10:00'),
        Assignment('S02','R03','WED-11:00'),
        Assignment('S04','R01','THU-09:00'),
        Assignment('S05','R02','THU-10:00'),
        Assignment('S01','R03','FRI-09:00'),
        Assignment('S02','R01','FRI-11:00'),
    ],
    stats={'nodes_explored':42,'backtracks':3,'time_ms':18.4,'pruning_per_step':[5,3,1]},
    is_complete=True
)


def render():
    st.markdown(
        '<h2 style="font-family:\'Syne\',sans-serif;font-weight:800;'
        'color:#e6edf3;margin-bottom:4px;">📅 Generated Timetable</h2>'
        '<p style="color:#484f58;font-size:13px;margin-bottom:20px;">'
        'Color-coded by teacher. Each block shows subject, teacher, and room.</p>',
        unsafe_allow_html=True
    )

    result = st.session_state.get('result', MOCK_RESULT)

    if not result.assignments:
        st.info('No schedule yet — go to ⚙️ Run Solver.')
        return

    # ── Session info: use real data on Day 8 ─────────────────────────────────
    # Day 8 replace MOCK_SESSION_INFO with:
    # from data.db import get_session_info
    # session_info = {a.session_id: get_session_info(a.session_id)
    #                 for a in result.assignments}
    session_info = MOCK_SESSION_INFO

    # ── Timetable grid ────────────────────────────────────────────────────────
    render_timetable_grid(result.assignments, session_info)

    st.divider()

    # ── Violations ────────────────────────────────────────────────────────────
    st.markdown(
        '<p style="font-family:\'Syne\',sans-serif;font-weight:700;'
        'font-size:14px;color:#8b949e;margin-bottom:8px;">CONSTRAINT VIOLATIONS</p>',
        unsafe_allow_html=True
    )
    violations = st.session_state.get('agent_logs', [])
    violations_only = [v for v in violations if '[ERR]' in v or 'clash' in v.lower()]
    render_violation_log(violations_only)

    # ── Download ──────────────────────────────────────────────────────────────
    import pandas as pd
    rows = [{'session': a.session_id, 'room': a.room_id, 'slot': a.time_slot}
            for a in result.assignments]
    csv = pd.DataFrame(rows).to_csv(index=False)
    st.download_button('⬇️ Download Schedule CSV', data=csv,
                       file_name='timetable.csv', mime='text/csv')