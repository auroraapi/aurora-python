import pytest, mock, json
from auroraapi.api.backend import CallParams, Credentials, Backend
from auroraapi.api.backend.aurora import AuroraBackend
from auroraapi.errors import APIException
from tests.mocks.requests import request

class TestAuroraBackend(object):
  def test_create(self):
    b = AuroraBackend("base_url")
    assert isinstance(b, AuroraBackend)
    assert b.base_url == "base_url"
  
  def test_call_success_json(self):
    b = AuroraBackend()
    with mock.patch('requests.request', new=request(200, '{"a":1}', "application/json")):
      assert b.call(CallParams()) == { "a": 1 }

  def test_call_success_raw(self):
    b = AuroraBackend()
    with mock.patch('requests.request', new=request(200, b'\0\0\0', "application/binary")):
      r = b.call(CallParams(response_type="raw"))
      assert r == b'\0\0\0'

  def test_call_success_text(self):
    b = AuroraBackend()
    with mock.patch('requests.request', new=request(200, 'test', "application/text")):
      r = b.call(CallParams(response_type="text"))
      assert r == 'test'

  def test_call_failure_api(self):
    b = AuroraBackend()
    error = {
      "id": "id",
      "code": "code",
      "type": "type",
      "status": 400,
      "message": "message",
    }
    with mock.patch('requests.request', new=request(400, json.dumps(error), "application/json")):
      with pytest.raises(APIException) as e:
        b.call(CallParams())
      assert e.value.id == error["id"]
      assert e.value.code == error["code"]
      assert e.value.type == error["type"]
      assert e.value.status == error["status"]
      assert e.value.message == error["message"]
  
  def test_call_failure_413(self):
    b = AuroraBackend()
    error = "Request size too large"
    with mock.patch('requests.request', new=request(413, error, "text/plain")):
      with pytest.raises(APIException) as e:
        b.call(CallParams())
      assert isinstance(e.value, APIException)
      assert e.value.id == None
      assert e.value.code == "RequestEntityTooLarge"
      assert e.value.type == "RequestEntityTooLarge"
      assert e.value.status == 413

  def test_call_failure_other(self):
    b = AuroraBackend()
    error = "unknown error"
    with mock.patch('requests.request', new=request(500, error, "text/plain")):
      with pytest.raises(APIException) as e:
        b.call(CallParams())
      assert isinstance(e.value, APIException)
      assert e.value.id == None
      assert e.value.code == None
      assert e.value.type == None
      assert e.value.status == 500
      assert e.value.message == error
