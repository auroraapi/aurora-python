class Credentials(object):
  def __init__(self, app_id=None, app_token=None, device_id=None):
    self.app_id = app_id
    self.app_token = app_token
    self.device_id = device_id
  
  @property
  def headers(self):
    return {
      "X-Application-ID": self.app_id,
      "X-Application-Token": self.app_token,
      "X-Device-ID": self.device_id,
    }

  @staticmethod
  def from_config(c):
    return Credentials(c.app_id, c.app_token, c.device_id)

class CallParams(object):
  def __init__(self, method="GET", path="/", credentials=Credentials(),
                     headers={}, query={}, body=None, chunked=False,
                     response_type="json"):
    self.method = method
    self.path = path
    self.credentials = credentials
    self.headers = headers
    self.query = query
    self.body = body
    self.chunked = chunked
    self.response_type = response_type

class Backend(object):
  def __init__(self, base_url, timeout=60000):
    self.base_url = base_url
    self.timeout = timeout

  def call(self, params):
    raise NotImplementedError()
