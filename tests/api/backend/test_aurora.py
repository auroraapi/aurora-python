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


# class MockResponse(object):
# 	def __init__(self):
# 		self.status_code = 200
# 		self.headers = {}
# 		self.text = ""
  
# 	def json(self):
# 		return json.loads(self.text)


# class TestAPIUtils(object):
# 	def setup(self):
# 		_config.app_id = "appid"
# 		_config.app_token = "apptoken"
  
# 	def teardown(self):
# 		_config.app_id = None
# 		_config.app_token = None
  
# 	def test_get_headers(self):
# 		h = get_headers()
# 		assert h["X-Application-ID"] == _config.app_id
# 		assert h["X-Application-Token"] == _config.app_token
# 		assert h["X-Device-ID"] == _config.device_id
  
# 	def test_handle_error_no_error(self):
# 		handle_error(MockResponse())
  
# 	def test_handle_error_json(self):
# 		r = MockResponse()
# 		r.status_code = 400
# 		r.headers = { "content-type": "application/json" }
# 		r.text = json.dumps({
# 			"id": "id",
# 			"code": "MissingApplicationIDHeader",
# 			"type": "BadRequest",
# 			"status": 400,
# 			"message": "message"
# 		})

# 		with pytest.raises(APIException) as e:
# 			handle_error(r)
# 			assert e.id == "id"
# 			assert e.code == "MissingApplicationIDHeader"
# 			assert e.type == "BadRequest"
# 			assert e.status == 400
# 			assert e.message == "message"
  
# 	def test_handle_error_413(self):
# 		r = MockResponse()
# 		r.status_code = 413
# 		r.headers["content-type"] = "text/html"
# 		r.text = "Request entity too large"

# 		with pytest.raises(APIException) as e:
# 			handle_error(r)
# 			assert e.id == None
# 			assert e.status == 413
# 			assert e.type == "RequestEntityTooLarge"
# 			assert e.code == "RequestEntityTooLarge"
# 			assert e.message == "Request entity too large"
  
# 	def test_handle_error_other(self):
# 		r = MockResponse()
# 		r.status_code = 503
# 		r.headers["content-type"] = "text/html"
# 		r.text = "Service unavailable"


# 		with pytest.raises(APIException) as e:
# 			handle_error(r)
# 			assert e.id == None
# 			assert e.status == 413
# 			assert e.type == None
# 			assert e.code == None
# 			assert e.message == r.text
# 			assert str(e) == "[{}] {}".format(r.status_code, r.text)