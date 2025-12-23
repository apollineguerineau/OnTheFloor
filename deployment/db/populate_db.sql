INSERT INTO users (username)
VALUES ('admin')
ON CONFLICT (username) DO NOTHING;
