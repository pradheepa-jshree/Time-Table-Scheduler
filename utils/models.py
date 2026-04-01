from dataclasses import dataclass, field


@dataclass
class Session:
    id: str
    teacher_id: str
    student_group: str
    subject: str
    session_type: str  # 'lecture' | 'lab'
    duration: int = 1


@dataclass
class Room:
    id: str
    name: str
    capacity: int
    type: str  # 'lecture' | 'lab'


@dataclass
class Assignment:
    session_id: str
    room_id: str
    time_slot: str  # format: 'MON-09:00'


@dataclass
class ScheduleResult:
    assignments: list  # list[Assignment]
    stats: dict  # keys: nodes_explored, backtracks, time_ms, pruning_per_step
    is_complete: bool


@dataclass
class ScheduleInput:
    sessions: list[Session] = field(default_factory=list)
    rooms: list[Room] = field(default_factory=list)
    