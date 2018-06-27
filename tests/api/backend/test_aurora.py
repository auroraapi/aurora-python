import pytest
from auroraapi.api.backend import CallParams, Credentials, Backend
from auroraapi.api.backend.aurora import AuroraBackend
from auroraapi.errors import APIException

class TestAuroraBackend(object):
  pass

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