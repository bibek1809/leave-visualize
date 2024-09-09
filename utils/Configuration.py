from utils.Env import Env
import os
import json
from database import DataSourceConfiguration
env = Env.instance()
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=10) 
DEFAULT_LIMITS = env.get_or_default("limiter.limits", "['100000 per minute']")
X_CUSTOM_PASSCODE = env.get_or_default("limiter.passcode", "passcode")


RAW_FILE_PATH = env.get_or_default("storage.path.raw", "raw")
TRANSFORM_FILE_PATH = env.get_or_default("storage.path.transform", "transform")
BASE_FOLDER_NAME = env.get_or_default("storage.name", "storage")


LEAVE_API_URL = env.get_or_default("api.url", "http://127.0.0.1:4448")
LEAVE_API_HEADER = 'Bearer ' + env.get_or_default("api.authorizer", "")
BASE_URL = env.get_or_default("base.url", "http://127.0.0.1:4448/api/v1/")
DATE_VALIDATION_LIMIT = env.get_or_default("data.date.validation", 10)
BASE_CODE = env.get_or_default("base.code","xxxx")

# def create_directories():
#     dir_list = [RAW_FILE_PATH, TRANSFORM_FILE_PATH, BASE_FOLDER_NAME]
#     for each_dir in dir_list:
#         os.makedirs(each_dir, exist_ok=True)


def check_configuration():
    # directory check
    # create_directories()
    data = {
        "database": DataSourceConfiguration.check_connection()

    }
    return data
