import streamlit as st
from utils.models import ScheduleResult, Assignment

MOCK_RESULT = ScheduleResult(
    assignments=[],
    stats={'nodes_explored': 0, 'backtracks': 0,
           'time_ms': 0, 'pruning_per_step': [0]},
    is_complete=False
)

def render():
    st.title('📊 Statistics')

    result = st.session_state.get('result', None)

    if result is None:
        st.warning('⚠ Run the solver first to see statistics.')
        return

    stats = result.stats

    # Metric cards
    col1, col2, col3 = st.columns(3)
    col1.metric('Nodes Explored', stats.get('nodes_explored', 0))
    col2.metric('Backtracks', stats.get('backtracks', 0))
    col3.metric('Time Taken (ms)', stats.get('time_ms', 0))

    # Pruning chart
    pruning = stats.get('pruning_per_step', [0])
    if pruning and any(p > 0 for p in pruning):
        st.subheader('📉 Pruning per Step')
        st.bar_chart(pruning)
    else:
        st.info('No pruning data available.')

    # Agent log
    st.subheader('🤖 Agent Monitor Log')
    violations = st.session_state.get('agent_logs', [])
    if not violations:
        st.success('✅ No conflicts detected.')
    else:
        for v in violations:
            st.warning(v)