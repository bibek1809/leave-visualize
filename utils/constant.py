def create_response(success, code, error, message):
    return {
        "success": success,
        "code": code,
        "error": error,
        "message": message,
        "traceback": message,
        "description": message
    }

# Constants
file_category = {'CSV': 'csv', 'GOOGLESHEET': 'googlesheet'}
file_condition = {'CSV': 'first', 'GOOGLESHEET': 'second'}

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
# Responses
space_missing_response = create_response(
    False,
    406,
    'BAD_REQUEST',
    'Data Not found, SpaceID was not found'
)

file_missing_response = create_response(
    False,
    406,
    'BAD_REQUEST',
    'Data Not found, FileID was not found'
)

missing_response = create_response(
    False,
    406,
    'BAD_REQUEST',
    'Data Not found, Account Id/ BidataSource  was not found or Space Exist !'
)

duplicate_entry_response = create_response(
    False,
    406,
    'BAD_REQUEST',
    "The File Name Already Exists!"
)

date_missing_response = create_response(
    False,
    412,
    'Missing Date Column Or Date Pattern',
    'Either Date or Date Pattern is Missing in files'
)

invalid_file_response = create_response(
    False,
    410,
    'Invalid Request Initiated',
    'Invalid File Upload or Invalid Seprator Used'
)

invalid_category_response = create_response(
    False,
    410,
    'Invalid Request Initiated',
    'Invalid Category Used'
)

schema_not_match_response = create_response(
    False,
    418,
    'Invalid Schema Merge Request',
    'Invalid Schema Merge Request :- Files Mismatched'
)

# Query
restore_query = "call csv_db_restore()"
