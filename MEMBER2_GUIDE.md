# Member 2 - Data Layer & Agent

All Member 2 files have been created following the exact specification. This document provides testing instructions and integration notes.

---

## 📁 File Structure Created

```
timetable-scheduler/
├── data/
│   ├── __init__.py
│   ├── db.py
│   ├── schema.sql
│   ├── sample_teachers.csv
│   ├── sample_rooms.csv
│   └── sample_sessions.csv
├── agent/
│   ├── __init__.py
│   ├── monitor.py
│   └── logger.py
├── utils/
│   ├── __init__.py
│   ├── models.py          ← SHARED (DO NOT BREAK M1/M3 imports)
│   ├── csv_parser.py
│   ├── validators.py
│   └── time_slots.py
└── tests/
    ├── test_db.py
    └── test_monitor.py
```

---

## 🧪 How to Test Locally

### Prerequisites
```bash
pip install pandas pytest sqlite3
```

### Step 1: Run All Tests
```bash
cd C:\Users\pradheepa jaya shree\Desktop\neww\Time-Table-Scheduler
pytest tests/ -v
```

### Step 2: Run Specific Test Suites

**Test database layer only:**
```bash
pytest tests/test_db.py -v
```

**Test monitoring layer only:**
```bash
pytest tests/test_monitor.py -v
```

### Step 3: Test Data Loading Flow

Create a quick test script (`test_flow.py`):

```python
from utils.csv_parser import load_from_csv
from data.db import load_data

# Load sample data
load_from_csv(
    'data/sample_teachers.csv',
    'data/sample_rooms.csv',
    'data/sample_sessions.csv',
    'test_timetable.db'
)

# Verify data loaded correctly
sessions, rooms, time_slots = load_data('test_timetable.db')

print(f"✓ Loaded {len(sessions)} sessions")
print(f"✓ Loaded {len(rooms)} rooms")
print(f"✓ Loaded {len(time_slots)} time slots")
print(f"First session: {sessions[0]}")
print(f"First room: {rooms[0]}")
print(f"Sample slots: {time_slots[:5]}")
```

Run it:
```bash
python test_flow.py
```

### Step 4: Test Violation Detection

Create a test script (`test_violations.py`):

```python
from utils.models import Assignment
from agent.monitor import ScheduleMonitor
from data.db import init_db, get_conn, insert_teacher, insert_session

# Initialize test database
init_db('test_monitor.db')
conn = get_conn('test_monitor.db')

# Add test data
insert_teacher(conn, {'id': 'T01', 'name': 'Dr. Smith', 'available_slots': 'MON-09:00'})
insert_teacher(conn, {'id': 'T02', 'name': 'Dr. Jones', 'available_slots': 'MON-09:00'})
insert_session(conn, {'id': 'S01', 'teacher_id': 'T01', 'student_group': 'CS-A', 'subject': 'Math', 'session_type': 'lecture'})
insert_session(conn, {'id': 'S02', 'teacher_id': 'T02', 'student_group': 'CS-B', 'subject': 'Physics', 'session_type': 'lecture'})
conn.commit()
conn.close()

# Test violation detection
monitor = ScheduleMonitor('test_monitor.db')

# Clean schedule (no violations)
clean = [
    Assignment(session_id='S01', room_id='R01', time_slot='MON-09:00'),
    Assignment(session_id='S02', room_id='R02', time_slot='TUE-10:00'),
]
print("Clean schedule violations:", monitor.check(clean))

# Room clash
clash = [
    Assignment(session_id='S01', room_id='R01', time_slot='MON-09:00'),
    Assignment(session_id='S02', room_id='R01', time_slot='MON-09:00'),
]
print("Room clash violations:", monitor.check(clash))
```

Run it:
```bash
python test_violations.py
```

---

## 🔗 Integration Notes for Teammates

### For Member 1 (Solver Engine)

**What you need to know:**

1. **Import from Member 2:**
   ```python
   from data.db import load_data
   from utils.models import Session, Room, Assignment, ScheduleResult
   ```

2. **Expected Data Signature:**
   ```python
   sessions, rooms, time_slots = load_data(db_path='timetable.db')
   # Returns:
   # - sessions: list[Session]  ← dataclass instances with fields: id, teacher_id, student_group, subject, session_type, duration
   # - rooms: list[Room]        ← dataclass instances with fields: id, name, capacity, type
   # - time_slots: list[str]    ← 40 slots formatted as 'MON-09:00', 'TUE-10:00', etc.
   ```

3. **Your solve() function should return:**
   ```python
   ScheduleResult(
       assignments=list[Assignment],  # Each Assignment has: session_id, room_id, time_slot
       stats={
           'nodes_explored': int,
           'backtracks': int,
           'time_ms': float,
           'pruning_per_step': float
       },
       is_complete: bool
   )
   ```

4. **Critical:** Do NOT modify `utils/models.py`. Those are shared dataclass definitions that Member 3 also depends on.

---

### For Member 3 (UI/Streamlit)

**What you need to know:**

1. **Import from Member 2:**
   ```python
   from utils.models import Assignment, ScheduleResult, Session, Room
   from data.db import load_data
   from agent.monitor import ScheduleMonitor
   ```

2. **Expected CSV Structure:**
   - Teachers CSV: `id`, `name`, `available_slots` (comma-separated list)
   - Rooms CSV: `id`, `name`, `capacity`, `type`
   - Sessions CSV: `id`, `teacher_id`, `student_group`, `subject`, `session_type`

3. **Using the Monitor:**
   ```python
   monitor = ScheduleMonitor(db_path='timetable.db', on_violation_callback=my_callback)
   violations = monitor.check(assignments)  # Returns list of formatted violation strings
   # Each violation string has emoji prefix: "⚠ Room clash: ..." or "⚠ Teacher clash: ..."
   ```

4. **Displaying Results:**
   - `Assignment` has fields: `session_id`, `room_id`, `time_slot` — use these in your UI
   - `ScheduleResult.stats` contains performance metrics for display
   - `ScheduleResult.is_complete` indicates if a complete schedule was found

---

### CSV Data Loading

**For loading sample data:**
```python
from utils.csv_parser import load_from_csv

load_from_csv(
    'data/sample_teachers.csv',
    'data/sample_rooms.csv',
    'data/sample_sessions.csv',
    db_path='timetable.db'
)
```

**Error Handling:**
```python
try:
    load_from_csv(teachers_csv, rooms_csv, sessions_csv)
except ValueError as e:
    print(f"CSV Error: {e}")  # Clear error messages for missing columns, duplicates, invalid references
```

---

### Database Schema

Four SQLite tables (auto-created by `init_db()`):

1. **teachers**: `id`, `name`, `available_slots` (JSON array as string)
2. **rooms**: `id`, `name`, `capacity`, `type`
3. **sessions**: `id`, `teacher_id`, `student_group`, `subject`, `session_type`, `duration`
4. **schedule**: `session_id`, `room_id`, `time_slot`, `is_flagged`

---

### Key Constraints

⚠️ **CRITICAL - Do NOT Break:**

1. `utils/models.py` - Exact dataclass definitions for Session, Room, Assignment, ScheduleResult
2. `load_data()` return type must be `(list[Session], list[Room], list[str])`
3. Time slot format is ALWAYS `'MON-09:00'` (day-time, hyphen-separated)
4. 40 time slots total: 5 days × 8 hours (09:00, 10:00, 11:00, 12:00, 14:00, 15:00, 16:00, 17:00)
5. No imports of streamlit, engine, or ui modules in Member 2 files

---

### Violation Detection Logic

The monitor detects two types of violations:

1. **Room Clash**: Same room assigned to 2+ sessions at the same time slot
2. **Teacher Clash**: Same teacher scheduled for 2+ sessions at the same time slot

Both use 'MON-09:00' format for time slot matching.

---

## ✅ Verification Checklist

- [x] All 15 files created with exact specifications
- [x] Dataclass definitions in `utils/models.py` match specification exactly
- [x] Database schema has all 4 tables
- [x] `load_data()` returns Session/Room instances (not dicts)
- [x] Time slots count = 40, format = 'DAY-HH:MM'
- [x] CSV parser validates schemas and references
- [x] Monitor detects room and teacher clashes
- [x] All tests pass (17 test functions total)
- [x] No breaking changes to existing M1/M3 architecture

Ready for integration!
