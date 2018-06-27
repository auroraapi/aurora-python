import pytest, mock
from auroraapi.globals import _config
from auroraapi.audio import *
from auroraapi.errors import APIException
from auroraapi.speech import *
from auroraapi.text import Text
from tests.mocks import *

class TestSpeech(object):
	def setup(self):
		self.orig_backend = _config.backend
		_config.backend = MockBackend()
		with open("tests/assets/hw.wav", "rb") as f:
			self.audio = AudioFile(f.read())

	def teardown(self):
		_config.backend = self.orig_backend

	def test_create_no_argument(self):
		with pytest.raises(TypeError):
			Speech()
	
	def test_create_none(self):
		with pytest.raises(TypeError):
			Speech(None)
	
	def test_create_wrong_type(self):
		with pytest.raises(TypeError):
			Speech("string")
	
	def test_create(self):
		s = Speech(self.audio)
		assert s.audio == self.audio
	
	def test_context_dict(self):
		s = Speech(self.audio)
		d = s.context_dict()
		assert len(d) == 0

	def test_text(self):
		_config.backend.set_expected_response(200, { "transcript": "hello world" })
		s = Speech(self.audio)
		t = s.text()

		assert isinstance(t, Text)
		assert t.text.lower().strip() == "hello world"

class TestListen(object):
	def setup(self):
		self.orig_backend = _config.backend
		_config.backend = MockBackend()
		with open("tests/assets/hw.wav", "rb") as f:
			self.audio_file = AudioFile(f.read())
			
	def teardown(self):
		_config.backend = self.orig_backend

	def test_listen(self):
		with mock.patch('auroraapi.audio._pyaudio_record', new=mock_pyaudio_record):
			s = listen()
			assert isinstance(s, Speech)
			assert isinstance(s.audio, AudioFile)
			assert len(self.audio_file.audio) == len(s.audio.audio)

	def test_continuously_listen(self):
		with mock.patch('auroraapi.audio._pyaudio_record', new=mock_pyaudio_record):
			for s in continuously_listen():
				assert isinstance(s, Speech)
				assert isinstance(s.audio, AudioFile)
				assert len(self.audio_file.audio) == len(s.audio.audio)
				break
	
	def test_listen_and_transcribe(self):
		_config.backend.set_expected_response(200, { "transcript": "hello world" })
		with mock.patch('auroraapi.audio._pyaudio_record', new=mock_pyaudio_record):
			t = listen_and_transcribe()
			assert isinstance(t, Text)
			assert t.text.lower().strip() == "hello world"
	
	def test_continuously_listen_and_transcribe(self):
		_config.backend.set_expected_response(200, { "transcript": "hello world" })
		with mock.patch('auroraapi.audio._pyaudio_record', new=mock_pyaudio_record):
			for t in continuously_listen_and_transcribe():
				assert isinstance(t, Text)
				assert t.text.lower().strip() == "hello world"
				break
