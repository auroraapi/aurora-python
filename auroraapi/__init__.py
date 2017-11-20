import api, audio

APP_ID = None
APP_TOKEN = None

###########################################################
## Text to Speech                                        ##
###########################################################

class Text(object):
	""" Methods for dealing with text """
	def __init__(self, text):
		""" Initialize with some text """
		self.text = text

	def to_speech(self):
		""" Convert speech to text """
		return Speech(api.get_tts(APP_ID, APP_TOKEN, self.text))

###########################################################
## Speech to Text                                        ##
###########################################################

class Speech(object):
	""" Methods for dealing with speech """
	def __init__(self, audio):
		""" Initialize object with some audio
		`audio` must be an instance of `auroraapi.audio.AudioFile`. It is returned from all methods that return audio or speech
		"""
		self.audio = audio

	def to_text(self):
		""" Convert speech to text and get the prediction """
		return Text(api.get_stt(APP_ID, APP_TOKEN, self.audio)["prediction"])

	@staticmethod
	def continuously_listen(length=0, silence_len=2.5):
		""" Continually listen and yield speech demarcated by silent periods """
		while True:
			yield Speech.listen(length, silence_len)

	@staticmethod
	def listen(length=0, silence_len=2.5):
		""" Listen with the given parameters and return a speech segment """
		return Speech(audio.AudioFile.from_recording(length=length, silence_len=silence_len).trim_silent().pad_left(0.1))
