CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS sessions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    session_type VARCHAR(50) NOT NULL,
    user_id INTEGER REFERENCES users(id),
    notes TEXT
);

CREATE TABLE IF NOT EXISTS blocks (
    id SERIAL PRIMARY KEY,
    block_type VARCHAR(50) NOT NULL,
    duration FLOAT,
    position INTEGER,
    session_id INTEGER REFERENCES sessions(id),
    notes TEXT,
    UNIQUE(session_id, position)
);

CREATE TABLE IF NOT EXISTS exercises (
    id SERIAL PRIMARY KEY,
    exercise_type VARCHAR(50) NOT NULL,
    weight_kg FLOAT,
    repetitions INTEGER,
    duration_seconds FLOAT,
    distance_meters FLOAT,
    block_id INTEGER REFERENCES blocks(id),
    position INTEGER,
    notes TEXT,
    UNIQUE(block_id, position)
);

CREATE TABLE IF NOT EXISTS photos (
    id SERIAL PRIMARY KEY,
    path VARCHAR(255) NOT NULL,
    session_id INTEGER REFERENCES sessions(id),
    notes TEXT
);
