import hashlib
import json
import logging
import re

import pandas as pd

VARIANT = 10
CSV_FILE_PATH = "10.csv"
JSON_FILE_PATH = "patterns.json"
RESULT_FILE = "result.json"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def calculate_checksum(row_numbers: list[int]) -> str:
    """
    Рассчитывает MD5 хеш для списка номеров строк.

    :param row_numbers: Список целочисленных номеров строк csv-файла,
                        на которых были найдены ошибки валидации.
    :return: MD5 хеш для проверки через GitHub Action.
    """
    row_numbers.sort()
    return hashlib.md5(json.dumps(row_numbers).encode('utf-8')).hexdigest()


def get_patterns(json_file_path: str):
    """
    Загружает JSON файл и возвращает его содержимое.

    :param json_file_path: Путь к JSON файлу.
    :return: Содержимое JSON файла в виде словаря или списка словарей.
             Возвращает None, если произошла ошибка.
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logging.info(f"Файл успешно загружен: {json_file_path}")
            return data

    except json.JSONDecodeError as e:
        logging.error(f"Ошибка при декодировании JSON: {e}")
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")

    return None


def get_data(csv_file_path: str):
    """
    Читает CSV файл с кодировкой utf-16 и разделителем ';'.

    :param csv_file_path: Путь к CSV файлу.
    :return: DataFrame с данными из CSV файла или None в случае ошибки.
    """
    try:
        logging.info(f"Чтение файла: {csv_file_path}")
        df = pd.read_csv(csv_file_path, encoding="utf-16", sep=";")
        logging.info("Файл успешно прочитан.")
        return df
    except FileNotFoundError:
        logging.error(f"Файл не найден: {csv_file_path}")
    except pd.errors.EmptyDataError:
        logging.error("Файл пуст.")
    except Exception as e:
        logging.error(f"Произошла ошибка при чтении файла: {e}")
    return None


def validate_data_with_patterns(df: pd.DataFrame, patterns: dict[str, str]) -> list[int]:
    """
    Проверяет строки DataFrame на соответствие паттернам регулярных выражений.

    :param df: DataFrame с данными для проверки.
    :param patterns: Словарь с паттернами регулярных выражений.
    :return: Список индексов строк, которые не соответствуют хотя бы одному паттерну.
    """
    invalid_indexes = set()  # Используем set для хранения уникальных индексов

    for column, pattern in patterns.items():
        if column in df.columns:
            compiled_pattern = re.compile(pattern)
            for index, value in df[column].items():
                if not compiled_pattern.match(str(value)):
                    invalid_indexes.add(index)
        else:
            logging.warning(f"Столбец '{column}' отсутствует в DataFrame.")

    return list(invalid_indexes)


def write_to_json(variant: str, checksum: str, file_path: str) -> None:
    """
    Создает JSON-объект с данными и записывает его в файл.

    :param variant: Значение для поля "variant".
    :param checksum: Значение для поля "checksum".
    :param file_path: Путь к файлу, в который будет записан JSON.
    """
    try:
        data = {
            "variant": variant,
            "checksum": checksum
        }

        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)

        logging.info(f"Данные успешно записаны в файл: {file_path}")
        print(f"Данные успешно записаны в файл: {file_path}")

    except Exception as e:
        logging.error(f"Ошибка при записи данных в файл {file_path}: {e}")
        print(f"Ошибка при записи данных в файл {file_path}: {e}")


if __name__ == "__main__":
    # Загрузка паттернов
    patterns = get_patterns(JSON_FILE_PATH)
    df = get_data(CSV_FILE_PATH)

    invalid_data = validate_data_with_patterns(df, patterns)
    checksum = calculate_checksum(invalid_data)
    write_to_json(VARIANT, checksum, RESULT_FILE)
