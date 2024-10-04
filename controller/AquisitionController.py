import json
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from utils import exception_handler
from utils.Acquisition import Acquisition
from utils.Configuration import executor
from utils import Configuration
aquisition = Blueprint(
    "acquire_controller", __name__, url_prefix="/api/v1/acquire")
handler = Acquisition()

@aquisition.app_errorhandler(Exception)
def handle_exception(e):
    return exception_handler.handle_exception(e)


@aquisition.post("/insert")
def bulk_insert():
    try:
        # Get start_date and end_date from the request body
        data = request.form.to_dict() or {}
        category = data.get('category')
        category = category if category is not None else 'api'
        if category == 'api':
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            # Default to yesterday and today if dates are not provided
            if not start_date:
                start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            if not end_date:
                end_date = datetime.now().strftime('%Y-%m-%d')
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
                datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
            # Start the leave data fetching process asynchronously
            executor.submit(handler.fetch_all_leave_data, start_date, end_date)
            return jsonify({"message": f"Insert operation started for {start_date} to {end_date}"}), 200
        else:
            csv_file = request.files['csv_file']
            import time
            filename = ".".join(csv_file.filename.split('.')[:-1])+ '_' + str(time.time()).split(".")[0]+'.'+csv_file.filename.split('.')[-1]
            allowed_extension = ['tsv','csv']
            if filename.rsplit('.', 1)[1].lower() not in allowed_extension:
                return jsonify("Invalid File"), 410
            csv_file.save(Configuration.RAW_FILE_PATH+ filename)
            return jsonify({"message": f"Insert operation started for {start_date} to {end_date}"}), 200
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON response"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

