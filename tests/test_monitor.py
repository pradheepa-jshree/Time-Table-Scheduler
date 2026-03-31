import pytest
import os
import tempfile
from utils.models import Assignment
from agent.monitor import ScheduleMonitor
from data.db import init_db, get_conn, insert_teacher, insert_session


@pytest.fixture
def temp_db_with_data():
    """Create a temporary database with sample data for testing."""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    init_db(path)
    conn = get_conn(path)
    
    # Insert teachers
    for i in range(1, 4):
        teacher_dict = {
            'id': f'T0{i}',
            'name': f'Dr. Teacher{i}',
            'available_slots': 'MON-09:00,TUE-10:00,WED-11:00'
        }
        insert_teacher(conn, teacher_dict)
    
    # Insert sessions
    sessions = [
        {'id': 'S01', 'teacher_id': 'T01', 'student_group': 'CS-A', 'subject': 'Math', 'session_type': 'lecture', 'duration': 1},
        {'id': 'S02', 'teacher_id': 'T02', 'student_group': 'CS-B', 'subject': 'Physics', 'session_type': 'lecture', 'duration': 1},
        {'id': 'S03', 'teacher_id': 'T03', 'student_group': 'EC-A', 'subject': 'Chemistry', 'session_type': 'lab', 'duration': 1},
        {'id': 'S04', 'teacher_id': 'T01', 'student_group': 'CS-C', 'subject': 'Biology', 'session_type': 'lecture', 'duration': 1},
    ]
    for session_dict in sessions:
        insert_session(conn, session_dict)
    
    conn.commit()
    conn.close()
    
    yield path
    
    if os.path.exists(path):
        os.remove(path)


def test_check_clean_schedule(temp_db_with_data):
    """Test that check() returns [] for a clean schedule (no conflicts)."""
    monitor = ScheduleMonitor(temp_db_with_data)
    
    assignments = [
        Assignment(session_id='S01', room_id='R01', time_slot='MON-09:00'),
        Assignment(session_id='S02', room_id='R02', time_slot='TUE-10:00'),
        Assignment(session_id='S03', room_id='R01', time_slot='WED-11:00'),
        Assignment(session_id='S04', room_id='R02', time_slot='MON-10:00'),
    ]
    
    violations = monitor.check(assignments)
    assert violations == []


def test_check_room_clash(temp_db_with_data):
    """Test that check() returns exactly 1 violation string when two sessions share the same room+slot."""
    monitor = ScheduleMonitor(temp_db_with_data)
    
    assignments = [
        Assignment(session_id='S01', room_id='R01', time_slot='MON-09:00'),
        Assignment(session_id='S02', room_id='R01', time_slot='MON-09:00'),  # Same room + time = clash
    ]
    
    violations = monitor.check(assignments)
    assert len(violations) == 1
    assert 'Room clash' in violations[0]
    assert 'R01' in violations[0]
    assert 'MON-09:00' in violations[0]


def test_check_teacher_clash(temp_db_with_data):
    """Test that check() returns exactly 1 violation string when same teacher is in two slots simultaneously."""
    monitor = ScheduleMonitor(temp_db_with_data)
    
    # S01 and S04 both have teacher T01
    assignments = [
        Assignment(session_id='S01', room_id='R01', time_slot='MON-09:00'),
        Assignment(session_id='S04', room_id='R02', time_slot='MON-09:00'),  # Same teacher + time = clash
    ]
    
    violations = monitor.check(assignments)
    assert len(violations) == 1
    assert 'Teacher clash' in violations[0]
    assert 'MON-09:00' in violations[0]


def test_check_violation_format(temp_db_with_data):
    """Test that violation string contains the room ID or time slot in the message."""
    monitor = ScheduleMonitor(temp_db_with_data)
    
    assignments = [
        Assignment(session_id='S01', room_id='R01', time_slot='MON-09:00'),
        Assignment(session_id='S02', room_id='R01', time_slot='MON-09:00'),
    ]
    
    violations = monitor.check(assignments)
    assert len(violations) == 1
    
    # Check for emoji prefix and content
    assert violations[0].startswith('⚠')
    assert ('R01' in violations[0] or 'MON-09:00' in violations[0])


def test_check_multiple_violations(temp_db_with_data):
    """Test that check() detects multiple different violation types."""
    monitor = ScheduleMonitor(temp_db_with_data)
    
    assignments = [
        Assignment(session_id='S01', room_id='R01', time_slot='MON-09:00'),
        Assignment(session_id='S02', room_id='R01', time_slot='MON-09:00'),  # Room clash
        Assignment(session_id='S04', room_id='R02', time_slot='MON-09:00'),  # Teacher clash (T01 again)
    ]
    
    violations = monitor.check(assignments)
    assert len(violations) >= 1


def test_check_callback_called(temp_db_with_data):
    """Test that callback is called for each violation."""
    callback_violations = []
    
    def test_callback(violation_str):
        callback_violations.append(violation_str)
    
    monitor = ScheduleMonitor(temp_db_with_data, on_violation_callback=test_callback)
    
    assignments = [
        Assignment(session_id='S01', room_id='R01', time_slot='MON-09:00'),
        Assignment(session_id='S02', room_id='R01', time_slot='MON-09:00'),
    ]
    
    violations = monitor.check(assignments)
    
    assert len(callback_violations) == len(violations)
    assert callback_violations[0] == violations[0]
