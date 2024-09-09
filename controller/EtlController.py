import json
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from utils import exception_handler
from utils.Acquisition import Acquisition
from database import DataSourceConfiguration
from utils.Configuration import executor
etl = Blueprint(
    "etl_controller", __name__, url_prefix="/api/v1/etl")
handler = Acquisition()
from services.RawService import RawService
@etl.app_errorhandler(Exception)
def handle_exception(e):
    return exception_handler.handle_exception(e)
aquisition_service = RawService(DataSourceConfiguration.mysql_datasource)

@etl.post("/load")
def insert_user_data():
    try:
        etl_datas = ['leave_txn','leave','user']
        # Get start_date and end_date from the request body
        data = request.form.to_dict() or {}
        inserted_date = data.get('inserted_date')
        etl_name = data.get('etl_name')
        # Default to yesterday and today if dates are not provided
        if not inserted_date:
            inserted_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        try:
            datetime.strptime(inserted_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
        if not etl_name:
            for i in etl_datas:
                executor.submit(handler.initiate_etl, i, inserted_date)
                return jsonify({"message": f"Insert operation started for {i} Table initiated as {inserted_date}"}), 200
        elif etl_name in etl_datas:
            executor.submit(handler.initiate_etl, etl_name, inserted_date)
            return jsonify({"message": f"Insert operation started for {etl_name} Table initiated as {inserted_date}"}), 200
        else:
            return jsonify({"error": "Invalid Input "}), 400
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON response"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

