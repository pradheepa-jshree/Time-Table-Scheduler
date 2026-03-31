CREATE TABLE IF NOT EXISTS teachers (
    id TEXT PRIMARY KEY,
    name TEXT,
    available_slots TEXT
);

CREATE TABLE IF NOT EXISTS rooms (
    id TEXT PRIMARY KEY,
    name TEXT,
    capacity INTEGER,
    type TEXT
);

CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    teacher_id TEXT REFERENCES teachers(id),
    student_group TEXT,
    subject TEXT,
    session_type TEXT,
    duration INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS schedule (
    session_id TEXT REFERENCES sessions(id),
    room_id TEXT REFERENCES rooms(id),
    time_slot TEXT,
    is_flagged INTEGER DEFAULT 0,
    PRIMARY KEY (session_id)
);
