import sqlite3
import os
from utils.models import Session, Room
from utils.time_slots import generate_slots


def get_conn(path='timetable.db'):
    """
    Get a connection to SQLite database.
    """
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(path='timetable.db') -> None:
    """
    Initialize database by running schema.sql.
    """
    conn = get_conn(path)
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as f:
        schema = f.read()
    conn.executescript(schema)
    conn.commit()
    conn.close()


def insert_teacher(conn, teacher_dict) -> None:
    """
    Insert a teacher record into the database.
    """
    conn.execute(
        '''INSERT INTO teachers (id, name, available_slots) 
           VALUES (?, ?, ?)''',
        (teacher_dict['id'], teacher_dict['name'], teacher_dict['available_slots'])
    )


def insert_room(conn, room_dict) -> None:
    """
    Insert a room record into the database.
    """
    conn.execute(
        '''INSERT INTO rooms (id, name, capacity, type) 
           VALUES (?, ?, ?, ?)''',
        (room_dict['id'], room_dict['name'], room_dict['capacity'], room_dict['type'])
    )


def insert_session(conn, session_dict) -> None:
    """
    Insert a session record into the database.
    """
    conn.execute(
        '''INSERT INTO sessions (id, teacher_id, student_group, subject, session_type, duration)
           VALUES (?, ?, ?, ?, ?, ?)''',
        (
            session_dict['id'],
            session_dict['teacher_id'],
            session_dict['student_group'],
            session_dict['subject'],
            session_dict['session_type'],
            session_dict.get('duration', 1)
        )
    )


def fetch_all(conn, table) -> list[dict]:
    """
    Fetch all rows from a table.
    Returns a list of dictionaries.
    """
    cursor = conn.execute(f'SELECT * FROM {table}')
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


def load_data(path='timetable.db') -> tuple:
    """
    Load all data from database and return as:
    (list[Session], list[Room], list[str])
    where list[str] = time slots from utils.time_slots.generate_slots()
    
    Returns exact Session and Room dataclass instances, NOT raw dicts.
    """
    conn = get_conn(path)
    
    # Fetch teachers, rooms, sessions
    teachers_rows = fetch_all(conn, 'teachers')
    rooms_rows = fetch_all(conn, 'rooms')
    sessions_rows = fetch_all(conn, 'sessions')
    
    conn.close()
    
    # Convert to Session dataclass instances
    sessions = []
    for row in sessions_rows:
        session = Session(
            id=row['id'],
            teacher_id=row['teacher_id'],
            student_group=row['student_group'],
            subject=row['subject'],
            session_type=row['session_type'],
            duration=row['duration']
        )
        sessions.append(session)
    
    # Convert to Room dataclass instances
    rooms = []
    for row in rooms_rows:
        room = Room(
            id=row['id'],
            name=row['name'],
            capacity=row['capacity'],
            type=row['type']
        )
        rooms.append(room)
    
    # Generate time slots
    time_slots = generate_slots()
    
    return (sessions, rooms, time_slots)
