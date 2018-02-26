import os, json, array, pytest, mock
import auroraapi
from auroraapi.globals import _config
from auroraapi.api import APIException
from auroraapi.audio import *
from auroraapi.text import Text
from auroraapi.speech import *

def mock_pyaudio_record(a, b):
	with open("tests/assets/hw.wav", "rb") as f:
		yield array.array('h', AudioFile(f.read()).audio.raw_data)

class TestSpeech(object):
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
		with open("tests/assets/hw.wav", "rb") as f:
			Speech(AudioFile(f.read()))

	def test_text(self):
		with open("tests/assets/hw.wav", "rb") as f:
			s = Speech(AudioFile(f.read()))
			t = s.text()

			assert isinstance(t, Text)
			assert t.text.lower().strip() == "hello world"

class TestSpeechNoCreds(object):
	def test_text(self):
		with pytest.raises(APIException):
			with open("tests/assets/hw.wav", "rb") as f:
				Speech(AudioFile(f.read())).text()

class TestListen(object):
	def setup(self):
		with open("tests/assets/hw.wav", "rb") as f:
			self.audio_file = AudioFile(f.read())
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
		with mock.patch('auroraapi.audio._pyaudio_record', new=mock_pyaudio_record):
			t = listen_and_transcribe()
			assert isinstance(t, Text)
			assert t.text.lower().strip() == "hello world"
	
	def test_continuously_listen_and_transcribe(self):
		with mock.patch('auroraapi.audio._pyaudio_record', new=mock_pyaudio_record):
			for t in continuously_listen_and_transcribe():
				assert isinstance(t, Text)
				assert t.text.lower().strip() == "hello world"
				break
