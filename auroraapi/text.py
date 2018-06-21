from auroraapi.api import get_tts, get_interpret

###########################################################
## Text to Speech                                        ##
###########################################################

class Text(object):
	"""
	Text is a high-level object that encapsulates some text and allows you to
	perform actions such as converting it to speech, interpretting it, and more.
	"""

	def __init__(self, text=""):
		"""
		Initialize with some text
		
		:param text the text that this object encapsulates
		:type  text string
		"""
		self.text = text
	
	def __repr__(self):
		return self.text

	def speech(self):
		""" Convert text to speech """
		from auroraapi.speech import Speech
		return Speech(get_tts(self.text))
	
	def interpret(self, model="general"):
		""" Interpret the text and return the results """
		from auroraapi.interpret import Interpret
		return Interpret(get_interpret(self.text, model))
	
	def context_dict(self):
		return { "text": self.text }
