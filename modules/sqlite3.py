import sqlite3


class MySqlite3:
    def __init__(self, db: str):
        self.db = db

    def get_tg_chats(self) -> list:
        """Get tg chats from db."""
        with sqlite3.connect(self.db) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM tg_chats")
            rows = cur.fetchall()

            # sqlite3.Row уже ведёт себя как dict, но можно явно привести, если хочется
            return [dict(row) for row in rows]
