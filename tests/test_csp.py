import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

import pytest
from utils.models import Session, Room
from engine.constraints import is_consistent
from engine.solver import solve


# Test data
sessions = [
    Session("S01", "T01", "CS-A", "Data Structures", "lecture"),
    Session("S02", "T01", "CS-B", "Networks", "lecture"),
    Session("S03", "T02", "CS-A", "Maths", "lecture")
]
sessions_map = {s.id: s for s in sessions}
rooms = [
    Room("R01", "Lab-101", 30, "lab"),
    Room("R02", "Hall-A", 60, "lecture")
]
time_slots = ["MON-09:00", "MON-10:00", "TUE-09:00"]


def test_empty_assignment_is_consistent():
    """Empty assignment should always allow any value."""
    result = is_consistent("S01", ("R01", "MON-09:00"), {}, sessions_map)
    assert result == True


def test_room_clash_detected():
    """Room clash: same room and time slot should fail."""
    assignment = {"S01": ("R01", "MON-09:00")}
    result = is_consistent("S02", ("R01", "MON-09:00"), assignment, sessions_map)
    assert result == False


def test_teacher_clash_detected():
    """Teacher clash: same teacher and time slot should fail.
    S01 (T01) assigned to MON-09:00.
    S02 also has T01 — assigning to different room but same slot should fail.
    """
    assignment = {"S01": ("R01", "MON-09:00")}
    result = is_consistent("S02", ("R02", "MON-09:00"), assignment, sessions_map)
    assert result == False


def test_group_clash_detected():
    """Group clash: same student_group and time slot should fail.
    S01 (group CS-A) assigned to MON-09:00.
    S03 also has CS-A — assigning to different room/teacher but same slot should fail.
    """
    assignment = {"S01": ("R01", "MON-09:00")}
    result = is_consistent("S03", ("R02", "MON-09:00"), assignment, sessions_map)
    assert result == False


def test_different_slot_no_clash():
    """No clash when assignments use different time slots.
    S01 at MON-09:00, S02 at MON-10:00 — both share teacher T01 but different slots.
    """
    assignment = {"S01": ("R01", "MON-09:00")}
    result = is_consistent("S02", ("R02", "MON-10:00"), assignment, sessions_map)
    assert result == True


def test_solve_returns_complete_result():
    """End-to-end: solve should find a complete assignment for all sessions."""
    result = solve(sessions, rooms, time_slots)
    assert result.is_complete == True
    assert len(result.assignments) == 3


def test_mrv_reduces_backtracks():
    """MRV heuristic should reduce or equal backtracks vs naive search."""
    result_mrv = solve(sessions, rooms, time_slots, use_mrv=True)
    result_no_mrv = solve(sessions, rooms, time_slots, use_mrv=False)
    assert result_mrv.stats["backtracks"] <= result_no_mrv.stats["backtracks"]
