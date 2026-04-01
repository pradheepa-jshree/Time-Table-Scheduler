from engine.constraints import is_consistent
from engine.heuristics import mrv_select, degree_tiebreak
from utils.models import Session, Room


class TimetableCSP:
    """
    Constraint Satisfaction Problem for timetable scheduling.
    
    Variables: Session IDs
    Domain: Each session can be assigned to any (room, time_slot) pair
    Constraints: No room clashes, no teacher clashes, no group clashes
    """
    
    def __init__(self, sessions: list, rooms: list, time_slots: list):
        """
        Initialize the CSP problem.
        
        Args:
            sessions: list of Session objects
            rooms: list of Room objects
            time_slots: list of time slot strings (e.g., ["MON-09:00", ...])
        """
        self.sessions_map = {s.id: s for s in sessions}
        self.variables = [s.id for s in sessions]
        self.domains = {s.id: [(r.id, t) for r in rooms for t in time_slots] 
                        for s in sessions}
    
    def backtrack(self, assignment: dict, stats: dict, 
                  use_mrv=True, use_fc=True) -> dict | None:
        """
        Backtracking search with optional MRV heuristic and forward checking.
        
        Args:
            assignment: dict of {session_id: (room_id, time_slot)}
            stats: dict to track search statistics
            use_mrv: whether to use Minimum Remaining Values heuristic
            use_fc: whether to use forward checking
        
        Returns:
            Complete assignment dict if solution found, None otherwise
        """
        # Base case: all variables assigned
        if len(assignment) == len(self.variables):
            return assignment
        
        # Select next variable
        unassigned = [v for v in self.variables if v not in assignment]
        
        if use_mrv:
            var = mrv_select(unassigned, self.domains)
        else:
            var = unassigned[0]
        
        # Try each value in the domain
        for value in self.domains[var]:
            # Check consistency
            if not is_consistent(var, value, assignment, self.sessions_map):
                continue
            
            # Assign value
            assignment[var] = value
            stats['nodes_explored'] += 1
            
            # Forward check if enabled
            pruned = {}
            if use_fc:
                pruned = self.forward_check(var, value, assignment)
                stats['pruning_per_step'].append(sum(len(v) for v in pruned.values()))
            
            # Recursively solve
            result = self.backtrack(assignment, stats, use_mrv, use_fc)
            if result is not None:
                return result
            
            # Undo assignment
            del assignment[var]
            
            # Restore pruned domains
            if use_fc:
                self.restore_pruned(pruned)
            
            stats['backtracks'] += 1
        
        return None
    
    def forward_check(self, session_id, value: tuple, 
                      assignment: dict) -> dict:
        """
        Forward checking: prune domains of unassigned variables.
        
        Removes values from unassigned variable domains that would cause
        a clash with the newly assigned (session_id, value) pair.
        
        Clashes detected:
        - Room clash: same room AND same time slot
        - Teacher clash: same teacher AND same time slot
        - Group clash: same student_group AND same time slot
        
        Args:
            session_id: the variable just assigned
            value: tuple of (room_id, time_slot)
            assignment: current partial assignment
        
        Returns:
            dict of {other_session_id: [removed_values]}
        """
        room, slot = value
        assigned_teacher = self.sessions_map[session_id].teacher_id
        assigned_group = self.sessions_map[session_id].student_group
        
        pruned = {}
        
        for other_id in self.variables:
            if other_id in assignment:
                continue
            
            to_remove = []
            for (r, t) in self.domains[other_id]:
                # Room clash: same room and time slot
                if r == room and t == slot:
                    to_remove.append((r, t))
                    continue
                
                # Teacher clash: same teacher and time slot
                if t == slot and self.sessions_map[other_id].teacher_id == assigned_teacher:
                    to_remove.append((r, t))
                    continue
                
                # Group clash: same student group and time slot
                if t == slot and self.sessions_map[other_id].student_group == assigned_group:
                    to_remove.append((r, t))
            
            # Remove pruned values from domain
            if to_remove:
                pruned[other_id] = to_remove
                self.domains[other_id] = [d for d in self.domains[other_id] 
                                          if d not in to_remove]
        
        return pruned
    
    def restore_pruned(self, pruned: dict):
        """
        Restore domains after backtracking.
        
        Re-adds all pruned values back to their original domains when
        backtracking from a failed branch.
        
        Args:
            pruned: dict of {session_id: [removed_values]}
        """
        for session_id, removed_values in pruned.items():
            self.domains[session_id].extend(removed_values)
