import pytest, mock
from auroraapi.audio import AudioFile
from auroraapi.dialog.context import DialogContext
from auroraapi.dialog.graph import GraphEdge
from auroraapi.dialog.step.speech import SpeechStep, resolve_path
from auroraapi.globals import _config
from auroraapi.speech import Speech
from tests.mocks import *

class ContextWrapper(object):
  def __init__(self, val):
    self.val = val
  def context_dict(self):
    return self.val

class TestResolvePath(object):  
  def test_bad_user(self):
    c = DialogContext()
    assert resolve_path(c, "user.bad_key") == None
  
  def test_bad_step(self):
    c = DialogContext()
    assert resolve_path(c, "bad_step") == None
  
  def test_bad_path_obj(self):
    c = DialogContext()
    c.set_step("test", ContextWrapper({ "a": { "c": 2 } }))
    assert resolve_path(c, "test.a.b") == None
  
  def test_bad_path_array(self):
    c = DialogContext()
    c.set_step("test", ContextWrapper({ "a": [ "b", "c" ], "d": "e", "f": 10 }))
    assert resolve_path(c, "test.a.2") == None
    assert resolve_path(c, "test.a.1a") == None
    assert resolve_path(c, "test.a.a") == None
    assert resolve_path(c, "test.d.e") == None
    assert resolve_path(c, "test.d.1") == None
    assert resolve_path(c, "test.f.a") == None

  def test_step(self):
    c = DialogContext()
    data = { "a": { "b": [1,2] } }
    c.set_step("test", ContextWrapper(data))
    assert resolve_path(c, "test") == data
    assert resolve_path(c, "test.a") == data["a"]
    assert resolve_path(c, "test.a.b") == data["a"]["b"]
    assert resolve_path(c, "test.a.b.0") == data["a"]["b"][0]
    assert resolve_path(c, "test.a.b.1") == data["a"]["b"][1]

  def test_user(self):
    c = DialogContext()
    data = { "a": { "b": [1,2] } }
    c.set_data("test", "data")
    assert resolve_path(c, "user") == { "test": "data" }
    assert resolve_path(c, "user.test") == "data"

    c.set_data("test", data)
    assert resolve_path(c, "user") == { "test": data }
    assert resolve_path(c, "user.test") == data
    assert resolve_path(c, "user.test.a") == data["a"]
    assert resolve_path(c, "user.test.a.b") == data["a"]["b"]
    assert resolve_path(c, "user.test.a.b.0") == data["a"]["b"][0]
    assert resolve_path(c, "user.test.a.b.1") == data["a"]["b"][1]

SPEECH = {
  "id": "speech_id",
  "type": "speech",
  "data": {
    "text": "Hello",
    "stepName": "speech_name",
  },
}

SPEECH_WITH_USER_TEMPLATE = {
  "id": "speech_id",
  "type": "speech",
  "data": {
    "text": "Hello ${user.profile.first} ${user.profile.last}. How are you?",
    "stepName": "speech_name",
  },
}

SPEECH_WITH_STEP_TEMPLATE = {
  "id": "speech_id",
  "type": "speech",
  "data": {
    "text": "Hello ${listen_step.text}. How are you?",
    "stepName": "speech_name",
  },
}

class TestSpeechStep(object):
  def setup(self):
    self.orig_backend = _config.backend
    _config.backend = MockBackend()
    with open("tests/assets/empty.wav", "rb") as f:
      self.audio_data = f.read()
  
  def teardown(self):
    _config.backend = self.orig_backend
  
  def test_create(self):
    s = SpeechStep(SPEECH)
    assert s.step_name == SPEECH["data"]["stepName"]
    assert s.text == SPEECH["data"]["text"]
  
  def test_get_text_no_template(self):
    s = SpeechStep(SPEECH)
    assert s.get_text(None) == s.text
  
  def test_get_text_step_template(self):
    c = DialogContext()
    c.set_step("listen_step", ContextWrapper({ "text": "name" }))
    s = SpeechStep(SPEECH_WITH_STEP_TEMPLATE)
    assert s.get_text(c) == "Hello name. How are you?"
  
  def test_get_text_user_template(self):
    c = DialogContext()
    c.set_data("profile", { "first": "first", "last": "last" })
    s = SpeechStep(SPEECH_WITH_USER_TEMPLATE)
    assert s.get_text(c) == "Hello first last. How are you?"

  def test_get_text_missing_template(self):
    c = DialogContext()
    c.set_data("profile", { "first": "first" })
    s = SpeechStep(SPEECH_WITH_USER_TEMPLATE)
    assert s.get_text(c) == "Hello first None. How are you?"

  def test_execute(self):
    _config.backend.set_expected_response(200, self.audio_data)
    c = DialogContext()

    with mock.patch('pyaudio.PyAudio', new=MockPyAudio):
      s = SpeechStep(SPEECH)
      assert s.execute(c, GraphEdge()) == None
      assert isinstance(c.get_step(s.step_name), Speech)
      assert c.get_step(s.step_name).audio.audio == AudioFile(self.audio_data).audio
