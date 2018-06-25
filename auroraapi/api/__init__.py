from auroraapi.api.backend import CallParams, Credentials
from auroraapi.audio import AudioFile

TTS_URL = "/v1/tts/"
STT_URL = "/v1/stt/"
INTERPRET_URL = "/v1/interpret/"
DIALOG_URL = "/v1/dialog/"

def get_tts(config, text):
	return AudioFile(config.backend.call(CallParams(
		path=TTS_URL,
		credentials=Credentials.from_config(config),
		query={ "text": text },
		chunked=True,
		response_type="raw",
	)))

def get_interpret(config, text, model):
	return config.backend.call(CallParams(
		path=INTERPRET_URL,
		credentials=Credentials.from_config(config),
		query={ "text": text, "model": model },
	))

def get_stt(config, audio, stream=False):
	return config.backend.call(CallParams(
		path=STT_URL,
		credentials=Credentials.from_config(config),
    # audio can either be an AudioFile (in case all of the data is known) or
    # it can be a generator function, which emits data as it gets known. We need
    # to modify the request based on whether stream is True, in which case we assume
    # that audio is a generator function
		body=(audio() if stream else audio.get_wav())
	))

def get_dialog(config, id):
	return config.backend.call(CallParams(
		path=DIALOG_URL + id,
		credentials=Credentials.from_config(config),
	))