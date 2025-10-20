import json
import csv
import sqlite3
from typing import List, Dict
from database import Database


class ExportImport:
    def __init__(self, db: Database):
        self.db = db

    def export_to_json(self, filename: str = "contacts.json") -> bool:
        """Экспорт контактов в JSON"""
        try:
            contacts = self.db.get_all_contacts()
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(contacts, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Ошибка при экспорте в JSON: {e}")
            return False

    def export_to_csv(self, filename: str = "contacts.csv") -> bool:
        """Экспорт контактов в CSV"""
        try:
            contacts = self.db.get_all_contacts()
            if not contacts:
                return False

            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=contacts[0].keys())
                writer.writeheader()
                writer.writerows(contacts)
            return True
        except Exception as e:
            print(f"Ошибка при экспорте в CSV: {e}")
            return False

    def import_from_json(self, filename: str) -> int:
        """Импорт контактов из JSON"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                contacts = json.load(f)

            imported_count = 0
            for contact in contacts:
                # Проверяем обязательные поля
                if 'name' in contact and 'phone' in contact:
                    self.db.add_contact(
                        contact['name'],
                        contact['phone'],
                        contact.get('email')
                    )
                    imported_count += 1

            return imported_count
        except Exception as e:
            print(f"Ошибка при импорте из JSON: {e}")
            return 0

    def import_from_csv(self, filename: str) -> int:
        """Импорт контактов из CSV"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                contacts = list(reader)

            imported_count = 0
            for contact in contacts:
                if 'name' in contact and 'phone' in contact:
                    self.db.add_contact(
                        contact['name'],
                        contact['phone'],
                        contact.get('email')
                    )
                    imported_count += 1

            return imported_count
        except Exception as e:
            print(f"Ошибка при импорте из CSV: {e}")
            return 0