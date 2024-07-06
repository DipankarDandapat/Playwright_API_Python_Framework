import json
from pathlib import Path
from API_Utilities import logger_utility



log = logger_utility.customLogger()

BASE_PATH = Path.cwd().joinpath('testData')


def read_file(file_name):
    path = get_file_with_json_extension(file_name)
    log.info(f"Reading file from path: {path}")
    try:
        with path.open(mode='r') as f:
            data = json.load(f)
            log.info(f"Successfully read data from file: {file_name}")
            return data
    except FileNotFoundError:
        log.error(f"File not found: {path}")
        raise
    except json.JSONDecodeError as e:
        log.error(f"Error decoding JSON from file: {path}. Error: {e}")
        raise
    except Exception as e:
        log.error(f"An unexpected error occurred while reading file: {path}. Error: {e}")
        raise

def get_file_with_json_extension(file_name):
    if '.json' in file_name:
        path = BASE_PATH.joinpath(file_name)
    else:
        path = BASE_PATH.joinpath(f'{file_name}.json')
    log.info(f"Resolved file path: {path}")
    return path