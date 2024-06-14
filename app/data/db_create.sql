DROP TABLE IF EXISTS stats;
CREATE TABLE IF NOT EXISTS stats(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT (datetime('now','localtime')) NOT NULL,
    total_users INTEGER,
    total_statuses BIGINT,
    last_updated_at DATETIME,
    total_instances SMALLINT,
    monthly_active_users INTEGER);