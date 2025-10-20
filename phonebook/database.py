import sqlite3
from typing import List, Dict, Optional


class Database:
    def __init__(self, db_name: str = "phonebook.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        """Инициализация базы данных и создание таблицы"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT
                )
            ''')
            conn.commit()

    def add_contact(self, name: str, phone: str, email: str = None) -> int:
        """Добавление нового контакта"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
                (name, phone, email)
            )
            conn.commit()
            return cursor.lastrowid

    def get_all_contacts(self) -> List[Dict]:
        """Получение всех контактов"""
        with sqlite3.connect(self.db_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM contacts ORDER BY name")
            return [dict(row) for row in cursor.fetchall()]

    def get_contact(self, contact_id: int) -> Optional[Dict]:
        """Получение контакта по ID"""
        with sqlite3.connect(self.db_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def update_contact(self, contact_id: int, name: str, phone: str, email: str = None) -> bool:
        """Обновление контакта"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?",
                (name, phone, email, contact_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete_contact(self, contact_id: int) -> bool:
        """Удаление контакта"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
            conn.commit()
            return cursor.rowcount > 0

    def search_contacts(self, query: str) -> List[Dict]:
        """Поиск контактов по имени или номеру телефона"""
        with sqlite3.connect(self.db_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ? ORDER BY name",
                (f"%{query}%", f"%{query}%")
            )
            return [dict(row) for row in cursor.fetchall()]