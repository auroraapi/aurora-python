from auroraapi.api.backend import Backend
from auroraapi.errors import APIException

class MockBackend(Backend):
  def __init__(self):
    self.response_code = 200
    self.response_data = ""
    self.called_params = {}

  def set_expected_response(self, code, data):
    self.response_code = code
    self.response_data = data
  
  def call(self, params):
    self.called_params = params
    if self.response_code != 200:
      try:
        e = APIException(**self.response_data)
      except:
        e = APIException(message=self.response_data, status=self.response_code)
      raise e
    return self.response_data
