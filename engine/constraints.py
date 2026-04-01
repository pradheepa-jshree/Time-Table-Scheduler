# Hard constraint checker functions for timetable CSP


def no_room_clash(new_room, new_slot, assignment):
    """
    Check if a room is available at the given time slot.
    Returns False if any existing assignment uses the same room and time slot.
    """
    for session_id, (room_id, time_slot) in assignment.items():
        if room_id == new_room and time_slot == new_slot:
            return False
    return True


def no_teacher_clash(new_session_id, new_slot, assignment, sessions_map):
    """
    Check if a teacher has no other sessions at the given time slot.
    Returns False if another session with the same teacher is scheduled at the same time.
    """
    new_teacher = sessions_map[new_session_id].teacher_id
    for session_id, (room_id, time_slot) in assignment.items():
        if time_slot == new_slot:
            existing_teacher = sessions_map[session_id].teacher_id
            if existing_teacher == new_teacher:
                return False
    return True


def no_group_clash(new_session_id, new_slot, assignment, sessions_map):
    """
    Check if a student group has no other sessions at the given time slot.
    Returns False if another session with the same student group is scheduled at the same time.
    """
    new_group = sessions_map[new_session_id].student_group
    for session_id, (room_id, time_slot) in assignment.items():
        if time_slot == new_slot:
            existing_group = sessions_map[session_id].student_group
            if existing_group == new_group:
                return False
    return True


def is_consistent(session_id, value, assignment, sessions_map):
    """
    Composite constraint check: verifies all hard constraints.
    Returns True only if assignment passes room, teacher, and group clash checks.
    value is a (room_id, time_slot) tuple.
    """
    room_id, time_slot = value
    return (
        no_room_clash(room_id, time_slot, assignment) and
        no_teacher_clash(session_id, time_slot, assignment, sessions_map) and
        no_group_clash(session_id, time_slot, assignment, sessions_map)
    )
