import os
import zipfile
import datetime
import logging
from pathlib import Path


class BackupUtility:
    def __init__(self):
        self.setup_logging()

    def setup_logging(self):
        """Настройка системы логирования"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('backup.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def get_user_input(self):
        """Получение путей от пользователя"""
        print("\n🗃️ УТИЛИТА РЕЗЕРВНОГО КОПИРОВАНИЯ")
        print("=" * 50)

        # Исходная папка
        while True:
            source_dir = input("Введите путь к исходной папке: ").strip()
            if os.path.exists(source_dir) and os.path.isdir(source_dir):
                break
            else:
                print("❌ Папка не существует или путь неверный! Попробуйте снова.")

        # Папка для сохранения
        while True:
            backup_dir = input("Введите путь для сохранения архива: ").strip()
            if os.path.exists(backup_dir) and os.path.isdir(backup_dir):
                break
            else:
                create = input("Папка не существует. Создать? (y/n): ").lower()
                if create == 'y':
                    try:
                        os.makedirs(backup_dir, exist_ok=True)
                        break
                    except Exception as e:
                        print(f"❌ Ошибка создания папки: {e}")
                else:
                    print("Попробуйте другой путь.")

        return source_dir, backup_dir

    def create_backup_name(self, source_dir):
        """Создание имени для архива"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = os.path.basename(os.path.normpath(source_dir))
        return f"backup_{folder_name}_{timestamp}.zip"

    def get_total_size(self, source_dir):
        """Подсчет общего размера файлов для резервного копирования"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(source_dir):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except OSError:
                    continue
        return total_size

    def format_size(self, size_bytes):
        """Форматирование размера в читаемый вид"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"

    def create_backup(self, source_dir, backup_path):
        """Создание ZIP-архива"""
        total_size = self.get_total_size(source_dir)
        processed_size = 0

        self.logger.info(f"🚀 Начало резервного копирования: {source_dir}")
        self.logger.info(f"📁 Общий размер данных: {self.format_size(total_size)}")

        try:
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(source_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, source_dir)

                        try:
                            # Показываем прогресс
                            file_size = os.path.getsize(file_path)
                            zipf.write(file_path, arcname)
                            processed_size += file_size

                            progress = (processed_size / total_size) * 100
                            print(
                                f"\r📦 Прогресс: {progress:.1f}% ({self.format_size(processed_size)} / {self.format_size(total_size)})",
                                end="", flush=True)

                        except Exception as e:
                            self.logger.error(f"❌ Ошибка при добавлении файла {file_path}: {e}")

            print()  # Новая строка после прогресса
            return True

        except Exception as e:
            self.logger.error(f"❌ Критическая ошибка при создании архива: {e}")
            return False

    def run(self):
        """Основной метод запуска утилиты"""
        try:
            source_dir, backup_dir = self.get_user_input()
            backup_name = self.create_backup_name(source_dir)
            backup_path = os.path.join(backup_dir, backup_name)

            print(f"\n🔍 ИНФОРМАЦИЯ О РЕЗЕРВНОЙ КОПИИ:")
            print(f"• Источник: {source_dir}")
            print(f"• Назначение: {backup_path}")
            print(f"• Размер исходных данных: {self.format_size(self.get_total_size(source_dir))}")

            confirm = input("\nПродолжить создание резервной копии? (y/n): ").lower()
            if confirm != 'y':
                self.logger.info("❌ Операция отменена пользователем")
                return

            print("\n🔄 СОЗДАНИЕ РЕЗЕРВНОЙ КОПИИ...")
            success = self.create_backup(source_dir, backup_path)

            if success:
                final_size = os.path.getsize(backup_path)
                self.logger.info(f"✅ Резервная копия успешно создана: {backup_path}")
                self.logger.info(f"📊 Размер архива: {self.format_size(final_size)}")

                print(f"\n🎉 РЕЗЕРВНАЯ КОПИЯ УСПЕШНО СОЗДАНА!")
                print(f"📁 Файл: {backup_path}")
                print(f"💾 Размер: {self.format_size(final_size)}")
                print(f"📝 Лог сохранен в: backup.log")
            else:
                self.logger.error("❌ Создание резервной копии завершилось с ошибками")
                print("\n❌ Произошли ошибки при создании резервной копии. Проверьте backup.log для деталей.")

        except KeyboardInterrupt:
            self.logger.info("⚠️  Операция прервана пользователем")
            print("\n⚠️  Операция прервана")
        except Exception as e:
            self.logger.error(f"❌ Непредвиденная ошибка: {e}")
            print(f"\n❌ Произошла ошибка: {e}")


if __name__ == "__main__":
    utility = BackupUtility()
    utility.run()