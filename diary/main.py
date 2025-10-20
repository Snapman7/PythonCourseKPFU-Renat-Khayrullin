import sqlite3
import csv
from datetime import datetime, date
import os


class ExpenseTracker:
    def __init__(self, db_name='expenses.db'):
        self.db_name = db_name
        self.categories = ['еда', 'транспорт', 'развлечения', 'жилье', 'здоровье', 'образование', 'другое']
        self.init_database()

    def init_database(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def add_expense(self):
        """Добавление новой записи о расходе"""
        print("\n➕ ДОБАВЛЕНИЕ РАСХОДА")

        try:
            amount = float(input("Введите сумму расхода: "))
            if amount <= 0:
                print("❌ Сумма должна быть положительной!")
                return
        except ValueError:
            print("❌ Неверный формат суммы!")
            return

        print("\n📂 КАТЕГОРИИ:")
        for i, category in enumerate(self.categories, 1):
            print(f"{i}. {category}")

        try:
            category_choice = int(input(f"\nВыберите категорию (1-{len(self.categories)}): "))
            if 1 <= category_choice <= len(self.categories):
                category = self.categories[category_choice - 1]
            else:
                print("❌ Неверный выбор категории!")
                return
        except ValueError:
            print("❌ Неверный формат номера!")
            return

        # Дата (по умолчанию сегодня)
        date_input = input("Введите дату (ГГГГ-ММ-ДД) или Enter для сегодня: ").strip()
        if date_input:
            try:
                expense_date = datetime.strptime(date_input, '%Y-%m-%d').date()
            except ValueError:
                print("❌ Неверный формат даты! Используется сегодняшняя дата.")
                expense_date = date.today()
        else:
            expense_date = date.today()

        description = input("Введите описание (необязательно): ").strip() or None

        # Сохранение в базу данных
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO expenses (amount, category, date, description) VALUES (?, ?, ?, ?)',
            (amount, category, expense_date.isoformat(), description)
        )
        conn.commit()
        conn.close()

        print("✅ Расход успешно добавлен!")

    def view_all_expenses(self):
        """Просмотр всех расходов"""
        print("\n📋 ВСЕ РАСХОДЫ")
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM expenses 
            ORDER BY date DESC, id DESC
        ''')
        expenses = cursor.fetchall()
        conn.close()

        self.display_expenses(expenses)

    def view_expenses_by_date(self):
        """Просмотр расходов по дате"""
        date_input = input("Введите дату (ГГГГ-ММ-ДД): ").strip()
        try:
            target_date = datetime.strptime(date_input, '%Y-%m-%d').date()
        except ValueError:
            print("❌ Неверный формат даты!")
            return

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM expenses WHERE date = ? ORDER BY id DESC',
            (target_date.isoformat(),)
        )
        expenses = cursor.fetchall()
        conn.close()

        print(f"\n📅 РАСХОДЫ ЗА {target_date}:")
        self.display_expenses(expenses)

    def view_expenses_by_category(self):
        """Просмотр расходов по категории"""
        print("\n📂 КАТЕГОРИИ:")
        for i, category in enumerate(self.categories, 1):
            print(f"{i}. {category}")

        try:
            category_choice = int(input(f"\nВыберите категорию (1-{len(self.categories)}): "))
            if 1 <= category_choice <= len(self.categories):
                category = self.categories[category_choice - 1]
            else:
                print("❌ Неверный выбор категории!")
                return
        except ValueError:
            print("❌ Неверный формат номера!")
            return

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM expenses WHERE category = ? ORDER BY date DESC, id DESC',
            (category,)
        )
        expenses = cursor.fetchall()
        conn.close()

        print(f"\n📂 РАСХОДЫ ПО КАТЕГОРИИ '{category.upper()}':")
        self.display_expenses(expenses)

    def display_expenses(self, expenses):
        """Отображение списка расходов"""
        if not expenses:
            print("Расходы не найдены")
            return

        total = 0
        print(f"{'ID':<3} {'Дата':<12} {'Категория':<12} {'Сумма':<10} {'Описание':<20}")
        print("-" * 65)
        for expense in expenses:
            id, amount, category, expense_date, description, created_at = expense
            description_display = description if description else "—"
            print(f"{id:<3} {expense_date:<12} {category:<12} {amount:<10.2f} {description_display:<20}")
            total += amount

        print("-" * 65)
        print(f"{'ВСЕГО:':<27} {total:<10.2f}")

    def get_statistics(self):
        """Получение статистики по расходам"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Общая сумма расходов
        cursor.execute('SELECT SUM(amount) FROM expenses')
        total_amount = cursor.fetchone()[0] or 0

        # Сумма по категориям
        cursor.execute('''
            SELECT category, SUM(amount) 
            FROM expenses 
            GROUP BY category 
            ORDER BY SUM(amount) DESC
        ''')
        category_totals = cursor.fetchall()

        # Последние 30 дней
        thirty_days_ago = (date.today() - timedelta(days=30)).isoformat()
        cursor.execute('SELECT SUM(amount) FROM expenses WHERE date >= ?', (thirty_days_ago,))
        last_30_days = cursor.fetchone()[0] or 0

        conn.close()

        return {
            'total_amount': total_amount,
            'category_totals': category_totals,
            'last_30_days': last_30_days
        }

    def show_statistics(self):
        """Отображение статистики"""
        stats = self.get_statistics()

        print("\n📊 СТАТИСТИКА РАСХОДОВ")
        print("=" * 40)
        print(f"💰 Общая сумма расходов: {stats['total_amount']:.2f}")
        print(f"📅 За последние 30 дней: {stats['last_30_days']:.2f}")

        print("\n📂 РАСПРЕДЕЛЕНИЕ ПО КАТЕГОРИЯМ:")
        for category, amount in stats['category_totals']:
            percentage = (amount / stats['total_amount']) * 100 if stats['total_amount'] > 0 else 0
            print(f"  {category:<12}: {amount:>8.2f} ({percentage:>5.1f}%)")

    def export_to_csv(self):
        """Экспорт всех расходов в CSV"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM expenses ORDER BY date, category')
        expenses = cursor.fetchall()
        conn.close()

        filename = f"expenses_export_{date.today()}.csv"

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Amount', 'Category', 'Date', 'Description', 'Created At'])
            writer.writerows(expenses)

        print(f"✅ Расходы экспортированы в {filename}")

    def show_menu(self):
        print("\n" + "=" * 50)
        print("💰 ДНЕВНИК РАСХОДОВ")
        print("=" * 50)
        print("1. ➕ Добавить расход")
        print("2. 👁️  Просмотреть все расходы")
        print("3. 📅 Просмотреть расходы по дате")
        print("4. 📂 Просмотреть расходы по категории")
        print("5. 📊 Показать статистику")
        print("6. 📤 Экспорт в CSV")
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
                self.add_expense()
            elif choice == '2':
                self.view_all_expenses()
            elif choice == '3':
                self.view_expenses_by_date()
            elif choice == '4':
                self.view_expenses_by_category()
            elif choice == '5':
                self.show_statistics()
            elif choice == '6':
                self.export_to_csv()
            else:
                print("❌ Неверный выбор!")

            input("\nНажмите Enter для продолжения...")


# Необходимый импорт для работы с датами
from datetime import timedelta

if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.run()