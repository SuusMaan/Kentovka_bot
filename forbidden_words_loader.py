# forbidden_words_loader.py

import os

def load_forbidden_words(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return set(line.strip().lower() for line in file if line.strip())
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return set()

# Убедитесь, что путь корректный
absolute_path = os.path.join(os.path.dirname(__file__), 'forbidden_words.txt')
forbidden_words = load_forbidden_words(absolute_path)
