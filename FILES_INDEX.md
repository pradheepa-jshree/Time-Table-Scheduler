# 📋 Member 2 - Data Layer & Agent - Complete File Index

## 📁 Directory Structure

```
timetable-scheduler/
│
├── utils/                          # Shared utilities layer
│   ├── __init__.py                # Empty package marker
│   ├── models.py                  # Dataclass definitions (SHARED - DO NOT MODIFY)
│   ├── time_slots.py              # Time slot generation (40 slots: MON-09:00 to FRI-17:00)
│   ├── validators.py              # CSV schema & duplicate validators
│   └── csv_parser.py              # CSV loading with full validation
│
├── data/                           # Data persistence layer
│   ├── __init__.py                # Empty package marker
│   ├── db.py                      # SQLite operations (init_db, load_data, insert_*, fetch_all)
│   ├── schema.sql                 # Database schema (4 tables)
│   ├── sample_teachers.csv        # 5 sample teachers
│   ├── sample_rooms.csv           # 3 sample rooms
│   └── sample_sessions.csv        # 10 sample sessions
│
├── agent/                          # Monitoring & violation detection
│   ├── __init__.py                # Empty package marker
│   ├── monitor.py                 # ScheduleMonitor class (room/teacher clash detection)
│   └── logger.py                  # Violation message formatting with emoji
│
├── tests/                          # Test suite (pytest)
│   ├── test_db.py                 # 7 database layer tests
│   └── test_monitor.py            # 6 monitor layer tests
│
├── MEMBER2_GUIDE.md               # Detailed integration guide for teammates
├── IMPLEMENTATION_SUMMARY.md       # Summary of implementation
├── verify_member2.py              # Quick verification script
└── README.md                      # Project description
```

---

## 📄 File Descriptions

### Utils Layer

| File | Purpose | Key Functions/Classes |
|------|---------|----------------------|
| `models.py` | Shared dataclasses | `Session`, `Room`, `Assignment`, `ScheduleResult` |
| `time_slots.py` | Generate scheduling time slots | `generate_slots()` → 40 slots |
| `validators.py` | CSV validation utilities | `validate_csv_schema()`, `validate_no_duplicates()` |
| `csv_parser.py` | Load CSV → Database | `load_from_csv()` with validation & error handling |

### Data Layer

| File | Purpose | Key Functions |
|------|---------|----------------|
| `db.py` | Database operations | `init_db()`, `load_data()`, `insert_teacher()`, `insert_room()`, `insert_session()`, `fetch_all()`, `get_conn()` |
| `schema.sql` | SQLite schema definition | 4 tables: `teachers`, `rooms`, `sessions`, `schedule` |
| `sample_*.csv` | Sample data files | Teachers, rooms, and sessions for testing |

### Agent Layer

| File | Purpose | Key Classes/Functions |
|------|---------|----------------------|
| `monitor.py` | Violation detection | `ScheduleMonitor` class with `check()` method |
| `logger.py` | Message formatting | `format_violation()` with emoji prefix |

### Tests

| File | Purpose | Test Count |
|------|---------|-----------|
| `test_db.py` | Database layer tests | 7 tests |
| `test_monitor.py` | Monitor layer tests | 6 tests |

---

## 🎯 Data Flow

```
CSV Files
    ↓
load_from_csv() [utils/csv_parser.py]
    ↓ (validates schema, duplicates, references)
    ↓
init_db() & insert_* [data/db.py]
    ↓
SQLite Database [data/schema.sql]
    ↓
load_data() [data/db.py]
    ↓ (returns dataclass instances)
    ↓
Member 1: solve(sessions, rooms, time_slots)
    ↓
    ↓ (generates assignments)
    ↓
Member 3: monitor.check(assignments) [agent/monitor.py]
    ↓
    ↓ (detects room/teacher clashes)
    ↓
Violation Messages with emoji [agent/logger.py]
```

---

## 🔌 Integration Points

### For Member 1 (Solver)
```python
from data.db import load_data
from utils.models import Session, Room, Assignment, ScheduleResult

# Load data
sessions, rooms, time_slots = load_data('timetable.db')

# Your solve function should:
# - Accept: sessions (list[Session]), rooms (list[Room]), time_slots (list[str])
# - Return: ScheduleResult with assignments (list[Assignment])

result = ScheduleResult(
    assignments=[Assignment(...)],  # Your algorithm output
    stats={'nodes_explored': ..., 'backtracks': ..., 'time_ms': ..., 'pruning_per_step': ...},
    is_complete=True
)
```

### For Member 3 (UI)
```python
from utils.models import Assignment, ScheduleResult
from data.db import load_data
from agent.monitor import ScheduleMonitor

# Load data
sessions, rooms, time_slots = load_data('timetable.db')

# Get violations
monitor = ScheduleMonitor('timetable.db')
violations = monitor.check(assignments)  # List of formatted violation strings

# Display
st.write("Assignments:")
for a in assignments:
    st.write(f"Session {a.session_id} → Room {a.room_id} at {a.time_slot}")

st.write("Violations:")
for v in violations:
    st.error(v)  # Shows: ⚠ Room clash: ...
```

---

## 📊 Specifications Summary

### Time Slots
- **Format**: 'DAY-HH:MM' (e.g., 'MON-09:00')
- **Days**: MON, TUE, WED, THU, FRI
- **Hours**: 09:00, 10:00, 11:00, 12:00, 14:00, 15:00, 16:00, 17:00
- **Total**: 40 slots

### Database Tables
1. **teachers**: id, name, available_slots (JSON array as string)
2. **rooms**: id, name, capacity, type (lecture/lab)
3. **sessions**: id, teacher_id, student_group, subject, session_type, duration
4. **schedule**: session_id, room_id, time_slot, is_flagged

### Dataclasses
```python
Session(id, teacher_id, student_group, subject, session_type, duration=1)
Room(id, name, capacity, type)
Assignment(session_id, room_id, time_slot)
ScheduleResult(assignments, stats, is_complete)
```

### Violation Detection
- **Room Clash**: Same room assigned to 2+ sessions at same time
- **Teacher Clash**: Same teacher scheduled for 2+ sessions at same time
- **Format**: "⚠ {clash_type}: {details}"

---

## ✅ Implementation Checklist

- [x] 15 files created
- [x] All imports working
- [x] Dataclasses match specification
- [x] Database schema complete (4 tables)
- [x] Time slot generation: 40 slots in 'DAY-HH:MM' format
- [x] CSV parsing with validation
- [x] Room clash detection
- [x] Teacher clash detection
- [x] 13 test functions (all passing)
- [x] Documentation complete
- [x] No breaking changes to M1/M3

---

## 🚀 Quick Commands

```bash
# Navigate to project
cd C:\Users\pradheepa jaya shree\Desktop\neww\Time-Table-Scheduler

# Install dependencies
pip install pandas pytest

# Verify setup
python verify_member2.py

# Run all tests
pytest tests/ -v

# Run specific tests
pytest tests/test_db.py -v
pytest tests/test_monitor.py -v

# Load sample data in Python
from utils.csv_parser import load_from_csv
load_from_csv('data/sample_teachers.csv', 'data/sample_rooms.csv', 'data/sample_sessions.csv')

# Access data
from data.db import load_data
sessions, rooms, time_slots = load_data('timetable.db')
```

---

## 📚 Documentation Files

- **MEMBER2_GUIDE.md** - Detailed guide with examples and integration notes
- **IMPLEMENTATION_SUMMARY.md** - Quick summary of what was implemented
- **verify_member2.py** - Automated verification script
- **This file** - Complete file index and reference

---

**Status**: ✅ **COMPLETE AND READY FOR INTEGRATION**

All Member 2 files follow the specification exactly. No changes made to Member 1 or Member 3 files.

See `MEMBER2_GUIDE.md` for detailed testing instructions and teammate integration notes.
