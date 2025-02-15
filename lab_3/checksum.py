import json
import logging
import pathlib as Path
import pandas as pd

csv_file_path = "10.csv"
json_file_path = "patterns.json"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_json_file(json_file_path: str):
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

if __name__ == "__main__":


