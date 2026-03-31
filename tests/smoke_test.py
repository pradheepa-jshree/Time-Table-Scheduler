#!/usr/bin/env python3
"""
Smoke Test for CSP Timetable Solver

A simple end-to-end test that validates the solver works correctly
with a realistic but small problem size.

Run with: python tests/smoke_test.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from utils.models import Session, Room, Assignment
from engine.solver import solve


def main():
    """Run smoke test with 5 sessions, 3 rooms, 20 time slots."""
    
    print("\n" + "=" * 50)
    print("CSP Solver Smoke Test")
    print("=" * 50)
    
    # ========================================================================
    # Setup Test Data
    # ========================================================================
    
    print("\n[Setup] Creating test data...")
    
    # 5 sessions
    sessions = [
        Session("S01", "T01", "CS-A", "Data Structures", "lecture"),
        Session("S02", "T02", "CS-A", "Algorithms", "lecture"),
        Session("S03", "T03", "CS-B", "Networks", "lab"),
        Session("S04", "T01", "CS-B", "Databases", "lecture"),
        Session("S05", "T04", "EC-A", "Digital Logic", "lab"),
    ]
    
    # 3 rooms
    rooms = [
        Room("R01", "Lab-101", 30, "lab"),
        Room("R02", "Hall-A", 60, "lecture"),
        Room("R03", "Hall-B", 80, "lecture"),
    ]
    
    # 20 time slots (MON-WED, 09:00-16:00)
    days = ["MON", "TUE", "WED"]
    hours = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]
    time_slots = [f"{day}-{hour}" for day in days for hour in hours][:20]
    
    print(f"  Sessions: {len(sessions)}")
    print(f"  Rooms: {len(rooms)}")
    print(f"  Time slots: {len(time_slots)}")
    
    # ========================================================================
    # Solve
    # ========================================================================
    
    print("\n[Solving] Running CSP solver...")
    result = solve(sessions, rooms, time_slots)
    
    # ========================================================================
    # Print Summary
    # ========================================================================
    
    print("\n" + "=" * 50)
    print("CSP Solver Smoke Test - Results")
    print("=" * 50)
    
    status_str = "COMPLETE ✓" if result.is_complete else "FAILED ✗"
    assignments_str = f"{len(result.assignments)}/{len(sessions)} assigned"
    
    print(f"\nStatus:           {status_str}")
    print(f"Sessions:         {assignments_str}")
    print(f"Nodes explored:   {result.stats['nodes_explored']}")
    print(f"Backtracks:       {result.stats['backtracks']}")
    print(f"Time taken:       {result.stats['time_ms']}ms")
    
    # ========================================================================
    # Print Assignments
    # ========================================================================
    
    if result.assignments:
        print("\n" + "=" * 50)
        print("Assignments")
        print("=" * 50)
        
        # Sort for consistent output
        sorted_assignments = sorted(result.assignments, key=lambda a: a.session_id)
        
        for assignment in sorted_assignments:
            print(f"{assignment.session_id} → Room {assignment.room_id} at {assignment.time_slot}")
    else:
        print("\n[No assignments found]")
    
    # ========================================================================
    # Final Status
    # ========================================================================
    
    print("\n" + "=" * 50)
    if result.is_complete:
        print("✓ Smoke test PASSED")
    else:
        print("✗ Smoke test FAILED")
    print("=" * 50 + "\n")
    
    return 0 if result.is_complete else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
