from collections import defaultdict
from agent.logger import format_violation
from data.db import get_conn, fetch_all


class ScheduleMonitor:
    """
    Monitor schedule assignments for conflicts.
    Detects room clashes and teacher clashes.
    """

    def __init__(self, db_path, on_violation_callback=None):
        """
        Initialize the monitor.
        
        Args:
            db_path: Path to the SQLite database
            on_violation_callback: Optional callback function to call on each violation
        """
        self.db_path = db_path
        self.callback = on_violation_callback
        self._load_session_teacher_map()

    def _load_session_teacher_map(self):
        """
        Load mapping from session_id to teacher_id for quick lookups.
        """
        conn = get_conn(self.db_path)
        sessions_rows = fetch_all(conn, 'sessions')
        conn.close()
        
        self.session_to_teacher = {}
        for row in sessions_rows:
            self.session_to_teacher[row['id']] = row['teacher_id']

    def check(self, assignments: list) -> list[str]:
        """
        Detect violations in the assignment list.
        
        Violations detected:
        1. Room clash: same room + same time_slot assigned to 2 sessions
        2. Teacher clash: same teacher + same time_slot
        
        For each violation, call self.callback if set.
        
        Args:
            assignments: List of Assignment objects
        
        Returns:
            List of violation strings formatted by logger.format_violation(),
            or [] if no violations found.
        """
        violations = []
        
        # Check for room clashes
        room_time_usage = defaultdict(list)
        for assignment in assignments:
            key = (assignment.room_id, assignment.time_slot)
            room_time_usage[key].append(assignment.session_id)
        
        for (room_id, time_slot), session_ids in room_time_usage.items():
            if len(session_ids) > 1:
                msg = f"Room clash: Room {room_id} assigned to multiple sessions at {time_slot} ({', '.join(session_ids)})"
                violation_str = format_violation(msg)
                violations.append(violation_str)
                if self.callback:
                    self.callback(violation_str)
        
        # Check for teacher clashes
        teacher_time_usage = defaultdict(list)
        for assignment in assignments:
            teacher_id = self.session_to_teacher.get(assignment.session_id)
            if teacher_id:
                key = (teacher_id, assignment.time_slot)
                teacher_time_usage[key].append(assignment.session_id)
        
        for (teacher_id, time_slot), session_ids in teacher_time_usage.items():
            if len(session_ids) > 1:
                msg = f"Teacher clash: Teacher {teacher_id} assigned to multiple sessions at {time_slot} ({', '.join(session_ids)})"
                violation_str = format_violation(msg)
                violations.append(violation_str)
                if self.callback:
                    self.callback(violation_str)
        
        return violations
