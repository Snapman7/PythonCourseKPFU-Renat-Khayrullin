import os
import re
from collections import Counter


class TextAnalyzer:
    def __init__(self):
        self.text = ""
        self.encoding = "utf-8"

    def try_decode(self, file_path):
        """Попытка декодирования файла разными кодировками"""
        encodings = ['utf-8', 'cp1251', 'koi8-r', 'iso-8859-1', 'windows-1251']

        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    content = file.read()
                    # Проверяем, что файл читается нормально
                    if content.strip():
                        print(f"✅ Успешно загружено с кодировкой: {encoding}")
                        return content, encoding
            except (UnicodeDecodeError, UnicodeError):
                continue
            except Exception as e:
                continue

        return None, None

    def load_file(self):
        """Загрузка файла с попыткой разных кодировок"""
        file_path = input("Введите путь к текстовому файлу: ").strip()

        if not os.path.exists(file_path):
            print("❌ Файл не найден!")
            return False

        try:
            # Пробуем разные кодировки
            content, encoding = self.try_decode(file_path)

            if content is None:
                print("❌ Не удалось определить кодировку файла!")
                return False

            self.text = content
            self.encoding = encoding
            print("✅ Файл успешно загружен!")
            return True

        except Exception as e:
            print(f"❌ Ошибка при чтении файла: {e}")
            return False

    def load_file_manual(self):
        """Ручной выбор кодировки"""
        file_path = input("Введите путь к текстовому файлу: ").strip()

        if not os.path.exists(file_path):
            print("❌ Файл не найден!")
            return False

        print("\n📝 Доступные кодировки:")
        encodings = ['utf-8', 'cp1251', 'koi8-r', 'iso-8859-1', 'windows-1251']
        for i, encoding in enumerate(encodings, 1):
            print(f"{i}. {encoding}")

        try:
            choice = int(input("Выберите кодировку (1-5): "))
            if 1 <= choice <= len(encodings):
                encoding = encodings[choice - 1]
            else:
                encoding = 'utf-8'
        except ValueError:
            encoding = 'utf-8'

        try:
            with open(file_path, 'r', encoding=encoding) as file:
                self.text = file.read()
                self.encoding = encoding
            print("✅ Файл успешно загружен!")
            return True
        except UnicodeDecodeError:
            print("❌ Ошибка декодирования! Попробуйте другую кодировку.")
            return False
        except Exception as e:
            print(f"❌ Ошибка при чтении файла: {e}")
            return False

    def count_words(self):
        """Подсчет общего количества слов"""
        words = re.findall(r'\b\w+\b', self.text)
        return len(words)

    def count_characters(self):
        """Подсчет символов (с пробелами и без)"""
        with_spaces = len(self.text)
        without_spaces = len(self.text.replace(' ', '').replace('\n', '').replace('\t', ''))
        return with_spaces, without_spaces

    def count_sentences(self):
        """Подсчет количества предложений"""
        # Разделяем по . ! ? и проверяем, что есть текст
        sentences = re.split(r'[.!?]+', self.text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 1]
        return len(sentences)

    def count_unique_words(self):
        """Подсчет уникальных слов"""
        words = re.findall(r'\b\w+\b', self.text.lower())
        return len(set(words))

    def top_frequent_words(self, n=10):
        """Топ-N самых частых слов"""
        words = re.findall(r'\b\w+\b', self.text.lower())
        # Исключаем короткие слова (меньше 3 букв)
        words = [word for word in words if len(word) > 2]
        word_counts = Counter(words)
        return word_counts.most_common(n)

    def count_paragraphs(self):
        """Подсчет количества абзацев"""
        paragraphs = [p for p in self.text.split('\n\n') if p.strip()]
        return len(paragraphs)

    def analyze_text(self):
        """Полный анализ текста"""
        if not self.text:
            print("❌ Сначала загрузите файл!")
            return None

        print("\n🔍 ВЫПОЛНЯЕТСЯ АНАЛИЗ ТЕКСТА...")

        total_words = self.count_words()
        chars_with_spaces, chars_without_spaces = self.count_characters()
        sentences = self.count_sentences()
        unique_words = self.count_unique_words()
        paragraphs = self.count_paragraphs()
        top_words = self.top_frequent_words(10)

        analysis = {
            'total_words': total_words,
            'characters_with_spaces': chars_with_spaces,
            'characters_without_spaces': chars_without_spaces,
            'sentences': sentences,
            'paragraphs': paragraphs,
            'unique_words': unique_words,
            'top_words': top_words,
            'word_length_avg': chars_without_spaces / total_words if total_words > 0 else 0,
            'sentence_length_avg': total_words / sentences if sentences > 0 else 0
        }

        return analysis

    def generate_report(self, analysis):
        """Генерация отчета"""
        if not analysis:
            return

        report = f"""📊 ОТЧЕТ АНАЛИЗА ТЕКСТА
{'=' * 50}

📝 ОСНОВНЫЕ СТАТИСТИКИ:
• Общее количество слов: {analysis['total_words']:,}
• Количество символов (с пробелами): {analysis['characters_with_spaces']:,}
• Количество символов (без пробелов): {analysis['characters_without_spaces']:,}
• Количество предложений: {analysis['sentences']:,}
• Количество абзацев: {analysis['paragraphs']:,}
• Количество уникальных слов: {analysis['unique_words']:,}

📈 ПЛОТНОСТЬ ТЕКСТА:
• Средняя длина слова: {analysis['word_length_avg']:.1f} символов
• Средняя длина предложения: {analysis['sentence_length_avg']:.1f} слов
• Процент уникальных слов: {(analysis['unique_words'] / analysis['total_words'] * 100):.1f}%

🔥 ТОП-10 САМЫХ ЧАСТОТНЫХ СЛОВ:
"""

        for i, (word, count) in enumerate(analysis['top_words'], 1):
            frequency = (count / analysis['total_words']) * 100
            report += f"{i:2d}. '{word}': {count:,} раз ({frequency:.2f}%)\n"

        report += f"\n{'=' * 50}"
        report += f"\n📅 Отчет сгенерирован: {self.get_timestamp()}"

        return report

    def get_timestamp(self):
        """Получение текущей даты и времени"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save_report(self, report):
        """Сохранение отчета в файл"""
        if not report:
            return

        timestamp = self.get_timestamp().replace(':', '-').replace(' ', '_')
        output_file = f"text_analysis_report_{timestamp}.txt"

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ Отчет сохранен в файл: {output_file}")
            return output_file
        except Exception as e:
            print(f"❌ Ошибка при сохранении отчета: {e}")
            return None

    def show_menu(self):
        print("\n" + "=" * 50)
        print("📖 АНАЛИЗАТОР ТЕКСТА")
        print("=" * 50)
        print("1. 📂 Автозагрузка файла (автоопределение кодировки)")
        print("2. 🔧 Ручная загрузка файла (выбор кодировки)")
        print("3. 🔍 Проанализировать текст")
        print("4. 💾 Сохранить отчет")
        print("5. 📊 Показать статистику")
        print("6. 📝 Показать образец текста")
        print("0. ❌ Выход")
        print("=" * 50)

    def display_statistics(self, analysis):
        """Отображение статистики в консоли"""
        if not analysis:
            return

        print("\n📊 СТАТИСТИКА ТЕКСТА:")
        print(f"• 📝 Слов: {analysis['total_words']:,}")
        print(f"• 🔤 Символов (с пробелами): {analysis['characters_with_spaces']:,}")
        print(f"• 🔡 Символов (без пробелов): {analysis['characters_without_spaces']:,}")
        print(f"• 📄 Предложений: {analysis['sentences']:,}")
        print(f"• 📑 Абзацев: {analysis['paragraphs']:,}")
        print(f"• 🎯 Уникальных слов: {analysis['unique_words']:,}")

        print(f"\n📈 ПЛОТНОСТЬ:")
        print(f"• 📏 Средняя длина слова: {analysis['word_length_avg']:.1f} симв.")
        print(f"• 📐 Средняя длина предложения: {analysis['sentence_length_avg']:.1f} слов")

        print("\n🔥 ТОП-10 СЛОВ:")
        for i, (word, count) in enumerate(analysis['top_words'], 1):
            percentage = (count / analysis['total_words']) * 100
            print(f"  {i:2d}. '{word}': {count:,} раз ({percentage:.1f}%)")

    def show_text_sample(self):
        """Показать образец текста"""
        if not self.text:
            print("❌ Текст не загружен!")
            return

        sample_length = min(500, len(self.text))
        sample = self.text[:sample_length]

        print(f"\n📝 ОБРАЗЕЦ ТЕКСТА (первые {sample_length} символов):")
        print("=" * 50)
        print(sample)
        if len(self.text) > sample_length:
            print("... [текст продолжается]")
        print("=" * 50)

    def run(self):
        current_analysis = None

        while True:
            self.show_menu()
            choice = input("\nВыберите действие: ")

            if choice == '0':
                print("👋 До свидания!")
                break
            elif choice == '1':
                if self.load_file():
                    print(f"📖 Загружено символов: {len(self.text):,}")
            elif choice == '2':
                if self.load_file_manual():
                    print(f"📖 Загружено символов: {len(self.text):,}")
            elif choice == '3':
                current_analysis = self.analyze_text()
                if current_analysis:
                    self.display_statistics(current_analysis)
            elif choice == '4':
                if current_analysis:
                    report = self.generate_report(current_analysis)
                    self.save_report(report)
                else:
                    print("❌ Сначала выполните анализ текста!")
            elif choice == '5':
                if current_analysis:
                    self.display_statistics(current_analysis)
                else:
                    print("❌ Сначала выполните анализ текста!")
            elif choice == '6':
                self.show_text_sample()
            else:
                print("❌ Неверный выбор!")

            input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    analyzer = TextAnalyzer()
    analyzer.run()