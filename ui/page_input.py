# ui/page_input.py
import streamlit as st
import pandas as pd
import tempfile
import os
from ui.components import card_start, card_end, render_badge

# ── Backend imports (with fallback for ui branch) ─────────────────────────────
try:
    from data.db import load_data
    from utils.csv_parser import load_from_csv
    BACKEND_AVAILABLE = True
except ImportError:
    BACKEND_AVAILABLE = False

def render():
    st.markdown(
        '<h2 style="font-family:\'Syne\',sans-serif;font-weight:800;'
        'color:#e6edf3;margin-bottom:4px;">📥 Input Data</h2>'
        '<p style="color:#484f58;font-size:13px;margin-bottom:20px;">'
        'Upload CSV files or enter session data manually.</p>',
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(['📂 Upload CSVs', '✏️ Manual Entry'])

    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<p style="color:#8b949e;font-size:13px;">👨‍🏫 Teachers CSV</p>', unsafe_allow_html=True)
            teachers_file = st.file_uploader('', type='csv', key='t_csv', label_visibility='collapsed')
            if teachers_file:
                df = pd.read_csv(teachers_file)
                st.dataframe(df, use_container_width=True, height=150)
                st.session_state['teachers_csv'] = teachers_file
                render_badge(f"{len(df)} teachers loaded", "#3fb950")

        with col2:
            st.markdown('<p style="color:#8b949e;font-size:13px;">🏫 Rooms CSV</p>', unsafe_allow_html=True)
            rooms_file = st.file_uploader('', type='csv', key='r_csv', label_visibility='collapsed')
            if rooms_file:
                df = pd.read_csv(rooms_file)
                st.dataframe(df, use_container_width=True, height=150)
                st.session_state['rooms_csv'] = rooms_file
                render_badge(f"{len(df)} rooms loaded", "#58a6ff")

        with col3:
            st.markdown('<p style="color:#8b949e;font-size:13px;">📚 Sessions CSV</p>', unsafe_allow_html=True)
            sessions_file = st.file_uploader('', type='csv', key='s_csv', label_visibility='collapsed')
            if sessions_file:
                df = pd.read_csv(sessions_file)
                st.dataframe(df, use_container_width=True, height=150)
                st.session_state['sessions_csv'] = sessions_file
                render_badge(f"{len(df)} sessions loaded", "#bc8cff")

        st.divider()
        if st.button('✅ Load Data from CSVs', type='primary', use_container_width=True):
            if all(k in st.session_state for k in ['teachers_csv','rooms_csv','sessions_csv']):
                if not BACKEND_AVAILABLE:
                    st.session_state['data_loaded'] = True
                    st.success('✅ Data loaded (mock) — go to ⚙️ Run Solver')
                else:
                    try:
                        # Save uploaded files to temp paths
                        with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as t_file:
                            t_file.write(st.session_state['teachers_csv'].getvalue())
                            teachers_path = t_file.name
                        with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as r_file:
                            r_file.write(st.session_state['rooms_csv'].getvalue())
                            rooms_path = r_file.name
                        with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as s_file:
                            s_file.write(st.session_state['sessions_csv'].getvalue())
                            sessions_path = s_file.name
                        
                        # Call backend CSV loader
                        db_path = st.session_state['db_path']
                        load_from_csv(teachers_path, rooms_path, sessions_path, db_path)
                        
                        # Clean up temp files
                        os.unlink(teachers_path)
                        os.unlink(rooms_path)
                        os.unlink(sessions_path)
                        
                        st.session_state['data_loaded'] = True
                        st.success('✅ Data loaded — go to ⚙️ Run Solver')
                    except ValueError as e:
                        st.error(f'❌ CSV Error: {e}')
                    except Exception as e:
                        st.error(f'❌ Error loading data: {e}')
            else:
                st.warning('⚠️ Upload all 3 CSV files first.')

    with tab2:
        st.markdown('<p style="color:#8b949e;font-size:13px;">Edit session data directly in the table.</p>', unsafe_allow_html=True)
        default_sessions = pd.DataFrame({
            'id':            ['S01','S02','S03'],
            'teacher_id':    ['T01','T02','T01'],
            'student_group': ['CS-A','CS-B','CS-A'],
            'subject':       ['Data Structures','Networks','DS Lab'],
            'session_type':  ['lecture','lecture','lab'],
            'duration':      [1,1,1],
        })
        edited = st.data_editor(default_sessions, num_rows='dynamic', use_container_width=True)
        if st.button('💾 Save Manual Data', type='primary'):
            st.session_state['manual_sessions'] = edited
            st.session_state['data_loaded'] = True
            st.success('✅ Manual data saved — go to ⚙️ Run Solver')