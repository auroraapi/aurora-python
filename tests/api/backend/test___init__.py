import pytest
from auroraapi.globals import Config
from auroraapi.api.backend import CallParams, Credentials, Backend

class TestCredentials(object):
  def test_create(self):
    c = Credentials("app_id", "app_token", "device_id")
    assert c.app_id == "app_id"
    assert c.app_token == "app_token"
    assert c.device_id == "device_id"
  
  def test_headers(self):
    c = Credentials("app_id", "app_token", "device_id")
    assert len(c.headers) == 3
    assert c.headers["X-Application-ID"] == "app_id"
    assert c.headers["X-Application-Token"] == "app_token"
    assert c.headers["X-Device-ID"] == "device_id"
  
  def test_from_config(self):
    config = Config("app_id", "app_token", "device_id")
    c = Credentials.from_config(config)
    assert c.app_id == "app_id"
    assert c.app_token == "app_token"
    assert c.device_id == "device_id"

class TestBackend(object):
  def test_create(self):
    b = Backend("base_url", timeout=10000)
    assert b.base_url == "base_url"
    assert b.timeout == 10000
  
  def test_call(self):
    with pytest.raises(NotImplementedError):
      b = Backend("base_url")
      b.call(CallParams())
