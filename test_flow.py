from utils.csv_parser import load_from_csv
from data.db import load_data

load_from_csv(
    'data/sample_teachers.csv',
    'data/sample_rooms.csv',
    'data/sample_sessions.csv',
    'test_timetable.db'
)

sessions, rooms, time_slots = load_data('test_timetable.db')
print(f"Sessions: {len(sessions)}")   # expect 10
print(f"Rooms: {len(rooms)}")         # expect 3
print(f"Time slots: {len(time_slots)}") # expect 40
print(f"Session type check: {type(sessions[0])}")  # must NOT say 'dict'