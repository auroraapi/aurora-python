import json
from auroraapi.errors import APIException

class TestAPIException(object):
	def test_create(self):
		e = APIException("id","status","code","type","message")
		assert isinstance(e, APIException)
		assert e.id == "id"
		assert e.status == "status"
		assert e.code == "code"
		assert e.type == "type"
		assert e.message == "message"
	
	def test_str(self):
		e = APIException("id","status","code","type","message")
		assert str(e) == "[{}] {}".format(e.code, e.message)

	def test_str_no_code(self):
		e = APIException("id","status",None,"type","message")
		assert str(e) == "[{}] {}".format(e.status, e.message)

	def test_repr(self):
		e = APIException("id","status","code","type","message")
		j = json.loads(repr(e))
		assert j["id"] == e.id
		assert j["status"] == e.status
		assert j["code"] == e.code
		assert j["type"] == e.type
		assert j["message"] == e.message
