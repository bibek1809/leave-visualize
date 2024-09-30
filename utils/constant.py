def create_response(success, code, error, message):
    return {
        "success": success,
        "code": code,
        "error": error,
        "message": message,
        "traceback": message,
        "description": message
    }



allowed_chars = 'a-zA-Z0-9_'
errorType = {
    'IndexError': 412,  # datanotfound
    'DatabaseError': 413,
    'UnsupportedMediaType': 414,
    'FileNotFoundError': 415,
    'EmptyDataError': 416,
    'InvalidPostRequest': 417,
    'BadRequestKeyError': 418,
    'Configuration Failed': 419
}
message = {
    'IndexError': 'No Data Found As Requested',
    'FileNotFoundError': 'File is Missing'

}





