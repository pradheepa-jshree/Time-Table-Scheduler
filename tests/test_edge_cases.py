import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

import pytest
from utils.models import Session, Room
from engine.solver import solve


# ============================================================================
# Edge Case Tests for CSP Solver
# ============================================================================

class TestEdgeCases:
    """Test edge cases and boundary conditions for the timetable CSP solver."""
    
    def test_single_session(self):
        """Test 1: Solve with minimal data: 1 session, 1 room, 1 time slot.
        
        Should solve instantly and find a complete solution.
        """
        sessions = [
            Session("S01", "T01", "CS-A", "Intro to CS", "lecture")
        ]
        rooms = [
            Room("R01", "Lab-101", 30, "lab")
        ]
        time_slots = ["MON-09:00"]
        
        result = solve(sessions, rooms, time_slots)
        
        assert result.is_complete is True, "Should find a solution for single session"
        assert len(result.assignments) == 1, "Should have exactly 1 assignment"
        assert result.assignments[0].session_id == "S01"
        assert result.assignments[0].room_id == "R01"
        assert result.assignments[0].time_slot == "MON-09:00"
    
    def test_impossible_case(self):
        """Test 2: Impossible constraint scenario.
        
        3 sessions all taught by the same teacher T01, but only 1 time slot.
        Teacher cannot teach 3 sessions at the same time, so unsolvable.
        Should return is_complete == False with empty assignments.
        """
        sessions = [
            Session("S01", "T01", "CS-A", "Data Structures", "lecture"),
            Session("S02", "T01", "CS-B", "Networks", "lecture"),
            Session("S03", "T01", "EC-A", "Algorithms", "lecture")
        ]
        rooms = [
            Room("R01", "Hall-A", 60, "lecture"),
            Room("R02", "Hall-B", 60, "lecture"),
            Room("R03", "Hall-C", 60, "lecture")
        ]
        time_slots = ["MON-09:00"]  # Only 1 slot available
        
        result = solve(sessions, rooms, time_slots)
        
        assert result.is_complete is False, "Should not find a solution for impossible case"
        assert len(result.assignments) == 0, "Should return empty assignments for unsolvable problem"
    
    def test_exact_fit(self):
        """Test 3: Exact fit scenario.
        
        Number of sessions exactly equals number of available (room, time_slot) pairs.
        Should find a complete solution.
        """
        sessions = [
            Session("S01", "T01", "CS-A", "Data Structures", "lecture"),
            Session("S02", "T02", "CS-B", "Algorithms", "lecture"),
            Session("S03", "T03", "EC-A", "Networks", "lecture")
        ]
        rooms = [
            Room("R01", "Hall-A", 60, "lecture")
        ]
        # 3 sessions, 1 room, 3 time slots = 3 total (room, time_slot) pairs (exact fit)
        time_slots = ["MON-09:00", "MON-10:00", "MON-11:00"]
        
        result = solve(sessions, rooms, time_slots)
        
        assert result.is_complete is True, "Should find solution with exact fit"
        assert len(result.assignments) == 3, "All 3 sessions should be assigned"
        
        # Verify no conflicts
        assigned_slots = set((a.room_id, a.time_slot) for a in result.assignments)
        assert len(assigned_slots) == 3, "All assignments should use different (room, time_slot) pairs"
    
    def test_stats_are_populated(self):
        """Test 4: Verify that solver statistics are properly populated.
        
        After solving, check that:
        - nodes_explored > 0
        - time_ms > 0
        - pruning_per_step is a list
        """
        sessions = [
            Session("S01", "T01", "CS-A", "Data Structures", "lecture"),
            Session("S02", "T02", "CS-B", "Networks", "lecture")
        ]
        rooms = [
            Room("R01", "Hall-A", 60, "lecture")
        ]
        time_slots = ["MON-09:00", "MON-10:00"]
        
        result = solve(sessions, rooms, time_slots)
        
        stats = result.stats
        assert isinstance(stats, dict), "Stats should be a dictionary"
        
        # Check required stat fields
        assert "nodes_explored" in stats, "Missing nodes_explored in stats"
        assert "time_ms" in stats, "Missing time_ms in stats"
        assert "backtracks" in stats, "Missing backtracks in stats"
        assert "pruning_per_step" in stats, "Missing pruning_per_step in stats"
        
        # Check stat values are reasonable
        assert isinstance(stats["nodes_explored"], int), \
            "nodes_explored should be an integer"
        assert stats["nodes_explored"] > 0, \
            "nodes_explored should be > 0 for any problem"
        
        assert isinstance(stats["time_ms"], (int, float)), \
            "time_ms should be numeric"
        assert stats["time_ms"] > 0, \
            "time_ms should be > 0"
        
        assert isinstance(stats["backtracks"], int), \
            "backtracks should be an integer"
        assert stats["backtracks"] >= 0, \
            "backtracks should be >= 0"
        
        assert isinstance(stats["pruning_per_step"], list), \
            "pruning_per_step should be a list"
    
    def test_mrv_off_still_solves(self):
        """Test 5: Brute force search (MRV=False, FC=False) still finds valid solutions.
        
        Even without heuristics, the basic backtracking algorithm should work.
        """
        sessions = [
            Session("S01", "T01", "CS-A", "Data Structures", "lecture"),
            Session("S02", "T02", "CS-B", "Networks", "lecture"),
            Session("S03", "T03", "EC-A", "Algorithms", "lecture")
        ]
        rooms = [
            Room("R01", "Hall-A", 60, "lecture"),
            Room("R02", "Hall-B", 60, "lecture")
        ]
        time_slots = ["MON-09:00", "MON-10:00", "MON-11:00"]
        
        # Solve without MRV and without Forward Checking (brute force)
        result = solve(sessions, rooms, time_slots, use_mrv=False, use_fc=False)
        
        assert result.is_complete is True, \
            "Brute force should still find a solution"
        assert len(result.assignments) == 3, \
            "All 3 sessions should be assigned even without heuristics"
        
        # Verify solution is valid (no conflicts)
        assignment_dict = {a.session_id: (a.room_id, a.time_slot) for a in result.assignments}
        sessions_map = {s.id: s for s in sessions}
        
        # Check no room double-bookings
        room_slots = {}
        for session_id, (room_id, time_slot) in assignment_dict.items():
            key = (room_id, time_slot)
            assert key not in room_slots, f"Room {room_id} double-booked at {time_slot}"
            room_slots[key] = session_id
        
        # Check no teacher conflicts
        teacher_slots = {}
        for session_id, (room_id, time_slot) in assignment_dict.items():
            teacher_id = sessions_map[session_id].teacher_id
            key = (teacher_id, time_slot)
            assert key not in teacher_slots, f"Teacher {teacher_id} conflict at {time_slot}"
            teacher_slots[key] = session_id
        
        # Check no group conflicts
        group_slots = {}
        for session_id, (room_id, time_slot) in assignment_dict.items():
            group = sessions_map[session_id].student_group
            key = (group, time_slot)
            assert key not in group_slots, f"Group {group} conflict at {time_slot}"
            group_slots[key] = session_id


# ============================================================================
# Additional Boundary Tests
# ============================================================================

class TestBoundaryConditions:
    """Test boundary conditions for the solver."""
    
    def test_many_sessions_few_slots(self):
        """Test with many sessions but few available slots.
        
        This creates high constraint density. The solver should either find
        a solution (if one exists) or correctly report unsolvable.
        """
        sessions = [
            Session(f"S{i:02d}", f"T{i % 3:02d}", f"G{i % 2}", f"Subject-{i}", "lecture")
            for i in range(1, 11)  # 10 sessions
        ]
        rooms = [
            Room("R01", "Hall-A", 60, "lecture")
        ]
        time_slots = ["MON-09:00", "MON-10:00", "MON-11:00"]  # Only 3 slots
        
        result = solve(sessions, rooms, time_slots)
        
        # Whether solvable or not, the result should be well-formed
        assert isinstance(result.is_complete, bool)
        assert isinstance(result.assignments, list)
        
        # If not complete, no assignments should be returned
        if not result.is_complete:
            assert len(result.assignments) == 0
    
    def test_multiple_rooms_many_slots(self):
        """Test with multiple rooms and many available slots (should be easy).
        
        The solver should quickly find a solution with abundant resources.
        """
        sessions = [
            Session("S01", "T01", "CS-A", "Subject-1", "lecture"),
            Session("S02", "T02", "CS-B", "Subject-2", "lecture")
        ]
        rooms = [
            Room("R01", "Hall-A", 60, "lecture"),
            Room("R02", "Hall-B", 80, "lecture"),
            Room("R03", "Hall-C", 100, "lecture")
        ]
        # 3 rooms × 10 slots = 30 available (room, time_slot) pairs
        time_slots = [f"MON-{h:02d}:00" for h in range(9, 19)]  # 9:00 to 18:00
        
        result = solve(sessions, rooms, time_slots)
        
        assert result.is_complete is True, \
            "Should easily solve with abundant resources"
        assert len(result.assignments) == 2
        assert result.stats["time_ms"] < 100, \
            "Should solve very quickly with abundant resources"
