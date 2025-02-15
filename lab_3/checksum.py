import hashlib
import json
import logging
import re
import pandas as pd

csv_file_path = "10.csv"
json_file_path = "patterns.json"
result_file = "result.json"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_checksum(row_numbers: list[int]) -> str:
    """
    :param row_numbers: список целочисленных номеров строк csv-файла, на которых были найдены ошибки валидации
    :return: md5 хеш для проверки через github action
    """
    row_numbers.sort()
    return hashlib.md5(json.dumps(row_numbers).encode('utf-8')).hexdigest()

def get_patterns(json_file_path: str):
    """
    Loads a JSON file and returns its content.

    Parameters:
    json_file_path (str): The path to the JSON file.

    Returns:
    Optional[Dict[str, Any] | List[Dict[str, Any]]]: The content of the JSON file as a dictionary or a list of dictionaries.
    Returns None if an error occurs.
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
    Reads a CSV file with utf-16 encoding and ';' delimiter.

    Parameters:
    csv_file_path (str): Path to the CSV file.

    Returns:
    Optional[pd.DataFrame]: DataFrame with data from the CSV file or None in case of an error.
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

    Parameters:
    df (pd.DataFrame): DataFrame с данными для проверки.
    patterns (Dict[str, str]): Словарь с паттернами регулярных выражений.

    Returns:
    List[int]: Список индексов строк, которые не соответствуют хотя бы одному паттерну.
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

# Пример использования
if __name__ == "__main__":
    # Загрузка паттернов
    patterns = get_patterns(json_file_path)
    df = get_data(csv_file_path)

    invalid_data = validate_data_with_patterns(df, patterns)
    result_hash_sum = calculate_checksum(invalid_data)


