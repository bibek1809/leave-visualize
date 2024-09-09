import os
from flask import Flask, request
from flask_limiter import Limiter
from flask_cors import CORS
from utils import Configuration, token_encryption
from controller import AquisitionController,FileController,EtlController
from middleware.checkXCustomPasscode import PasscodeValidator

complete_env_path = os.getcwd() + "/.env"
os.environ['env'] = complete_env_path

app = Flask(__name__)
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
    if request.endpoint != 'check_config' and request.endpoint !='app_start':
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


def start():
    Configuration.check_configuration()
    app.run(port=4448, debug=True, threaded=True)


if __name__ == '__main__':
    start()
