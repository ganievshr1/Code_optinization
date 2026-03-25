import requests
from collections import Counter
import re


def get_text(url):
    """
    Получение текста по URL.
    Оптимизация: использование сессии для повторного использования соединения.
    """
    session = requests.Session()
    response = session.get(url)
    return response.text


def count_word_frequencies_optimized(url, words_to_count):
    """
    Оптимизированная функция подсчёта частот слов.

    Основные улучшения:
    1. Текст загружается один раз для всех слов (вместо загрузки на каждое слово).
    2. Используется Counter для подсчёта всех слов за один проход.
    3. Слова приводятся к нижнему регистру и очищаются от знаков препинания.
    4. Возвращаются частоты только для запрошенных слов.
    """
    # Загружаем текст один раз
    text = get_text(url)

    # Очистка текста: приводим к нижнему регистру и заменяем знаки препинания на пробелы
    # Это улучшает точность подсчёта и уменьшает количество уникальных слов. Используем регулярку
    text_clean = re.sub(r'[^\w\s]', ' ', text.lower())

    # Разбиваем на слова
    words = text_clean.split()

    # Подсчитываем частоты всех слов за один проход (O(n) вместо O(n * m))
    word_counts = Counter(words)

    # Возвращаем частоты только для запрошенных слов
    return {word: word_counts.get(word, 0) for word in words_to_count}


def main():
    words_file = "words.txt"
    url = "https://eng.mipt.ru/why-mipt/"

    # Загружаем слова из файла
    with open(words_file, 'r') as file:
        # Используем генератор для экономии памяти
        words_to_count = [line.strip() for line in file if line.strip()]

    # Считаем частоты
    frequencies = count_word_frequencies_optimized(url, words_to_count)

    print(frequencies)


if __name__ == "__main__":
    main()