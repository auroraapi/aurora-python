import api

APP_ID = None
APP_TOKEN = None

class TTS(object):
	@staticmethod
	def text_to_speech(text):
		return api.get_tts(APP_ID, APP_TOKEN, text)
