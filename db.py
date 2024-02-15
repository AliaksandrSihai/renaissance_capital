import sqlite3


class DBConnect:
    """Класс для работы с бд"""

    def __init__(self, db_name):
        self.db_name = db_name
        self.table = None

    def connection(self):
        """Создание подключения к бд"""
        conn = sqlite3.connect(self.db_name)
        return conn, conn.cursor()

    def create_table(self, table_name):
        """Создание таблицы в бд"""
        self.table = table_name
        conn, cursor = self.connection()
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.table} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type VARCHAR(50),
            secID VARCHAR(250),
            secType VARCHAR(50),
            price INTEGER CHECK (price >= 0),
            date DATE,
            ImportedStatus VARCHAR(250)
        )"""
        )
        conn.commit()
        conn.close()

    def update_status(self, label, status):
        """Обновление статуса"""
        conn, cursor = self.connection()

        cursor.execute(f"SELECT id FROM {self.table} WHERE secID=?", (label,))
        record = cursor.fetchone()
        if record:
            cursor.execute(
                f"UPDATE {self.table} SET ImportedStatus=? WHERE secID=?",
                (status, label),
            )
            conn.commit()
            conn.close()
