from engine.csp import TimetableCSP
from utils.models import Assignment, ScheduleResult
import time


def solve(sessions, rooms, time_slots, 
          use_mrv=True, use_fc=True) -> ScheduleResult:
    """
    Solve the timetable CSP and return a ScheduleResult.
    
    Args:
        sessions: list of Session objects
        rooms: list of Room objects
        time_slots: list of time slot strings (e.g., ["MON-09:00", ...])
        use_mrv: whether to use Minimum Remaining Values heuristic (default: True)
        use_fc: whether to use forward checking (default: True)
    
    Returns:
        ScheduleResult containing assignments, stats, and completion status
    """
    # Step 1: Initialize stats
    stats = {
        "nodes_explored": 0,
        "backtracks": 0,
        "time_ms": 0,
        "pruning_per_step": []
    }
    
    # Step 2: Record start time
    start = time.time()
    
    # Step 3: Create CSP instance
    csp = TimetableCSP(sessions, rooms, time_slots)
    
    # Step 4: Run backtracking search
    result = csp.backtrack({}, stats, use_mrv, use_fc)
    
    # Step 5: Calculate elapsed time
    stats["time_ms"] = round((time.time() - start) * 1000, 2)
    
    # Step 6: Convert result to Assignment list
    if result is not None:
        assignments = [
            Assignment(session_id=sid, room_id=room, time_slot=slot)
            for sid, (room, slot) in result.items()
        ]
    else:
        assignments = []
    
    # Step 7: Return ScheduleResult
    return ScheduleResult(
        assignments=assignments,
        stats=stats,
        is_complete=result is not None
    )
