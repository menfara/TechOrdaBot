import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import string
import json
import configparser

OUTPUT_FILENAME = 'data_dict.json' # название файла BIN - NPS для локальной связки для бота
IDS_OUTPUT_FILENAME = 'ids_dict.json' # название файла для локальной связки BIN - ID для бота
IDS_PAGE_ID = 65528724 # ID страницы(листа) со связкой BIN - ID IT школ


def read_config():
    """
    Чтение конфигурационного файла и получение URL Google Sheets.
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config.get('google_sheets', 'sheet_url')


def read_config_sheet_number():
    """
    Чтение конфигурационного файла и получение номера листа Google Sheets.
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    return int(config.get('google_sheets', 'sheet_number'))


def column_letter_to_index(letter):
    """
    Преобразование буквы столбца в индекс.

    Параметры:
    - letter (str): Буква столбца.

    Возвращает:
    - int: Индекс столбца (начинается с 0) или -1, если буква неверна.
    """
    letter = letter.upper()
    if letter in string.ascii_uppercase:
        return string.ascii_uppercase.index(letter)
    return -1


def get_ids_as_dict(key_column_letter, value_column_letter):
    """
    Получение данных из Google Sheets и преобразование их в словарь.

    Параметры:
    - key_column_letter (str): Буква столбца с ключами.
    - value_column_letter (str): Буква столбца со значениями.

    Возвращает:
    - dict: Словарь с данными из таблицы.
    """
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('astanahubproject-e12b990a0580.json', scope)
    client = gspread.authorize(creds)

    sheet_url = read_config()
    sheet = client.open_by_url(sheet_url).get_worksheet_by_id(IDS_PAGE_ID)
    all_values = sheet.get_all_values()

    key_col_index = column_letter_to_index(key_column_letter)
    value_col_index = column_letter_to_index(value_column_letter)

    if key_col_index == -1 or value_col_index == -1:
        print(f"Invalid column letter(s): '{key_column_letter}' or '{value_column_letter}'.")
        return {}

    if all_values:
        headers = all_values[0]
        if key_col_index >= len(headers) or value_col_index >= len(headers):
            print(f"Column indexes '{key_column_letter}' or '{value_column_letter}' are out of range.")
            return {}

        data_dict = {}
        for row in all_values[1:]:
            if len(row) > key_col_index and len(row) > value_col_index:
                key = str(row[key_col_index])
                value = str(row[value_col_index])
                data_dict[key] = value

        return data_dict
    else:
        print("No data found in the sheet.")
        return {}


def get_column_data_as_dict(key_column_letter, value_column_letter, extra_column_letter):
    """
    Получение данных из Google Sheets и преобразование их в словарь с дополнительными данными.

    Параметры:
    - key_column_letter (str): Буква столбца с ключами.
    - value_column_letter (str): Буква столбца со значениями.
    - extra_column_letter (str): Буква столбца с дополнительными данными.

    Возвращает:
    - dict: Словарь с данными из таблицы.
    """
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('astanahubproject-e12b990a0580.json', scope)
    client = gspread.authorize(creds)

    sheet_url = read_config()
    spreadsheet = client.open_by_url(sheet_url)

    # Извлечение идентификатора листа из URL
    match = re.search(r'gid=([0-9]+)', sheet_url)
    if match:
        sheet_id = int(match.group(1))
    else:
        raise ValueError("Не удалось извлечь gid из URL")

    print(f'sheet_id = {sheet_id}')
    # Открытие листа по ID
    sheet = spreadsheet.get_worksheet_by_id(sheet_id)
    all_values = sheet.get_all_values()

    key_col_index = column_letter_to_index(key_column_letter)
    value_col_index = column_letter_to_index(value_column_letter)
    extra_col_index = column_letter_to_index(extra_column_letter)

    if key_col_index == -1 or value_col_index == -1 or extra_col_index == -1:
        print(f"Invalid column letter(s): '{key_column_letter}', '{value_column_letter}', or '{extra_column_letter}'.")
        return {}

    if all_values:
        headers = all_values[0]
        if key_col_index >= len(headers) or value_col_index >= len(headers) or extra_col_index >= len(headers):
            print(f"Column indexes '{key_column_letter}', '{value_column_letter}', or '{extra_column_letter}' are out of range.")
            return {}

        data_dict = {}
        for row in all_values[1:]:
            if len(row) > key_col_index and len(row) > value_col_index and len(row) > extra_col_index:
                key = str(row[key_col_index])
                value = str(row[value_col_index]) + ' : ' + str(row[extra_col_index])
                data_dict[key] = value

        data_dict['name'] = sheet.title
        return data_dict
    else:
        print("No data found in the sheet.")
        return {}


def save_dict_to_file(data_dict, filename):
    """
    Сохранение словаря в файл JSON.

    Параметры:
    - data_dict (dict): Словарь с данными.
    - filename (str): Имя файла для сохранения.
    """
    with open(filename, 'w') as file:
        json.dump(data_dict, file, indent=4)


def load_dict_from_file():
    """
    Загрузка словаря из файла JSON.

    Возвращает:
    - dict: Словарь с данными из файла.
    """
    with open(OUTPUT_FILENAME, 'r') as file:
        return json.load(file)


def get_value_by_key(key):
    """
    Получение значения из словаря по ключу.

    Параметры:
    - key (str): Ключ для поиска значения.

    Возвращает:
    - str: Значение, соответствующее ключу, или None, если ключ не найден.
    """
    data_dict = load_dict_from_file()
    return data_dict.get(key, None)


def create_and_fill_dict_from_json(filename):
    """
    Создание словаря и заполнение его данными из файла JSON.

    Параметры:
    - filename (str): Имя файла для загрузки данных.

    Возвращает:
    - dict: Словарь с данными из файла.
    """
    with open(filename, 'r') as file:
        data_dict = json.load(file)
    return data_dict


def update_dict_from_sheet():
    """
    Обновление основного словаря данными из Google Sheets.
    """
    key_column_letter = 'B'
    value_column_letter = 'C'
    extra_column_letter = 'H'
    data_dict = get_column_data_as_dict(key_column_letter, value_column_letter, extra_column_letter)
    if data_dict:
        save_dict_to_file(data_dict, OUTPUT_FILENAME)
        print(f"Data Dictionary saved to '{OUTPUT_FILENAME}'.")


def update_ids_dict():
    """
    Обновление словаря идентификаторов данными из Google Sheets.
    """
    key_column_letter = 'B'
    value_column_letter = 'A'
    data_dict = get_ids_as_dict(key_column_letter, value_column_letter)
    if data_dict:
        save_dict_to_file(data_dict, IDS_OUTPUT_FILENAME)
        print(f"Data Dictionary saved to '{IDS_OUTPUT_FILENAME}'.")


def update_dicts():
    """
    Обновление всех словарей данными из Google Sheets.
    """
    update_dict_from_sheet()
    update_ids_dict()


if __name__ == "__main__":
    update_dicts()
