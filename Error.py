from werkzeug.exceptions import HTTPException
class AccessError(HTTPException):
    code = 400
    message = 'No message specified'

