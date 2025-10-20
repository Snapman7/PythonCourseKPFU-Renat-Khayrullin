import os
from database import Database
from export_import import ExportImport


class PhoneBook:
    def __init__(self):
        self.db = Database()
        self.exporter = ExportImport(self.db)

    def display_menu(self):
        """Отображение главного меню"""
        print("\n" + "=" * 50)
        print("📞 ТЕЛЕФОННАЯ КНИГА")
        print("=" * 50)
        print("1. 📋 Просмотреть все контакты")
        print("2. 🔍 Поиск контактов")
        print("3. ➕ Добавить контакт")
        print("4. ✏️  Редактировать контакт")
        print("5. 🗑️  Удалить контакт")
        print("6. 📤 Экспорт контактов")
        print("7. 📥 Импорт контактов")
        print("8. 🚪 Выход")
        print("=" * 50)

    def display_contacts(self, contacts=None):
        """Отображение списка контактов"""
        if contacts is None:
            contacts = self.db.get_all_contacts()

        if not contacts:
            print("\n📭 Контакты не найдены")
            return

        print(f"\n📋 Найдено контактов: {len(contacts)}")
        print("-" * 60)
        for contact in contacts:
            email = contact['email'] if contact['email'] else "не указан"
            print(f"ID: {contact['id']}")
            print(f"👤 Имя: {contact['name']}")
            print(f"📞 Телефон: {contact['phone']}")
            print(f"📧 Email: {email}")
            print("-" * 60)

    def add_contact(self):
        """Добавление нового контакта"""
        print("\n➕ ДОБАВЛЕНИЕ НОВОГО КОНТАКТА")
        print("-" * 30)

        name = input("Введите имя: ").strip()
        if not name:
            print("❌ Имя не может быть пустым!")
            return

        phone = input("Введите номер телефона: ").strip()
        if not phone:
            print("❌ Номер телефона не может быть пустым!")
            return

        email = input("Введите email (необязательно): ").strip()
        if not email:
            email = None

        contact_id = self.db.add_contact(name, phone, email)
        print(f"✅ Контакт успешно добавлен (ID: {contact_id})")

    def edit_contact(self):
        """Редактирование контакта"""
        print("\n✏️  РЕДАКТИРОВАНИЕ КОНТАКТА")
        print("-" * 30)

        try:
            contact_id = int(input("Введите ID контакта для редактирования: "))
        except ValueError:
            print("❌ Неверный формат ID!")
            return

        contact = self.db.get_contact(contact_id)
        if not contact:
            print("❌ Контакт с таким ID не найден!")
            return

        print(f"\nТекущие данные контакта:")
        print(f"👤 Имя: {contact['name']}")
        print(f"📞 Телефон: {contact['phone']}")
        print(f"📧 Email: {contact['email'] if contact['email'] else 'не указан'}")
        print("-" * 30)

        name = input(f"Введите новое имя [{contact['name']}]: ").strip()
        phone = input(f"Введите новый телефон [{contact['phone']}]: ").strip()
        email = input(f"Введите новый email [{contact['email'] if contact['email'] else ''}]: ").strip()

        # Если поле пустое, оставляем старое значение
        name = name if name else contact['name']
        phone = phone if phone else contact['phone']
        email = email if email else contact['email']
        if not email:
            email = None

        if self.db.update_contact(contact_id, name, phone, email):
            print("✅ Контакт успешно обновлен!")
        else:
            print("❌ Ошибка при обновлении контакта!")

    def delete_contact(self):
        """Удаление контакта"""
        print("\n🗑️  УДАЛЕНИЕ КОНТАКТА")
        print("-" * 30)

        try:
            contact_id = int(input("Введите ID контакта для удаления: "))
        except ValueError:
            print("❌ Неверный формат ID!")
            return

        contact = self.db.get_contact(contact_id)
        if not contact:
            print("❌ Контакт с таким ID не найден!")
            return

        print(f"\nВы действительно хотите удалить контакт:")
        print(f"👤 {contact['name']} - 📞 {contact['phone']}")

        confirm = input("Подтвердите удаление (y/N): ").lower()
        if confirm == 'y':
            if self.db.delete_contact(contact_id):
                print("✅ Контакт успешно удален!")
            else:
                print("❌ Ошибка при удалении контакта!")
        else:
            print("❌ Удаление отменено")

    def search_contacts(self):
        """Поиск контактов"""
        print("\n🔍 ПОИСК КОНТАКТОВ")
        print("-" * 30)

        query = input("Введите имя или номер телефона для поиска: ").strip()
        if not query:
            print("❌ Поисковый запрос не может быть пустым!")
            return

        contacts = self.db.search_contacts(query)
        self.display_contacts(contacts)

    def export_contacts(self):
        """Экспорт контактов"""
        print("\n📤 ЭКСПОРТ КОНТАКТОВ")
        print("-" * 30)
        print("1. 📄 Экспорт в JSON")
        print("2. 📊 Экспорт в CSV")
        print("3. ↩️  Назад")

        choice = input("Выберите формат: ").strip()

        if choice == '1':
            filename = input("Введите имя файла [contacts.json]: ").strip()
            filename = filename if filename else "contacts.json"
            if self.exporter.export_to_json(filename):
                print(f"✅ Контакты успешно экспортированы в {filename}")
            else:
                print("❌ Ошибка при экспорте!")

        elif choice == '2':
            filename = input("Введите имя файла [contacts.csv]: ").strip()
            filename = filename if filename else "contacts.csv"
            if self.exporter.export_to_csv(filename):
                print(f"✅ Контакты успешно экспортированы в {filename}")
            else:
                print("❌ Ошибка при экспорте!")

    def import_contacts(self):
        """Импорт контактов"""
        print("\n📥 ИМПОРТ КОНТАКТОВ")
        print("-" * 30)
        print("1. 📄 Импорт из JSON")
        print("2. 📊 Импорт из CSV")
        print("3. ↩️  Назад")

        choice = input("Выберите формат: ").strip()

        if choice in ['1', '2']:
            filename = input("Введите имя файла: ").strip()
            if not os.path.exists(filename):
                print("❌ Файл не найден!")
                return

            if choice == '1':
                count = self.exporter.import_from_json(filename)
            else:
                count = self.exporter.import_from_csv(filename)

            if count > 0:
                print(f"✅ Успешно импортировано {count} контактов")
            else:
                print("❌ Не удалось импортировать контакты")

    def run(self):
        """Запуск основного цикла приложения"""
        print("🚀 Запуск Телефонной книги...")

        while True:
            self.display_menu()
            choice = input("Выберите действие (1-8): ").strip()

            if choice == '1':
                self.display_contacts()
            elif choice == '2':
                self.search_contacts()
            elif choice == '3':
                self.add_contact()
            elif choice == '4':
                self.edit_contact()
            elif choice == '5':
                self.delete_contact()
            elif choice == '6':
                self.export_contacts()
            elif choice == '7':
                self.import_contacts()
            elif choice == '8':
                print("\n👋 До свидания!")
                break
            else:
                print("❌ Неверный выбор! Попробуйте снова.")

            input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    app = PhoneBook()
    app.run()