import pandas as pd
from utils.models import Session, Room
from utils.validators import validate_csv_schema, validate_no_duplicates
from data.db import init_db, insert_teacher, insert_room, insert_session, get_conn


def load_from_csv(teachers_csv, rooms_csv, sessions_csv, db_path='timetable.db') -> None:
    """
    Load data from CSV files, validate, and insert into SQLite database.
    
    Raises ValueError with clear human-readable message if:
      - any required column is missing
      - duplicate IDs exist
      - session references a teacher_id not in teachers table
    """
    # Load CSVs
    try:
        teachers_df = pd.read_csv(teachers_csv)
        rooms_df = pd.read_csv(rooms_csv)
        sessions_df = pd.read_csv(sessions_csv)
    except FileNotFoundError as e:
        raise ValueError(f"CSV file not found: {e}")
    except Exception as e:
        raise ValueError(f"Error reading CSV files: {e}")

    # Validate schemas
    validate_csv_schema(teachers_df, ['id', 'name', 'available_slots'], "Teachers CSV")
    validate_csv_schema(rooms_df, ['id', 'name', 'capacity', 'type'], "Rooms CSV")
    validate_csv_schema(
        sessions_df,
        ['id', 'teacher_id', 'student_group', 'subject', 'session_type'],
        "Sessions CSV"
    )

    # Validate no duplicates
    validate_no_duplicates(teachers_df, 'id', "Teachers CSV")
    validate_no_duplicates(rooms_df, 'id', "Rooms CSV")
    validate_no_duplicates(sessions_df, 'id', "Sessions CSV")

    # Validate referential integrity: all session teacher_ids must exist in teachers
    teacher_ids = set(teachers_df['id'].astype(str))
    invalid_teachers = sessions_df[~sessions_df['teacher_id'].astype(str).isin(teacher_ids)]
    if not invalid_teachers.empty:
        invalid_ids = invalid_teachers['teacher_id'].unique().tolist()
        raise ValueError(
            f"Sessions CSV: Invalid teacher_id(s) referenced: {', '.join(map(str, invalid_ids))}"
        )

    # Initialize database
    init_db(db_path)
    conn = get_conn(db_path)

    try:
        # Clear existing data before inserting new data
        conn.execute('DELETE FROM schedule')
        conn.execute('DELETE FROM sessions')
        conn.execute('DELETE FROM rooms')
        conn.execute('DELETE FROM teachers')
        
        # Insert teachers
        for _, row in teachers_df.iterrows():
            teacher_dict = {
                'id': row['id'],
                'name': row['name'],
                'available_slots': row['available_slots']
            }
            insert_teacher(conn, teacher_dict)

        # Insert rooms
        for _, row in rooms_df.iterrows():
            room_dict = {
                'id': row['id'],
                'name': row['name'],
                'capacity': int(row['capacity']),
                'type': row['type']
            }
            insert_room(conn, room_dict)

        # Insert sessions
        for _, row in sessions_df.iterrows():
            session_dict = {
                'id': row['id'],
                'teacher_id': row['teacher_id'],
                'student_group': row['student_group'],
                'subject': row['subject'],
                'session_type': row['session_type'],
                'duration': int(row.get('duration', 1))
            }
            insert_session(conn, session_dict)

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise ValueError(f"Error inserting data into database: {e}")
    finally:
        conn.close()
