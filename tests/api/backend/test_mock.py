import pytest
from auroraapi.api.backend import CallParams, Credentials, Backend
from auroraapi.errors import APIException
from tests.mocks.backend import MockBackend

class TestMockBackend(object):
  def test_create(self):
    b = MockBackend()
    assert b.responses == []
  
  def test_call_success(self):
    b = MockBackend()
    b.set_expected_response(200, { "data": "value" })
    
    r = b.call(CallParams())
    assert len(r) == 1
    assert r["data"] == "value"
  
  def test_call_failure_text(self):
    b = MockBackend()
    b.set_expected_response(400, "error")

    with pytest.raises(APIException) as e:
      r = b.call(CallParams())
      assert e.status == 400
      assert e.code == None
      assert e.message == "error"
  
  def test_call_failure_json(self):
    b = MockBackend()
    b.set_expected_response(400, { "code": "ErrorCode", "message": "error" })

    with pytest.raises(APIException) as e:
      r = b.call(CallParams())
      assert e.status == 400
      assert e.code == "ErrorCode"
      assert e.message == "error"

  def test_call_multiple(self):
    b = MockBackend()
    b.set_expected_responses((200, "first"), (200, "second"))

    assert b.call(CallParams()) == "first"
    assert b.call(CallParams()) == "second"
