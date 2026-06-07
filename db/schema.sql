CREATE TABLE IF NOT EXISTS tg_chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_name TEXT NOT NULL UNIQUE,
    send_message TEXT NOT NULL,
    last_send_at TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);
