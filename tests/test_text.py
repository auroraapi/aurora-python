import os, json, pytest
from auroraapi.globals import _config
from auroraapi.audio import AudioFile
from auroraapi.errors import APIException
from auroraapi.interpret import Interpret
from auroraapi.speech import Speech
from auroraapi.text import Text
from tests.mocks.backend import MockBackend

class TestText(object):
	def test_create(self):
		t = Text("test")
		assert isinstance(t, Text)
		assert t.text == "test"
	
	def test___repr__(self):
		t = Text("test")
		assert repr(t) == "test"
	
	def test_context_dict(self):
		t = Text("test")
		d = t.context_dict()
		assert len(d) == 1
		assert d["text"] == "test"

class TestTextInterpret(object):
	def setup(self):
		self.orig_backend = _config.backend
		_config.backend = MockBackend()
			
	def teardown(self):
		_config.backend = self.orig_backend

	def test_interpret(self):
		_config.backend.set_expected_response(200, { "text": "hello", "intent": "greeting", "entities": {} })
		t = Text("hello")
		i = t.interpret()
		assert isinstance(i, Interpret)
		assert i.intent == "greeting"

class TestTextSpeech(object):
	def setup(self):
		self.orig_backend = _config.backend
		_config.backend = MockBackend()
		with open("tests/assets/hw.wav", "rb") as f:
			self.audio_data = f.read()
			
	def teardown(self):
		_config.backend = self.orig_backend

	def test_speech(self):
		_config.backend.set_expected_response(200, self.audio_data)
		t = Text("hello")
		s = t.speech()
		assert isinstance(s, Speech)
		assert isinstance(s.audio, AudioFile)
		assert len(s.audio.audio) > 0
