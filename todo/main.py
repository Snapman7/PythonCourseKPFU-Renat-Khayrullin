import sqlite3
from datetime import datetime
import os


class TaskManager:
    def __init__(self, db_name='todo.db'):
        self.db_name = db_name
        self.init_database()

    def init_database(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                created_at TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT FALSE,
                completed_at TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def add_task(self):
        """Добавление новой задачи"""
        print("\n➕ ДОБАВЛЕНИЕ НОВОЙ ЗАДАЧИ")
        description = input("Введите описание задачи: ").strip()

        if not description:
            print("❌ Описание задачи не может быть пустым!")
            return

        created_at = datetime.now().isoformat()

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO tasks (description, created_at) VALUES (?, ?)',
            (description, created_at)
        )
        conn.commit()
        conn.close()

        print("✅ Задача успешно добавлена!")

    def view_tasks(self, show_completed=True):
        """Просмотр задач"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        if show_completed:
            cursor.execute('''
                SELECT * FROM tasks 
                ORDER BY completed, created_at DESC
            ''')
        else:
            cursor.execute('''
                SELECT * FROM tasks 
                WHERE completed = FALSE 
                ORDER BY created_at DESC
            ''')

        tasks = cursor.fetchall()
        conn.close()

        return tasks

    def display_tasks(self, tasks):
        """Отображение списка задач"""
        if not tasks:
            print("📝 Задачи не найдены")
            return

        print(f"\n{'ID':<3} {'Статус':<8} {'Дата создания':<20} {'Описание':<30}")
        print("-" * 70)

        for task in tasks:
            id, description, created_at, completed, completed_at = task

            # Форматируем дату
            created_date = datetime.fromisoformat(created_at).strftime("%d.%m.%Y %H:%M")

            # Статус задачи
            status = "✅ [x]" if completed else "⏳ [ ]"

            print(f"{id:<3} {status:<8} {created_date:<20} {description:<30}")

    def mark_completed(self):
        """Отметка задачи как выполненной"""
        tasks = self.view_tasks(show_completed=False)
        if not tasks:
            print("❌ Нет активных задач для отметки!")
            return

        self.display_tasks(tasks)

        try:
            task_id = int(input("\nВведите ID задачи для отметки как выполненной: "))
        except ValueError:
            print("❌ Неверный формат ID!")
            return

        completed_at = datetime.now().isoformat()

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE tasks SET completed = TRUE, completed_at = ? WHERE id = ? AND completed = FALSE',
            (completed_at, task_id)
        )

        if cursor.rowcount > 0:
            print("✅ Задача отмечена как выполненная!")
        else:
            print("❌ Задача не найдена или уже выполнена!")

        conn.commit()
        conn.close()

    def delete_task(self):
        """Удаление задачи"""
        tasks = self.view_tasks()
        if not tasks:
            print("❌ Нет задач для удаления!")
            return

        self.display_tasks(tasks)

        try:
            task_id = int(input("\nВведите ID задачи для удаления: "))
        except ValueError:
            print("❌ Неверный формат ID!")
            return

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))

        if cursor.rowcount > 0:
            print("✅ Задача успешно удалена!")
        else:
            print("❌ Задача не найдена!")

        conn.commit()
        conn.close()

    def get_statistics(self):
        """Получение статистики по задачам"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM tasks')
        total_tasks = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM tasks WHERE completed = TRUE')
        completed_tasks = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM tasks WHERE completed = FALSE')
        active_tasks = cursor.fetchone()[0]

        conn.close()

        return {
            'total': total_tasks,
            'completed': completed_tasks,
            'active': active_tasks,
            'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        }

    def show_statistics(self):
        """Отображение статистики"""
        stats = self.get_statistics()

        print("\n📊 СТАТИСТИКА ЗАДАЧ")
        print("=" * 30)
        print(f"📝 Всего задач: {stats['total']}")
        print(f"✅ Выполнено: {stats['completed']}")
        print(f"⏳ Активных: {stats['active']}")
        print(f"📈 Прогресс: {stats['completion_rate']:.1f}%")

    def show_menu(self):
        print("\n" + "=" * 50)
        print("✅ МЕНЕДЖЕР ЗАДАЧ")
        print("=" * 50)
        print("1. 👁️  Просмотреть все задачи")
        print("2. 📋 Просмотреть активные задачи")
        print("3. ➕ Добавить задачу")
        print("4. ✅ Отметить задачу как выполненную")
        print("5. 🗑️  Удалить задачу")
        print("6. 📊 Показать статистику")
        print("0. ❌ Выход")
        print("=" * 50)

    def run(self):
        while True:
            self.show_menu()
            choice = input("\nВыберите действие: ")

            if choice == '0':
                print("👋 До свидания!")
                break
            elif choice == '1':
                tasks = self.view_tasks(show_completed=True)
                self.display_tasks(tasks)
            elif choice == '2':
                tasks = self.view_tasks(show_completed=False)
                self.display_tasks(tasks)
            elif choice == '3':
                self.add_task()
            elif choice == '4':
                self.mark_completed()
            elif choice == '5':
                self.delete_task()
            elif choice == '6':
                self.show_statistics()
            else:
                print("❌ Неверный выбор!")

            input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    manager = TaskManager()
    manager.run()