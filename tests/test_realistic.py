import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

import pytest
from utils.models import Session, Room
from engine.solver import solve


# ============================================================================
# TEST DATA: Realistic timetable with 5 teachers, 3 rooms, 10 sessions
# ============================================================================

# Teachers
TEACHERS = ["T01", "T02", "T03", "T04", "T05"]

# Rooms: R01 (lab, 30), R02 (lecture, 60), R03 (lecture, 80)
ROOMS = [
    Room("R01", "Lab-101", 30, "lab"),
    Room("R02", "Lecture-Hall-A", 60, "lecture"),
    Room("R03", "Lecture-Hall-B", 80, "lecture")
]

# Generate time slots: MON-FRI, 09:00-17:00 (40 slots total)
# 8 slots per day: 09:00, 10:00, 11:00, 12:00, 13:00, 14:00, 15:00, 16:00
DAYS = ["MON", "TUE", "WED", "THU", "FRI"]
HOURS = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]
TIME_SLOTS = [f"{day}-{hour}" for day in DAYS for hour in HOURS]

# 10 sessions across 3 student groups with different teachers and subjects
SESSIONS = [
    # CS-A group (4 sessions)
    Session("S01", "T01", "CS-A", "Data Structures", "lecture"),
    Session("S02", "T02", "CS-A", "Algorithms", "lecture"),
    Session("S03", "T03", "CS-A", "Database Systems", "lab"),
    Session("S04", "T04", "CS-A", "Operating Systems", "lecture"),
    
    # CS-B group (3 sessions)
    Session("S05", "T01", "CS-B", "Networks", "lecture"),
    Session("S06", "T03", "CS-B", "Web Development", "lab"),
    Session("S07", "T05", "CS-B", "Software Engineering", "lecture"),
    
    # EC-A group (3 sessions)
    Session("S08", "T02", "EC-A", "Digital Logic", "lab"),
    Session("S09", "T04", "EC-A", "Microprocessors", "lecture"),
    Session("S10", "T05", "EC-A", "Signal Processing", "lecture"),
]

SESSIONS_MAP = {s.id: s for s in SESSIONS}


# ============================================================================
# Tests
# ============================================================================

class TestRealisticTimetable:
    """Test suite for realistic timetable scheduling."""
    
    def test_realistic_solve_completes(self):
        """Test 1: Verify that the solver finds a complete solution."""
        result = solve(SESSIONS, ROOMS, TIME_SLOTS)
        assert result.is_complete is True, "Solver should find a complete solution"
    
    def test_all_sessions_assigned(self):
        """Test 5: Verify that all 10 sessions are assigned."""
        result = solve(SESSIONS, ROOMS, TIME_SLOTS)
        assert len(result.assignments) == 10, \
            f"Expected 10 assignments, got {len(result.assignments)}"
    
    def test_no_room_double_booked(self):
        """Test 2: Verify no two assignments share the same room and time slot."""
        result = solve(SESSIONS, ROOMS, TIME_SLOTS)
        
        # Group assignments by (room_id, time_slot)
        room_time_slots = {}
        for assignment in result.assignments:
            key = (assignment.room_id, assignment.time_slot)
            if key in room_time_slots:
                pytest.fail(
                    f"Room {assignment.room_id} double-booked at {assignment.time_slot}. "
                    f"Sessions: {room_time_slots[key]} and {assignment.session_id}"
                )
            room_time_slots[key] = assignment.session_id
    
    def test_no_teacher_double_booked(self):
        """Test 3: Verify no teacher appears twice in the same time slot."""
        result = solve(SESSIONS, ROOMS, TIME_SLOTS)
        
        # Group assignments by (teacher_id, time_slot)
        teacher_time_slots = {}
        for assignment in result.assignments:
            session = SESSIONS_MAP[assignment.session_id]
            teacher_id = session.teacher_id
            key = (teacher_id, assignment.time_slot)
            
            if key in teacher_time_slots:
                pytest.fail(
                    f"Teacher {teacher_id} double-booked at {assignment.time_slot}. "
                    f"Sessions: {teacher_time_slots[key]} and {assignment.session_id}"
                )
            teacher_time_slots[key] = assignment.session_id
    
    def test_no_group_double_booked(self):
        """Test 4: Verify no student group appears twice in the same time slot."""
        result = solve(SESSIONS, ROOMS, TIME_SLOTS)
        
        # Group assignments by (student_group, time_slot)
        group_time_slots = {}
        for assignment in result.assignments:
            session = SESSIONS_MAP[assignment.session_id]
            group = session.student_group
            key = (group, assignment.time_slot)
            
            if key in group_time_slots:
                pytest.fail(
                    f"Group {group} double-booked at {assignment.time_slot}. "
                    f"Sessions: {group_time_slots[key]} and {assignment.session_id}"
                )
            group_time_slots[key] = assignment.session_id
    
    def test_mrv_faster_than_no_mrv(self):
        """Test 6: Verify that MRV heuristic produces faster solutions."""
        result_with_mrv = solve(SESSIONS, ROOMS, TIME_SLOTS, use_mrv=True)
        result_without_mrv = solve(SESSIONS, ROOMS, TIME_SLOTS, use_mrv=False)
        
        time_with_mrv = result_with_mrv.stats["time_ms"]
        time_without_mrv = result_without_mrv.stats["time_ms"]
        
        # MRV should be faster (or at least not significantly slower)
        # We use a tolerance to account for system variability
        tolerance = time_without_mrv * 0.5  # Allow 50% margin
        assert time_with_mrv <= time_without_mrv + tolerance, \
            f"MRV ({time_with_mrv}ms) should be faster than no-MRV ({time_without_mrv}ms)"
        
        # Optional: Print performance metrics for debugging
        print(f"\nMRV Time: {time_with_mrv}ms, No-MRV Time: {time_without_mrv}ms")
        print(f"MRV Backtracks: {result_with_mrv.stats['backtracks']}, "
              f"No-MRV Backtracks: {result_without_mrv.stats['backtracks']}")


# ============================================================================
# Additional integration tests
# ============================================================================

class TestRealisticScheduleValidity:
    """Additional validation tests for the realistic schedule."""
    
    def test_schedule_has_valid_assignments(self):
        """Verify all assignments reference valid sessions, rooms, and time slots."""
        result = solve(SESSIONS, ROOMS, TIME_SLOTS)
        valid_sessions = {s.id for s in SESSIONS}
        valid_rooms = {r.id for r in ROOMS}
        valid_times = set(TIME_SLOTS)
        
        for assignment in result.assignments:
            assert assignment.session_id in valid_sessions, \
                f"Invalid session: {assignment.session_id}"
            assert assignment.room_id in valid_rooms, \
                f"Invalid room: {assignment.room_id}"
            assert assignment.time_slot in valid_times, \
                f"Invalid time slot: {assignment.time_slot}"
    
    def test_lab_sessions_assigned_to_lab_rooms(self):
        """Verify that lab sessions are assigned to lab rooms."""
        result = solve(SESSIONS, ROOMS, TIME_SLOTS)
        
        lab_room_ids = {r.id for r in ROOMS if r.type == "lab"}
        
        for assignment in result.assignments:
            session = SESSIONS_MAP[assignment.session_id]
            if session.session_type == "lab":
                assert assignment.room_id in lab_room_ids, \
                    f"Lab session {assignment.session_id} assigned to non-lab room {assignment.room_id}"
    
    def test_schedule_statistics_present(self):
        """Verify that solver statistics are properly recorded."""
        result = solve(SESSIONS, ROOMS, TIME_SLOTS)
        
        assert "time_ms" in result.stats, "Missing time_ms in stats"
        assert "nodes_explored" in result.stats, "Missing nodes_explored in stats"
        assert "backtracks" in result.stats, "Missing backtracks in stats"
        assert result.stats["time_ms"] > 0, "Time should be positive"
        assert result.stats["nodes_explored"] > 0, "Nodes explored should be positive"
