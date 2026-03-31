import streamlit as st
from data.db import load_data
from engine.solver import solve
from agent.monitor import ScheduleMonitor

def render():
    st.title('⚙ Run Solver')
    st.caption('Configure the CSP algorithm and generate the timetable.')

    # Algorithm toggles
    col1, col2 = st.columns(2)
    with col1:
        use_mrv = st.toggle('MRV Heuristic', value=True,
                    help='Assigns most-constrained session first')
    with col2:
        use_fc = st.toggle('Forward Checking', value=True,
                    help='Prunes impossible slots early')

    # Check data is loaded
    db_path = st.session_state.get('db_path', 'timetable.db')

    if st.button('🚀 Run AI Solver', use_container_width=True):
        try:
            # Load real data from YOUR database
            sessions, rooms, slots = load_data(db_path)

            if not sessions:
                st.error('No sessions found. Go to Input Data and load CSVs first.')
                return

            st.info(f'Loaded {len(sessions)} sessions, {len(rooms)} rooms, {len(slots)} slots')

            with st.spinner('Running CSP Backtracking...'):
                result = solve(sessions, rooms, slots,
                               use_mrv=use_mrv, use_fc=use_fc)

            # Store in session_state for other pages to read
            st.session_state['result'] = result
            st.session_state['sessions'] = sessions

            # Run monitor on real result
            monitor = ScheduleMonitor(db_path)
            violations = monitor.check(result.assignments)
            st.session_state['agent_logs'] = violations

            if result.is_complete:
                st.success(f'✅ Schedule generated! '
                           f'{len(result.assignments)} sessions assigned.')
                if violations:
                    for v in violations:
                        st.warning(v)
                else:
                    st.success('✅ Zero conflicts detected by agent.')
            else:
                st.error('❌ No valid schedule found. Try relaxing constraints.')

        except Exception as e:
            st.error(f'Solver error: {e}')
            raise e