import functools
from auroraapi.audio import AudioFile, record, stream
from auroraapi.api import get_stt
from auroraapi.globals import _config

###########################################################
## Speech to Text                                        ##
###########################################################

class Speech(object):
  """
  Speech is a high-level object that encapsulates some audio and allows you to
  perform actions such as converting it to text, playing and recording audio,
  and more.

  Attributes:
    audio: an instance of audio.AudioFile. You can access methods on this to
      play, stop, and save the audio.
  """

  def __init__(self, audio):
    """ Initialize object with some audio
    
    Args:
      audio: an instance of audio.AudioFile
    """
    if not isinstance(audio, AudioFile):
      raise TypeError("audio must be an instance of auroraapi.audio.AudioFile")
    self.audio = audio

  def text(self):
    """ Convert speech to text and get the prediction
    
    Returns:
      And instance of Text, which contains the text returned by the STT API call.
      You can then further use the returned Text object to call other APIs.
    """
    from auroraapi.text import Text
    return Text(get_stt(_config, self.audio)["transcript"])
  
  def context_dict(self):
    return {}

###########################################################
## Listening functions                                   ##
###########################################################

def listen(length=0, silence_len=0.5):
  """ Listens with the given parameters and returns a speech segment
  
  Args:
    length: the length of time (seconds) to record for. If 0, it will record
      indefinitely, until the specified amount of silence (default 0.0)
    silence_len: the amount of silence (seconds) to allow before stopping the
      recording (ignored if length != 0) (default 0.5)
  
  Returns:
    A Speech object containing the recorded audio
  """
  return Speech(record(length=length, silence_len=silence_len))

def continuously_listen(length=0, silence_len=0.5):
  """ Continuously listens and yields Speech objects demarcated by silent periods
  
  Args:
    length: the length of time (seconds) to record for. If 0, it will record
      indefinitely, until the specified amount of silence (default 0.0)
    silence_len: the amount of silence (seconds) to allow before stopping the
      recording (ignored if length != 0) (default 0.5)
  
  Yields:
    Speech objects containin the recorded data in each demarcation
  """
  while True:
    yield listen(length, silence_len)

def listen_and_transcribe(length=0, silence_len=0.5):
  """
  Listen with the given parameters, but simulaneously stream the audio to the
  Aurora API, transcribe, and return a Text object. This reduces latency if
  you already know you want to convert the speech to text.
  
  Args:
    length: the length of time (seconds) to record for. If 0, it will record
      indefinitely, until the specified amount of silence (default 0.0)
    silence_len: the amount of silence (seconds) to allow before stopping the
      recording (ignored if length != 0) (default 0.5)
  
  Returns:
    A Text object containing the transcription of the recorded audio
  """
  from auroraapi.text import Text
  return Text(get_stt(_config, functools.partial(stream, length, silence_len), stream=True)["transcript"])

def continuously_listen_and_transcribe(length=0, silence_len=0.5):
  """
  Continuously listen with the given parameters, but simulaneously stream the
  audio to the Aurora API, transcribe, and return a Text object. This reduces
  latency if you already know you want to convert the speech to text.
  
  Args:
    length: the length of time (seconds) to record for. If 0, it will record
      indefinitely, until the specified amount of silence (default 0.0)
    silence_len: the amount of silence (seconds) to allow before stopping the
      recording (ignored if length != 0) (default 0.5)
  
  Yields:
    Text objects containing the transcription of the recorded audio from each
    demarcation
  """
  while True:
    yield listen_and_transcribe(length, silence_len)
