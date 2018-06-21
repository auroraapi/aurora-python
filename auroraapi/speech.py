import functools
from auroraapi.audio import AudioFile, record, stream
from auroraapi.api import get_stt

###########################################################
## Speech to Text                                        ##
###########################################################

class Speech(object):
	"""
	Speech is a high-level object that encapsulates some audio and allows you to
	perform actions such as converting it to text, playing and recording audio,
	and more.

	Speech objects have an `audio` property, which is an instance of auroraapi.
	audio.AudioFile. You can access methods on this to play and stop the audio
	"""

	def __init__(self, audio):
		"""
		Initialize object with some audio
		
		:param audio an audio file
		:type  audio auroraapi.audio.AudioFile
		"""
		if not isinstance(audio, AudioFile):
			raise TypeError("audio must be an instance of auroraapi.audio.AudioFile")
		self.audio = audio

	def text(self):
		""" Convert speech to text and get the prediction """
		from auroraapi.text import Text
		return Text(get_stt(self.audio)["transcript"])
	
	def context_dict(self):
		return {}

###########################################################
## Listening functions                                   ##
###########################################################

def listen(length=0, silence_len=0.5):
	"""
	Listen with the given parameters and return a speech segment
	
	:param length      the length of time (seconds) to record for. If 0, it will record indefinitely, until the specified amount of silence
	:type  length      float
	:param silence_len the amount of silence (seconds) to allow before stoping (ignored if length != 0)
	:type  silence_len float
	"""
	return Speech(record(length=length, silence_len=silence_len))

def continuously_listen(length=0, silence_len=0.5):
	"""
	Continually listen and yield speech demarcated by silent periods
	
	:param length      the length of time (seconds) to record for. If 0, it will record indefinitely, until the specified amount of silence
	:type  length      float
	:param silence_len the amount of silence (seconds) to allow before stoping (ignored if length != 0)
	:type  silence_len float
	"""
	while True:
		yield listen(length, silence_len)

def listen_and_transcribe(length=0, silence_len=0.5):
	"""
	Listen with the given parameters, but simulaneously stream the audio to the
	Aurora API, transcribe, and return a Text object. This reduces latency if
	you already know you want to convert the speech to text.
	
	:param length      the length of time (seconds) to record for. If 0, it will record indefinitely, until the specified amount of silence
	:type  length      float
	:param silence_len the amount of silence (seconds) to allow before stoping (ignored if length != 0)
	:type  silence_len float
	"""
	from auroraapi.text import Text
	return Text(get_stt(functools.partial(stream, length, silence_len), stream=True)["transcript"])

def continuously_listen_and_transcribe(length=0, silence_len=0.5):
	"""
	Continuously listen with the given parameters, but simulaneously stream the
	audio to the Aurora API, transcribe, and return a Text object. This reduces
	latency if you already know you want to convert the speech to text.
	
	:param length      the length of time (seconds) to record for. If 0, it will record indefinitely, until the specified amount of silence
	:type  length      float
	:param silence_len the amount of silence (seconds) to allow before stoping (ignored if length != 0)
	:type  silence_len float
	"""
	while True:
		yield listen_and_transcribe(length, silence_len)
