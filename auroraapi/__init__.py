try:
	from api import *
	from audio import *
	from globals import __store
except:
	from .api import *
	from .audio import *
	from .globals import __store

###########################################################
## General Methods                                       ##
###########################################################

def set_app_id(id):
	__store.app_id = id

def set_app_token(token):
	__store.app_token = token

def set_device_id(id):
	__store.device_id = id

###########################################################
## Text to Speech                                        ##
###########################################################

class Text(object):
	""" Methods for dealing with text """
	def __init__(self, text):
		""" Initialize with some text """
		self.text = text

	def speech(self):
		""" Convert speech to text """
		return Speech(get_tts(self.text))
	
	def interpret(self):
		""" Interpret the text and return the results """
		return Interpret(get_interpret(self.text))

###########################################################
## Interpret                                             ##
###########################################################

class Interpret(object):
	def __init__(self, interpretation):
		""" Construct an interpret object from the API response """
		self.intent = interpretation["intent"]
		self.entities = interpretation["entities"]

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

	def text(self):
		""" Convert speech to text and get the prediction """
		return Text(get_stt(self.audio)["transcript"])

	@staticmethod
	def continuously_listen(length=0, silence_len=1.0):
		""" Continually listen and yield speech demarcated by silent periods """
		while True:
			yield Speech.listen(length, silence_len)

	@staticmethod
	def listen(length=0, silence_len=1.0):
		""" Listen with the given parameters and return a speech segment """
		return Speech(AudioFile.from_recording(length=length, silence_len=silence_len))
