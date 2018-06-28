from auroraapi.api.backend import CallParams, Credentials
from auroraapi.audio import AudioFile

DIALOG_URL = "/v1/dialog/"
INTERPRET_URL = "/v1/interpret/"
STT_URL = "/v1/stt/"
TTS_URL = "/v1/tts/"

def get_tts(config, text):
  """ Performs a TTS query

  Args:
    config: an instance of globals.Config that contains the backend to be used
      and the credentials to be sent along with the request
    text: the text to convert to speech

  Returns:
    The raw WAV data returned from the TTS service
  """
  return config.backend.call(CallParams(
    path=TTS_URL,
    credentials=Credentials.from_config(config),
    query={ "text": text },
    chunked=True,
    response_type="raw",
  ))

def get_interpret(config, text, model):
  """ Performs an Interpret query

  Args:
    config: an instance of globals.Config that contains the backend to be used
      and the credentials to be sent along with the request
    text: the text to interpret
    model: the model to use to interpret

  Returns:
    A dictionary representation of the JSON response from the Interpret service
  """
  return config.backend.call(CallParams(
    path=INTERPRET_URL,
    credentials=Credentials.from_config(config),
    query={ "text": text, "model": model },
  ))

def get_stt(config, audio, stream=False):
  """ Performs an STT query

  Args:
    config: an instance of globals.Config that contains the backend to be used
      and the credentials to be sent along with the request
    audio: either an instance of an AudioFile or a function that returns a
      generator that supplies the audio data to be sent to the backend. If it is
      the latter, then the `stream` argument should be set to `True` as well.
    stream: pass `True` if the body is a function that returns a generator

  Returns:
    A dictionary representation of the JSON response from the STT service
  """
  return config.backend.call(CallParams(
    path=STT_URL,
    method="POST",
    credentials=Credentials.from_config(config),
    # audio can either be an AudioFile (in case all of the data is known) or
    # it can be a generator function, which emits data as it gets known. We need
    # to modify the request based on whether stream is True, in which case we assume
    # that audio is a generator function
    body=(audio() if stream else audio.get_wav())
  ))

def get_dialog(config, id):
  """ Gets a dialog from the Dialog service

  Args:
    config: an instance of globals.Config that contains the backend to be used
      and the credentials to be sent along with the request
    id: the ID of the dialog to get

  Returns:
    A dictionary representation of the JSON response from the Dialog service
  """
  return config.backend.call(CallParams(
    path=DIALOG_URL + id,
    credentials=Credentials.from_config(config),
  ))