import streamlit as st
import pandas as pd
from utils.models import Assignment, ScheduleResult

# Mock data ONLY used if solver has never been run
MOCK_RESULT = ScheduleResult(
    assignments=[
        Assignment('S01', 'R02', 'MON-09:00'),
        Assignment('S02', 'R03', 'MON-10:00'),
        Assignment('S03', 'R01', 'TUE-09:00'),
    ],
    stats={'nodes_explored': 0, 'backtracks': 0,
           'time_ms': 0, 'pruning_per_step': [0]},
    is_complete=False
)

GROUP_COLORS = {
    'CS-A': '#4CAF50',
    'CS-B': '#2196F3',
    'EC-A': '#FF9800',
    'ME-A': '#9C27B0',
}

def render():
    st.title('📅 View Schedule')

    result = st.session_state.get('result', None)

    if result is None:
        st.warning('⚠ No schedule generated yet. Go to Run Solver first.')
        return

    if not result.is_complete:
        st.error('❌ Last solver run did not find a complete schedule.')
        return

    st.success(f'✅ Showing {len(result.assignments)} scheduled sessions.')

    # Build display dataframe
    sessions_map = {}
    session_list = st.session_state.get('sessions', [])
    for s in session_list:
        sessions_map[s.id] = s

    rows = []
    for a in result.assignments:
        s = sessions_map.get(a.session_id)
        label = f"{s.subject}\n{s.student_group}" if s else a.session_id
        rows.append({
            'time_slot': a.time_slot,
            'room_id': a.room_id,
            'session_label': label,
            'student_group': s.student_group if s else '',
        })

    if not rows:
        st.info('No assignments to display.')
        return

    df = pd.DataFrame(rows)

    # Pivot: rows = time_slot, columns = room
    df_pivot = df.pivot_table(
        index='time_slot',
        columns='room_id',
        values='session_label',
        aggfunc='first'
    ).fillna('')

    # Sort time slots properly
    df_pivot = df_pivot.sort_index()

    # Color by student group
    group_map = df.set_index('time_slot').get('student_group', {})

    def color_cell(val):
        for group, color in GROUP_COLORS.items():
            if group in str(val):
                return f'background-color: {color}; color: white'
        return 'background-color: #2a2a2a; color: #888'

    styled = df_pivot.style.applymap(color_cell)
    st.dataframe(styled, use_container_width=True)

    # Agent violations
    violations = st.session_state.get('agent_logs', [])
    st.subheader('🤖 Agent Monitor Log')
    if not violations:
        st.success('✅ No conflicts detected.')
    else:
        for v in violations:
            st.warning(v)