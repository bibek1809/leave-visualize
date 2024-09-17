import os
from flask import Flask, request, render_template,jsonify
from flask_limiter import Limiter
from datetime import datetime
from flask_cors import CORS
from utils import Configuration, token_encryption, Visualize
from controller import AquisitionController,FileController,EtlController,VisualizeController
from middleware.checkXCustomPasscode import PasscodeValidator

complete_env_path = os.getcwd() + "/.env"
os.environ['env'] = complete_env_path

app = Flask(__name__, template_folder='templates')
CORS(app, resources=r"/*")

# 100 conncetion limit garni
# limits the connection from single ip per minutes
limiter = Limiter(app, default_limits=Configuration.DEFAULT_LIMITS)


# Add a before_request function for global rate limiting
@app.before_request
def before_request():
    # This decorator applies rate limiting to all routes
    limiter.limit("10/minute")(lambda: None)()


@app.before_request
def add_custom_header():
    # Configuration.create_directories()
    if request.endpoint != 'check_config' and request.endpoint !='app_start' and request.endpoint !='sample' and request.endpoint != 'download' and request.endpoint != 'swagger':
        message = {
            "success": False,
            "code": '400',
            "error": 'Unauthorized',
            "message":  'Unauthorized Access',
            "traceback": '',
            "description": ''
        }
        try:
            x_custom_passcode = request.headers.get("X-Custom-Passcode")
            is_valid = PasscodeValidator.validate(x_custom_passcode)
            if not is_valid:
                return message
        except Exception as e:
            message['message'] = str(e)
            return message


app.register_blueprint(FileController.file_blueprint)
app.register_blueprint(AquisitionController.aquisition)
app.register_blueprint(EtlController.etl)
app.register_blueprint(VisualizeController.viz)
# app.register_blueprint(SchemaController.schema_blueprint)
# app.register_blueprint(SpaceController.space_blueprint)
# app.register_blueprint(FileSpaceController.fileregistry_blueprint)
# app.register_blueprint(MongoController.mongo_blueprint)

@app.route("/health", methods=['GET'])
def check_config():
    return Configuration.check_configuration()

@app.route("/", methods=['GET'])
def app_start():
    return {"App Connection State":"Api Access"}

@app.route("/swagger", methods=['GET'])
def swagger():
    return render_template('swagger.html')


@app.route("/sample", methods=['GET', 'POST'])
def sample():
    if request.method == "GET":
        start_date = request.args.get('startdate', '2024-03-01')
        end_date = request.args.get('enddate', '2024-08-12')
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
        # Load the default data when the page is first loaded
        try:
            dataframe = Visualize.get_data(start_date,end_date)

        # Generate initial plots
            department_plot_path = Visualize.department_analysis(dataframe)
            supervisor_plot_path = Visualize.supervisor_analysis(dataframe)
            designation_plot_path = Visualize.designation_analysis(dataframe)
            leave_days_plot_path = Visualize.leave_days_analysis(dataframe)
            leave_type_plot_path = Visualize.leave_type_bar_chart(dataframe)

            # Render the HTML template with the default plots
            return render_template('sample.html',
                                department_plot=department_plot_path,
                                supervisor_plot=supervisor_plot_path,
                                designation_plot=designation_plot_path,
                                leave_days_plot=leave_days_plot_path,
                                leave_type_plot=leave_type_plot_path,
                                startdate=start_date,
                                        todate=end_date)
        except:
            return render_template('sample.html',
                                       department_plot=None,
                                       supervisor_plot=None,
                                       designation_plot=None,
                                       leave_days_plot=None,
                                       leave_type_plot=None,
                                       startdate=start_date,
                                        todate=end_date,
                                       error="Invalid date format.Check Data Range Properly")

    elif request.method == "POST":
        if request.form['Submit'] == 'Submit':  # Checking for button press
            # Get start and end dates from form submission
            start_date = request.form.get('startdate')
            end_date = request.form.get('todate')

            # Default to some dates if not provided
            if not start_date:
                start_date = '2024-03-01'
            if not end_date:
                end_date = '2024-08-12'

            # Validate the date format
            try:
                # start_date = datetime.strptime(start_date, '%Y-%m-%d')
                # end_date = datetime.strptime(end_date, '%Y-%m-%d')
                # # Get the dataframe based on the selected dates
                # date_diff = (end_date - start_date).days
                # if date_diff > 270:    
                #     return render_template('sample.html',
                #                        department_plot=None,
                #                        supervisor_plot=None,
                #                        designation_plot=None,
                #                        leave_days_plot=None,
                #                        leave_type_plot=None,
                #                        error="Check Date Range It is limited to 90 days")
                dataframe = Visualize.get_data(start_date, end_date)


                # Generate updated plots
                department_plot = Visualize.department_analysis(dataframe)
                supervisor_plot = Visualize.supervisor_analysis(dataframe)
                designation_plot = Visualize.designation_analysis(dataframe)
                leave_days_plot = Visualize.leave_days_analysis(dataframe)
                leave_type_plot = Visualize.leave_type_bar_chart(dataframe)
                print(start_date,end_date)
                # Return the updated plots as part of the rendered template
                return render_template('sample.html',
                                    department_plot=department_plot,
                                    supervisor_plot=supervisor_plot,
                                    designation_plot=designation_plot,
                                    leave_days_plot=leave_days_plot,
                                    leave_type_plot=leave_type_plot,
                                    startdate=start_date,
                                    todate=end_date)
            except:
                return render_template('sample.html',
                                       department_plot=None,
                                       supervisor_plot=None,
                                       designation_plot=None,
                                       leave_days_plot=None,
                                       leave_type_plot=None,
                                       startdate=start_date,
                                        todate=end_date,
                                       error="Invalid date format.Check Data Range Properly")



def start():
    Configuration.check_configuration()
    app.run(port=4448, debug=True, threaded=True)


if __name__ == '__main__':
    start()
