#!/usr/bin/env python3
"""
Quick verification script for Member 2 implementation.
Run this to verify all files are in place and imports work correctly.
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def verify_imports():
    """Verify all Member 2 imports work."""
    print("=" * 60)
    print("MEMBER 2 IMPLEMENTATION VERIFICATION")
    print("=" * 60)
    
    try:
        print("\n✓ Importing utils.models...", end=" ")
        from utils.models import Session, Room, Assignment, ScheduleResult
        print("OK")
        
        print("✓ Importing utils.time_slots...", end=" ")
        from utils.time_slots import generate_slots
        print("OK")
        
        print("✓ Importing utils.validators...", end=" ")
        from utils.validators import validate_csv_schema, validate_no_duplicates
        print("OK")
        
        print("✓ Importing utils.csv_parser...", end=" ")
        from utils.csv_parser import load_from_csv
        print("OK")
        
        print("✓ Importing data.db...", end=" ")
        from data.db import init_db, get_conn, load_data, insert_teacher, insert_room, insert_session, fetch_all
        print("OK")
        
        print("✓ Importing agent.monitor...", end=" ")
        from agent.monitor import ScheduleMonitor
        print("OK")
        
        print("✓ Importing agent.logger...", end=" ")
        from agent.logger import format_violation
        print("OK")
        
        return True
    except ImportError as e:
        print(f"\n✗ Import failed: {e}")
        return False


def verify_dataclasses():
    """Verify dataclass structure."""
    print("\n" + "-" * 60)
    print("VERIFYING DATACLASS STRUCTURE")
    print("-" * 60)
    
    from utils.models import Session, Room, Assignment, ScheduleResult
    
    # Create test instances
    session = Session(
        id="S01",
        teacher_id="T01",
        student_group="CS-A",
        subject="Math",
        session_type="lecture",
        duration=1
    )
    print(f"✓ Session instance: {session}")
    
    room = Room(id="R01", name="Lab-101", capacity=30, type="lab")
    print(f"✓ Room instance: {room}")
    
    assignment = Assignment(
        session_id="S01",
        room_id="R01",
        time_slot="MON-09:00"
    )
    print(f"✓ Assignment instance: {assignment}")
    
    schedule = ScheduleResult(
        assignments=[assignment],
        stats={"nodes_explored": 100, "backtracks": 5, "time_ms": 250.5, "pruning_per_step": 0.8},
        is_complete=True
    )
    print(f"✓ ScheduleResult instance: {schedule}")


def verify_time_slots():
    """Verify time slot generation."""
    print("\n" + "-" * 60)
    print("VERIFYING TIME SLOTS")
    print("-" * 60)
    
    from utils.time_slots import generate_slots
    
    slots = generate_slots()
    print(f"✓ Generated {len(slots)} time slots")
    print(f"  First 5: {slots[:5]}")
    print(f"  Last 5: {slots[-5:]}")
    
    assert len(slots) == 40, "Expected 40 time slots"
    assert slots[0] == "MON-09:00", "First slot should be MON-09:00"
    assert slots[-1] == "FRI-17:00", "Last slot should be FRI-17:00"
    print("✓ Time slot format and count verified")


def verify_database():
    """Verify database creation."""
    print("\n" + "-" * 60)
    print("VERIFYING DATABASE LAYER")
    print("-" * 60)
    
    import tempfile
    import sqlite3
    from data.db import init_db, get_conn
    
    # Create temp database
    fd, temp_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    try:
        init_db(temp_path)
        print(f"✓ Database initialized: {temp_path}")
        
        conn = get_conn(temp_path)
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        expected_tables = ['rooms', 'schedule', 'sessions', 'teachers']
        assert set(tables) == set(expected_tables), f"Expected {expected_tables}, got {tables}"
        print(f"✓ All tables created: {', '.join(tables)}")
        
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def verify_csv_files():
    """Verify sample CSV files exist."""
    print("\n" + "-" * 60)
    print("VERIFYING SAMPLE CSV FILES")
    print("-" * 60)
    
    csv_files = [
        'data/sample_teachers.csv',
        'data/sample_rooms.csv',
        'data/sample_sessions.csv'
    ]
    
    for csv_file in csv_files:
        path = os.path.join(project_root, csv_file)
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"✓ {csv_file} ({size} bytes)")
        else:
            print(f"✗ {csv_file} NOT FOUND")
            return False
    
    return True


def verify_test_files():
    """Verify test files exist."""
    print("\n" + "-" * 60)
    print("VERIFYING TEST FILES")
    print("-" * 60)
    
    test_files = [
        'tests/test_db.py',
        'tests/test_monitor.py'
    ]
    
    for test_file in test_files:
        path = os.path.join(project_root, test_file)
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"✓ {test_file} ({size} bytes)")
        else:
            print(f"✗ {test_file} NOT FOUND")
            return False
    
    return True


def main():
    """Run all verifications."""
    success = True
    
    # Check imports
    if not verify_imports():
        print("\n✗ Import verification FAILED")
        return False
    
    # Verify dataclasses
    try:
        verify_dataclasses()
    except Exception as e:
        print(f"\n✗ Dataclass verification FAILED: {e}")
        success = False
    
    # Verify time slots
    try:
        verify_time_slots()
    except Exception as e:
        print(f"\n✗ Time slot verification FAILED: {e}")
        success = False
    
    # Verify database
    try:
        verify_database()
    except Exception as e:
        print(f"\n✗ Database verification FAILED: {e}")
        success = False
    
    # Verify CSV files
    if not verify_csv_files():
        success = False
    
    # Verify test files
    if not verify_test_files():
        success = False
    
    # Summary
    print("\n" + "=" * 60)
    if success:
        print("✅ ALL VERIFICATIONS PASSED - Member 2 is ready!")
    else:
        print("❌ SOME VERIFICATIONS FAILED - Please check above")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run pytest: pytest tests/ -v")
    print("2. Load sample data: python -c \"from utils.csv_parser import load_from_csv; load_from_csv('data/sample_teachers.csv', 'data/sample_rooms.csv', 'data/sample_sessions.csv')\"")
    print("3. Test in Member 1/3: from data.db import load_data; sessions, rooms, slots = load_data()")
    
    return success


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
