# ui/page_solver.py
import streamlit as st
from ui.components import render_constraint_checklist, render_agent_console

# ── Backend imports (with fallback for ui branch) ─────────────────────────────
try:
    from data.db import load_data
    from engine.solver import solve
    from agent.monitor import ScheduleMonitor
    BACKEND_AVAILABLE = True
except ImportError:
    BACKEND_AVAILABLE = False

# Default boot logs shown before solver runs
BOOT_LOGS = [
    "[BOOT] TimetableAgent v2.1 initialized...",
    "[INFO] Awaiting data load and solver trigger.",
    "[INFO] MRV + Forward Checking ready.",
]

def render():
    st.markdown(
        '<h2 style="font-family:\'Syne\',sans-serif;font-weight:800;'
        'color:#e6edf3;margin-bottom:4px;">⚙️ Run Solver</h2>'
        '<p style="color:#484f58;font-size:13px;margin-bottom:20px;">'
        'Configure the CSP algorithm and generate the timetable.</p>',
        unsafe_allow_html=True
    )

    col_left, col_right = st.columns([1, 2])

    with col_left:
        # ── Algorithm toggles ─────────────────────────────────────────────
        st.markdown(
            '<p style="font-family:\'Syne\',sans-serif;font-weight:700;'
            'font-size:14px;color:#8b949e;letter-spacing:0.06em;">⚙ SETTINGS</p>',
            unsafe_allow_html=True
        )
        hours_per_day = st.number_input('Hours per Day', min_value=1, max_value=10, value=6)
        classrooms    = st.number_input('Classrooms',    min_value=1, max_value=20,  value=10)
        start_time    = st.text_input('Start Time', value='09:00')

        st.markdown('<p style="color:#8b949e;font-size:13px;margin-top:8px;">Working Days</p>', unsafe_allow_html=True)
        
        # ── Checkbox styling for working days ──────────────────────────────
        st.markdown("""
        <style>
        [data-testid="stCheckbox"] {
            padding: 8px 4px !important;
            min-width: 90px !important;
        }
        [data-testid="stCheckbox"] label {
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            gap: 4px !important;
        }
        [data-testid="stCheckbox"] label p {
            font-size: 11px !important;
            font-weight: 600 !important;
            color: #ffffff !important;
            white-space: nowrap !important;
            text-shadow: 1px 1px 4px rgba(0,0,0,0.9) !important;
            margin: 0 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # ── Working days selector (7 columns - one per day) ─────────────────
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        cols = st.columns(7)
        days_selected = {}
        selected_days = []
        
        for i, day in enumerate(days):
            with cols[i]:
                checked = st.checkbox(
                    day,
                    value=(day not in ["Saturday", "Sunday"]),
                    key=f"day_{day}"
                )
                days_selected[day[:3]] = checked  # Store as Mon, Tue, etc. for compatibility
                if checked:
                    selected_days.append(day)

        st.markdown('<br>', unsafe_allow_html=True)
        use_mrv = st.toggle('🎯 MRV Heuristic', value=True)
        use_fc  = st.toggle('✂️ Forward Checking', value=True)

        st.markdown('<br>', unsafe_allow_html=True)
        render_constraint_checklist(use_mrv, use_fc)

    with col_right:
        # ── Run button ────────────────────────────────────────────────────
        if not st.session_state.get('data_loaded'):
            st.warning('⚠️ No data loaded yet. Go to 📥 Input Data first.')
        else:
            if st.button('🚀 Run AI Solver', type='primary', width='stretch'):
                with st.spinner('Running CSP backtracking...'):
                    if not BACKEND_AVAILABLE:
                        # ── Mock fallback until backend is merged ─────────
                        from utils.models import Assignment, ScheduleResult
                        result = ScheduleResult(
                            assignments=[
                                Assignment('S01','R02','MON-09:00'),
                                Assignment('S02','R03','MON-10:00'),
                                Assignment('S03','R01','TUE-09:00'),
                                Assignment('S04','R02','TUE-11:00'),
                                Assignment('S05','R03','WED-09:00'),
                            ],
                            stats={
                                'nodes_explored':    42 if use_mrv else 187,
                                'backtracks':         3 if use_mrv else 21,
                                'time_ms':           18.4,
                                'pruning_per_step':  [5,3,1,4,2],
                                'teacher_clash_pruned': 312,
                                'room_clash_pruned':    234,
                                'slot_overlap_pruned':  196,
                            },
                            is_complete=True
                        )
                        st.session_state['result']  = result
                        st.session_state['sessions'] = []
                        st.session_state['rooms']    = []
                        st.session_state['use_mrv'] = use_mrv
                        st.session_state['use_fc']  = use_fc

                        # Build agent logs
                        logs = [
                            "[BOOT] TimetableAgent v2.1 initialized...",
                            f"[INFO] Loading variables: {len(result.assignments)} class sessions",
                            f"[INFO] Building domains: 30 time slots × 5 rooms",
                            f"[OK]  MRV heuristic {'active — most constrained first' if use_mrv else 'disabled'}",
                            f"[OK]  Forward Checking {'enabled' if use_fc else 'disabled'}",
                            "[INFO] Backtracking search started (DFS)...",
                        ]
                        for i, a in enumerate(result.assignments, 1):
                            logs.append(f"[OK]  Depth {i} — {a.session_id} assigned to {a.time_slot}, {a.room_id}")
                        if result.is_complete:
                            logs.append(f"[OK]  Schedule complete in {result.stats['time_ms']} ms ✓")
                        else:
                            logs.append("[ERR] No valid schedule found — check constraints")
                        st.session_state['agent_logs'] = logs
                        
                    else:
                        # ── Real backend integration ──────────────────────
                        try:
                            # Load data from database
                            db_path = st.session_state['db_path']
                            sessions, rooms, slots = load_data(db_path)
                            
                            # Run the solver
                            result = solve(sessions, rooms, slots, use_mrv=use_mrv, use_fc=use_fc)
                            
                            # Store result and data in session state
                            st.session_state['result']  = result
                            st.session_state['sessions'] = sessions
                            st.session_state['rooms']    = rooms
                            st.session_state['use_mrv'] = use_mrv
                            st.session_state['use_fc']  = use_fc
                            
                            # Run monitor to check violations
                            monitor = ScheduleMonitor(db_path)
                            violations = monitor.check(result.assignments)
                            
                            # Build agent logs
                            logs = [
                                "[BOOT] TimetableAgent v2.1 initialized...",
                                f"[INFO] Loading variables: {len(result.assignments)} class sessions",
                                f"[INFO] Building domains: {len(slots)} time slots × {len(rooms)} rooms",
                                f"[OK]  MRV heuristic {'active — most constrained first' if use_mrv else 'disabled'}",
                                f"[OK]  Forward Checking {'enabled' if use_fc else 'disabled'}",
                                "[INFO] Backtracking search started (DFS)...",
                            ]
                            for i, a in enumerate(result.assignments, 1):
                                logs.append(f"[OK]  Depth {i} — {a.session_id} assigned to {a.time_slot}, {a.room_id}")
                            
                            if result.is_complete:
                                logs.append(f"[OK]  Schedule complete in {result.stats.get('time_ms', 0)} ms ✓")
                            else:
                                logs.append("[ERR] No valid schedule found — check constraints")
                            
                            # Add violations to logs
                            for v in violations:
                                logs.append(f"[ERR] {v}")
                            
                            st.session_state['agent_logs'] = logs
                            
                        except Exception as e:
                            st.error(f'❌ Solver error: {e}')
                            import traceback
                            st.error(traceback.format_exc())

        # ── Console always visible ────────────────────────────────────────
        logs = st.session_state.get('agent_logs', BOOT_LOGS)
        render_agent_console(logs, height=280)