import os, json, pytest
from auroraapi.globals import _config
from auroraapi.api import APIException
from auroraapi.audio import AudioFile
from auroraapi.text import Text
from auroraapi.speech import Speech
from auroraapi.interpret import Interpret

class TestText(object):
	def test_create_no_argument(self):
		with pytest.raises(TypeError):
			t = Text()
	
	def test_create(self):
		t = Text("test")
		assert isinstance(t, Text)
		assert t.text == "test"

class TestTextNoCreds(object):
	def test_interpret(self):
		with pytest.raises(APIException):
			Text("test").interpret()
	
	def test_speech(self):
		with pytest.raises(APIException):
			Text("test").speech()

class TestTextInterpret(object):
	def setup(self):
		try:
			_config.app_id = os.environ["APP_ID"]
			_config.app_token = os.environ["APP_TOKEN"]
			_config.device_id = os.environ["DEVICE_ID"]
		except:
			pass
	
	def teardown(self):
		_config.app_id = None
		_config.app_token = None
		_config.device_id = None

	def test_interpret(self):
		t = Text("hello")
		i = t.interpret()
		assert isinstance(i, Interpret)
		assert i.intent == "greeting"
	
	def test_interpret_empty_string(self):
		with pytest.raises(APIException):
			Text("").interpret()

class TestTextSpeech(object):
	def setup(self):
		try:
			_config.app_id = os.environ["APP_ID"]
			_config.app_token = os.environ["APP_TOKEN"]
			_config.device_id = os.environ["DEVICE_ID"]
		except:
			pass
			
	def teardown(self):
		_config.app_id = None
		_config.app_token = None
		_config.device_id = None
	
	def test_speech(self):
		t = Text("hello")
		s = t.speech()
		assert isinstance(s, Speech)
		assert isinstance(s.audio, AudioFile)
		assert len(s.audio.audio) > 0
	
	def test_speech_empty_string(self):
		with pytest.raises(APIException):
			Text("").speech()
