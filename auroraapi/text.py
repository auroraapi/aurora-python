from auroraapi.api import get_tts, get_interpret
from auroraapi.audio import AudioFile
from auroraapi.globals import _config

###########################################################
## Text to Speech                                        ##
###########################################################

class Text(object):
  """
  Text is a high-level object that encapsulates some text and allows you to
  perform actions such as converting it to speech, interpretting it, and more.
  """

  def __init__(self, text=""):
    """ Initialize with some text
    
    Args:
      text: the text that this object encapsulates
    """
    self.text = text
  
  def __repr__(self):
    return self.text

  def speech(self):
    """ Convert text to speech """
    from auroraapi.speech import Speech
    return Speech(AudioFile(get_tts(_config, self.text)))
  
  def interpret(self, model="general"):
    """ Interpret the text and return the results
    
    Calls the Aurora Interpret service on the encapsulated text using the given
    model and returns its interpretation

    Args:
      model: the specific model to use to interpret (default "general")
    
    Returns:
      An instance of Interpret, which contains the intent and entities parsed
      by the API call
    """
    from auroraapi.interpret import Interpret
    return Interpret(get_interpret(_config, self.text, model))
  
  def context_dict(self):
    return { "text": self.text }
