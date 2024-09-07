import json
import time
import pandas as pd
from flask import Blueprint, jsonify, request, send_file
from utils import Configuration, exception_handler

aquisition = Blueprint(
    "acquire controller", __name__, url_prefix="/api/v1/acquire")


@aquisition.app_errorhandler(Exception)
def handle_exception(e):
    return exception_handler.handle_exception(e)


@aquisition.get("/")
def get_all_files():
    return 'HI'
