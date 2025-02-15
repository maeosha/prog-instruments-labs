import json
import logging
import pathlib as Path
import pandas as pd

csv_file_path = "10.csv"
json_file_path = "patterns.json"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        # Проверка существования файла
        if not Path(json_file_path).exists():
            logging.error(f"Файл не найден: {json_file_path}")
            return None

        # Открытие и чтение файла
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


