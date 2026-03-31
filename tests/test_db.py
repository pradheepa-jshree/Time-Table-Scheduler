import pytest
import os
import sqlite3
import tempfile
from utils.models import Session, Room
from data.db import (
    init_db,
    get_conn,
    insert_teacher,
    insert_room,
    insert_session,
    fetch_all,
    load_data
)


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)


def test_init_db_creates_tables(temp_db):
    """Test that init_db() creates all 4 tables without error."""
    init_db(temp_db)
    
    conn = get_conn(temp_db)
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    assert 'teachers' in tables
    assert 'rooms' in tables
    assert 'sessions' in tables
    assert 'schedule' in tables


def test_insert_and_fetch_teacher(temp_db):
    """Test insert + fetch round-trip for teacher."""
    init_db(temp_db)
    conn = get_conn(temp_db)
    
    teacher_dict = {
        'id': 'T01',
        'name': 'Dr. Smith',
        'available_slots': 'MON-09:00,TUE-10:00'
    }
    insert_teacher(conn, teacher_dict)
    conn.commit()
    
    rows = fetch_all(conn, 'teachers')
    conn.close()
    
    assert len(rows) == 1
    assert rows[0]['id'] == 'T01'
    assert rows[0]['name'] == 'Dr. Smith'
    assert rows[0]['available_slots'] == 'MON-09:00,TUE-10:00'


def test_insert_and_fetch_room(temp_db):
    """Test insert + fetch round-trip for room."""
    init_db(temp_db)
    conn = get_conn(temp_db)
    
    room_dict = {
        'id': 'R01',
        'name': 'Lab-101',
        'capacity': 30,
        'type': 'lab'
    }
    insert_room(conn, room_dict)
    conn.commit()
    
    rows = fetch_all(conn, 'rooms')
    conn.close()
    
    assert len(rows) == 1
    assert rows[0]['id'] == 'R01'
    assert rows[0]['name'] == 'Lab-101'
    assert rows[0]['capacity'] == 30
    assert rows[0]['type'] == 'lab'


def test_insert_and_fetch_session(temp_db):
    """Test insert + fetch round-trip for session."""
    init_db(temp_db)
    conn = get_conn(temp_db)
    
    # Insert teacher first (foreign key)
    teacher_dict = {'id': 'T01', 'name': 'Dr. Smith', 'available_slots': 'MON-09:00'}
    insert_teacher(conn, teacher_dict)
    
    session_dict = {
        'id': 'S01',
        'teacher_id': 'T01',
        'student_group': 'CS-A',
        'subject': 'Data Structures',
        'session_type': 'lecture',
        'duration': 1
    }
    insert_session(conn, session_dict)
    conn.commit()
    
    rows = fetch_all(conn, 'sessions')
    conn.close()
    
    assert len(rows) == 1
    assert rows[0]['id'] == 'S01'
    assert rows[0]['teacher_id'] == 'T01'
    assert rows[0]['student_group'] == 'CS-A'


def test_load_data_returns_correct_types(temp_db):
    """Test that load_data() returns (list[Session], list[Room], list[str])."""
    init_db(temp_db)
    conn = get_conn(temp_db)
    
    # Insert sample data
    teacher_dict = {'id': 'T01', 'name': 'Dr. Smith', 'available_slots': 'MON-09:00'}
    insert_teacher(conn, teacher_dict)
    
    room_dict = {'id': 'R01', 'name': 'Lab-101', 'capacity': 30, 'type': 'lab'}
    insert_room(conn, room_dict)
    
    session_dict = {
        'id': 'S01',
        'teacher_id': 'T01',
        'student_group': 'CS-A',
        'subject': 'Data Structures',
        'session_type': 'lecture',
        'duration': 1
    }
    insert_session(conn, session_dict)
    conn.commit()
    conn.close()
    
    sessions, rooms, time_slots = load_data(temp_db)
    
    assert isinstance(sessions, list)
    assert isinstance(rooms, list)
    assert isinstance(time_slots, list)


def test_load_data_returns_session_instances(temp_db):
    """Test that load_data() returns Session instances (not dicts)."""
    init_db(temp_db)
    conn = get_conn(temp_db)
    
    teacher_dict = {'id': 'T01', 'name': 'Dr. Smith', 'available_slots': 'MON-09:00'}
    insert_teacher(conn, teacher_dict)
    
    session_dict = {
        'id': 'S01',
        'teacher_id': 'T01',
        'student_group': 'CS-A',
        'subject': 'Data Structures',
        'session_type': 'lecture',
        'duration': 1
    }
    insert_session(conn, session_dict)
    conn.commit()
    conn.close()
    
    sessions, rooms, time_slots = load_data(temp_db)
    
    assert len(sessions) == 1
    assert isinstance(sessions[0], Session)
    assert sessions[0].id == 'S01'
    assert sessions[0].teacher_id == 'T01'


def test_load_data_returns_room_instances(temp_db):
    """Test that load_data() returns Room instances (not dicts)."""
    init_db(temp_db)
    conn = get_conn(temp_db)
    
    room_dict = {'id': 'R01', 'name': 'Lab-101', 'capacity': 30, 'type': 'lab'}
    insert_room(conn, room_dict)
    conn.commit()
    conn.close()
    
    sessions, rooms, time_slots = load_data(temp_db)
    
    assert len(rooms) == 1
    assert isinstance(rooms[0], Room)
    assert rooms[0].id == 'R01'
    assert rooms[0].name == 'Lab-101'


def test_load_data_time_slots_count(temp_db):
    """Test that time_slots has 40 entries (5 days * 8 hours)."""
    init_db(temp_db)
    
    sessions, rooms, time_slots = load_data(temp_db)
    
    assert len(time_slots) == 40
    assert 'MON-09:00' in time_slots
    assert 'FRI-17:00' in time_slots
