import os
from flask import Flask, request, render_template
from flask_limiter import Limiter

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


@app.route("/sample", methods=['GET'])
def sample():
    dataframe = Visualize.get_data()
    department_plot_path = Visualize.department_analysis(dataframe)
    supervisor_plot_path = Visualize.supervisor_analysis(dataframe)
    designation_plot_path = Visualize.designation_analysis(dataframe)
    leave_days_plot_path = Visualize.leave_days_analysis(dataframe)
    leave_type_plot_path = Visualize.leave_type_bar_chart(dataframe)
    return render_template('sample.html', 
                           department_plot=department_plot_path, 
                           supervisor_plot=supervisor_plot_path, 
                           designation_plot=designation_plot_path, 
                           leave_days_plot=leave_days_plot_path,
                           leave_type_plot=leave_type_plot_path)



def start():
    Configuration.check_configuration()
    app.run(port=4448, debug=True, threaded=True)


if __name__ == '__main__':
    start()
