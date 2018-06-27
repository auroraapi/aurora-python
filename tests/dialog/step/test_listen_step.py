import pytest, mock
from auroraapi.dialog.context import DialogContext
from auroraapi.dialog.graph import GraphEdge
from auroraapi.dialog.step.listen import ListenStep
from auroraapi.globals import _config
from auroraapi.interpret import Interpret
from auroraapi.text import Text
from tests.mocks import *

class ContextWrapper(object):
  def __init__(self, val):
    self.val = val
  def context_dict(self):
    return self.val

LISTEN_TEXT = {
  "id": "listen_id",
  "type": "listen",
  "data": {
    "model": "general",
    "interpret": False,
    "stepName": "listen_name",
    "length": "",
    "silenceLen": "",
  },
}

LISTEN_TEXT_CUSTOM = {
  "id": "listen_id",
  "type": "listen",
  "data": {
    "model": "general",
    "interpret": False,
    "stepName": "listen_name",
    "length": "3.5",
    "silenceLen": "1",
  },
}

LISTEN_INTERPRET = {
  "id": "listen_id",
  "type": "listen",
  "data": {
    "model": "general",
    "interpret": True,
    "stepName": "listen_name",
    "length": "",
    "silenceLen": "",
  },
}

class TestListenStep(object):
  def setup(self):
    self.orig_backend = _config.backend
    _config.backend = MockBackend()
  
  def teardown(self):
    _config.backend = self.orig_backend
  
  def test_create_default_text(self):
    s = ListenStep(LISTEN_TEXT)
    assert s.model == LISTEN_TEXT["data"]["model"]
    assert s.step_name == LISTEN_TEXT["data"]["stepName"]
    assert s.interpret == LISTEN_TEXT["data"]["interpret"]
    assert s.listen_settings["length"] == 0
    assert s.listen_settings["silence_len"] == 0.5
  
  def test_create_custom_text(self):
    s = ListenStep(LISTEN_TEXT_CUSTOM)
    assert s.listen_settings["length"] == 3.5
    assert s.listen_settings["silence_len"] == 1
  
  def test_create_default_interpret(self):
    s = ListenStep(LISTEN_INTERPRET)
    assert s.interpret
    assert s.listen_settings["length"] == 0
    assert s.listen_settings["silence_len"] == 0.5
  
  def test_execute_text(self):
    _config.backend.set_expected_response(200, { "transcript": "hello" })
    c = DialogContext()
    s = ListenStep(LISTEN_TEXT)
    with mock.patch('auroraapi.audio._pyaudio_record', new=mock_pyaudio_record):
      assert s.execute(c, GraphEdge()) == None
      assert isinstance(c.get_step("listen_name"), Text)
      assert c.get_step("listen_name").text == "hello"
  
  def test_execute_interpret(self):
    _config.backend.set_expected_responses(
      (200, {
        "transcript": "hello"
      }),
      (200, {
        "text": "hello",
        "intent": "greeting",
        "entities": {},
      }),
    )
    c = DialogContext()
    s = ListenStep(LISTEN_INTERPRET)
    with mock.patch('auroraapi.audio._pyaudio_record', new=mock_pyaudio_record):
      assert s.execute(c, GraphEdge()) == None
      assert isinstance(c.get_step("listen_name"), Interpret)
      assert c.get_step("listen_name").text == "hello"
      assert c.get_step("listen_name").intent == "greeting"
      assert c.get_step("listen_name").entities == {}
