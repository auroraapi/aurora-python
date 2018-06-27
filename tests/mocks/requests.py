import json

class raw(object):
  def __init__(self, data):
    self.data = data if isinstance(data, bytes) else bytes(str(data), "utf-8")
  
  def read(self, **kwargs):
    return self.data

class request(object):
  def __init__(self, code, data, content_type):
    self.code = code
    self.data = data
    self.content_type = content_type
  
  def __call__(self, method, url, **kwargs):
    return response(self.code, self.data, self.content_type, kwargs)

class response(object):
  def __init__(self, code, data, content_type, req_args):
    self.status_code = code
    self.text = data
    self.raw = raw(data)
    self.headers = { "content-type": content_type }
    self.req_args = req_args
  
  def json(self):
    return json.loads(self.text)