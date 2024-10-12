# phrase_loader.py

# Функция для загрузки фраз из файла
def load_phrases(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return []

# Загрузка фраз из файла frazi.txt
phrases = load_phrases('frazi.txt')

# Загрузка фраз из файла dogmati.txt для команды "напомни правила"
rules_phrases = load_phrases('dogmati.txt')
