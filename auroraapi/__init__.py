import api

APP_ID = None
APP_TOKEN = None

class TTS(object):
	@staticmethod
	def text_to_speech(text):
		return api.get_tts(APP_ID, APP_TOKEN, text)

class STT(object):
	@staticmethod
	def speech_to_text(audio):
		return api.get_stt(APP_ID, APP_TOKEN, audio)
