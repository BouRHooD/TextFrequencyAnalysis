import csv
import os
from collections import Counter


def get_rang_from_i(words: dict) -> dict:
    """ Формирование ранга слов """
    words_value = words.values()                  # Получаем значения встречания слов в тексте
    words_set = set(words_value)                  # Множество удаляет одинаковые значения частот повторения слов
    words_rang = sorted(words_set, reverse=True)  # Передаем значения частоты встречания, порядок сортировки по убыванию (reverse=True)
    dict_rang = {words_rang[i]: i + 1 for i in range(len(words_rang))}  # Формируем словарь рангов по частоте встречания слов в тексте
    return dict_rang


def get_csv(path: str, words: list) -> None:
    """ Формирование csv файла результата ЧА """
    path = os.path.join(path, "out_analysis.csv")
    with open(path, "w", newline='') as file:
        name_columns = ['№', 'Словоформа', 'Частота I', 'Ранг', 'I норм (i\K)', 'r^(-1)', '0.1*r^(-1)']
        writer = csv.DictWriter(file, fieldnames=name_columns)
        writer.writeheader()
        for i, word in enumerate(words):
            writer.writerow({'№': i + 1,
                             'Словоформа': word[0],
                             'Частота I': word[1],
                             'Ранг': word[2],
                             'I норм (i\K)': word[3],
                             'r^(-1)': word[4],
                             '0.1*r^(-1)': word[5]})


def frequency_analysis_text(path_text: str, path_save_result: str) -> None:
    """ Выполнение частотного анализа текста """
    if not os.path.exists(path_save_result):
        os.mkdir(path_save_result)

    # Считываем текст из файла для анализа
    text = ""
    with open(path_text, encoding='utf-8', mode='r') as file:
        text = file.read()

    # Удаляем все знаки
    items_replace = r"?!.,:;/')(0123456789“”"
    for item in items_replace:
        text = text.replace(item, '')
    text = text.replace('"', '')
    # перевод всех слов в нижний регистр
    text = text.lower()
    # разделение текста на слова
    list_text = text.split()
    # удаление всех одиночных -
    list_text.remove('—')
    new_list = []
    for i, _word in enumerate(list_text):
        items_replace = r"?!.,:;/')(0123456789“”"
        for _char in items_replace:
            _word = _word.replace(_char, '')
            _word = _word.replace('"', '')
            _word = _word.replace('—', '')
        if _word is None or len(_word) <= 0: continue; 
        new_list.append(_word)
    list_text = new_list.copy()
    # Подсчет слов и выделение каждого слова
    dict_words_frequency_i = dict(Counter(list_text))
    # сортировка кол-во повторов слов
    dict_tuples = sorted(dict_words_frequency_i.items(), key=lambda item: item[1], reverse=True)
    dict_words_frequency_i = {k: v for k, v in dict_tuples}
    dict_rang = get_rang_from_i(dict_words_frequency_i)
    _words_count_K = len(dict_words_frequency_i)
    words_list_to_save = []
    for item in dict_words_frequency_i.items():
        _select_word = item[0]                               # Словоформа            
        _frequency_i = item[1]                               # Частота повторений в тексте
        _select_rang = dict_rang.get(_frequency_i)           # Получить ранг словоформы
        _i_normal = round(_frequency_i / _words_count_K, 4)  # Процент содержания в тексте
        _r_revers = round((_select_rang ** (-1)), 4)         # Обратный ранг
        _law_frequencies_words = round(0.1 * (_select_rang ** (-1)), 4)  # Закона частот слов (закон Ципфа в математике)
        _word_list_out = [_select_word, _frequency_i, _select_rang, _i_normal, _r_revers, _law_frequencies_words]
        words_list_to_save.append(_word_list_out)

    # Сохранение результата
    get_csv(path_save_result, words_list_to_save)

# Точка входа в программу (Запуск анализа)
if __name__ == "__main__":
    print("----->  Запустили частотный анализ текста  <-----")
    path_save = "frequency_analysis_result/"
    path_text = "text.txt"
    frequency_analysis_text(path_text, path_save)
    print("----->  Частотный анализ текста завершен   <-----")

