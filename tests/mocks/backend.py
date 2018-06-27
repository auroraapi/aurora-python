from auroraapi.api.backend import Backend
from auroraapi.errors import APIException

class MockBackend(Backend):
  def __init__(self):
    self.responses = []

  def set_expected_response(self, code, data):
    self.responses = [(code, data)]

  def set_expected_responses(self, *res):
    self.responses = list(res)

  def call(self, params):
    code, data = self.responses.pop(0)
    if code != 200:
      try:
        e = APIException(**data)
      except:
        e = APIException(message=data, status=code)
      raise e
    return data
