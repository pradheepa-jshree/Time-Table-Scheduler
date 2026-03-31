import streamlit as st
from data.db import init_db

st.set_page_config(
    page_title='AI Timetable Scheduler',
    page_icon='🗓',
    layout='wide'
)

# Always init DB on startup
init_db()

# Sidebar navigation
st.sidebar.title("SRM UNIVERSITY · KTR")
page = st.sidebar.radio('Navigate', [
    '📥 Input Data',
    '⚙ Run Solver', 
    '📅 View Schedule',
    '📊 Statistics',
])

# Route to pages
if page == '📥 Input Data':
    from ui import page_input as p
elif page == '⚙ Run Solver':
    from ui import page_solver as p
elif page == '📅 View Schedule':
    from ui import page_schedule as p
else:
    from ui import page_stats as p

p.render()