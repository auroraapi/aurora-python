import json

class APIException(Exception):
  """ The exception raised as result of an API error
  
  Attributes:
    id: The ID of the request that caused the error
    code: The Aurora-specific code of the error that occurred
    status: The HTTP status code
    type: A string representation of the HTTP status Code (e.g. BadRequest)
    message: A descriptive message detailing the error that occurred and possible
      resolutions
  """
  def __init__(self, id=None, status=None, code=None, type=None, message=None):
    """ Creates an APIException with the given arguments """
    self.id = id
    self.status = status
    self.code = code
    self.type = type
    self.message = message
    super(APIException, self).__init__("[{}] {}".format(code if code != None else status, message))
  
  def __repr__(self):
    """ Returns a JSON representation of the exception """
    return json.dumps({ 
      "id": self.id,
      "status": self.status,
      "code": self.code,
      "type": self.type,
      "message": self.message
    }, indent=2)
