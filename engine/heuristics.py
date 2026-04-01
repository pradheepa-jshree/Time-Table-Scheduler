# Heuristics for variable and value selection in CSP backtracking


def mrv_select(unassigned, domains):
    """
    Minimum Remaining Values (MRV) heuristic.
    
    Select the unassigned variable with the smallest domain.
    This is also called "fail-first" because by picking the most 
    constrained variable first, we maximize the chance of detecting 
    contradictions early and pruning the search tree.
    
    Args:
        unassigned: list of session_id strings not yet assigned
        domains: dict of {session_id: [(room_id, time_slot), ...]}
    
    Returns:
        session_id string with the minimum remaining domain size
    """
    if not unassigned:
        return None
    
    # Find the variable with the fewest domain values
    return min(unassigned, key=lambda var: len(domains[var]))


def degree_tiebreak(tied_vars, sessions_map):
    """
    Degree heuristic for breaking ties in MRV.
    
    When multiple variables have the same domain size, select the one
    that is most "connected" — i.e., appears most often alongside other
    unassigned variables. This is measured by counting how many times
    the session's teacher_id or student_group appears in the pool.
    
    More connections = more constraints = better chance of early pruning.
    
    Args:
        tied_vars: list of session_ids with equal domain sizes
        sessions_map: dict of {session_id: Session}
    
    Returns:
        session_id string with highest degree (most constrained)
    """
    if not tied_vars:
        return None
    
    if len(tied_vars) == 1:
        return tied_vars[0]
    
    # Count teacher and group occurrences across all tied variables
    teacher_count = {}
    group_count = {}
    
    for sid in tied_vars:
        teacher = sessions_map[sid].teacher_id
        group = sessions_map[sid].student_group
        teacher_count[teacher] = teacher_count.get(teacher, 0) + 1
        group_count[group] = group_count.get(group, 0) + 1
    
    # Select variable whose teacher/group has highest total count
    # This variable is most constrained by its peers
    def degree_score(session_id):
        teacher = sessions_map[session_id].teacher_id
        group = sessions_map[session_id].student_group
        return teacher_count.get(teacher, 0) + group_count.get(group, 0)
    
    return max(tied_vars, key=degree_score)
