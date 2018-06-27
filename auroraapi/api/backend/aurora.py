import requests, functools, json, inspect
from auroraapi.api.backend import Backend
from auroraapi.errors import APIException

BASE_URL = "https://api.auroraapi.com/v1"

class AuroraBackend(Backend):
  def __init__(self, base_url=BASE_URL):
    super().__init__(base_url)
  
  def call(self, params):
    r = requests.request(
      params.method,
      self.base_url + params.path,
      data=params.body,
      stream=params.chunked,
      params=params.query.items(),
      headers={ **params.credentials.headers, **params.headers },
      timeout=self.timeout
    )

    if r.status_code != requests.codes.ok:
      if "application/json" in r.headers["content-type"]:
        raise APIException(**r.json())
      # Handle the special case where nginx doesn't return a JSON response for 413
      if r.status_code == 413:
        raise APIException(code="RequestEntityTooLarge", message="Request entity too large", status=413, type="RequestEntityTooLarge")
      # A non JSON error occurred (very strange)
      raise APIException(message=r.text, status=r.status_code)
    
    if params.response_type == "json":
      return r.json()
    if params.response_type == "raw":
      r.raw.read = functools.partial(r.raw.read, decode_content=True)
      return r.raw.read()
    return r.text
