import json
from flask import Blueprint, jsonify, request,Response
import base64
from datetime import datetime, timedelta
from utils import exception_handler,Visualize

from utils.Configuration import executor
viz = Blueprint(
    "visulaize_controller", __name__, url_prefix="/api/v1/viz")

@viz.app_errorhandler(Exception)
def handle_exception(e):
    return exception_handler.handle_exception(e)

@viz.route("/sample/download/<plot_type>", methods=['GET'])
def download(plot_type):
    try:
        data = request.form.to_dict() or {}
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        # Default to yesterday and today if dates are not provided
        if not start_date:
            start_date = '2024-01-01'
        if not end_date:
            end_date = '2024-08-12'
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
        # Ensure the plot_type is valid
        if plot_type not in ['department', 'supervisor', 'designation', 'leave']:
            return "Invalid plot type", 400
        # Extract optional filter parameters
        filters = {key: value for key, value in data.items() if key not in ['start_date', 'end_date']}
        print(filters)
        # Validate filter parameters if necessary (add your own validation logic if needed)
        for key, value in filters.items():
            if value is None or not isinstance(value, str):  # Example validation
                return jsonify({"error": f"Invalid filter for {key}. It must be a non-empty string."}), 400

        # Get the sample dataframe

        dataframe = Visualize.get_data(start_date,end_date,filters)
        if dataframe.empty:
            img_data = None
        else:
            # Generate the plot based on type
            if plot_type == 'department':
                plt = Visualize.department_analysis(dataframe)
            elif plot_type == 'supervisor':
                plt = Visualize.supervisor_analysis(dataframe)
            elif plot_type == 'designation':
                plt = Visualize.designation_analysis(dataframe)
            elif plot_type == 'leave':
                plt = Visualize.leave_days_analysis(dataframe)
            elif plot_type == 'leave_type':
                plt = Visualize.leave_type_bar_chart(dataframe)
            img_data = base64.b64decode(plt)

        # Return the file for download
        return Response(
            img_data,
            mimetype='image/png',
            headers={"Content-Disposition": f"attachment;filename={plot_type}_plot.png"}
        )
    except:
        return jsonify({"Status":"Invalid Request or Invalid Date or Invalid Parameters"})