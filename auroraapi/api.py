import requests, functools, json, inspect
from auroraapi.globals import _config
from auroraapi.audio import AudioFile

BASE_URL = "https://api.auroraapi.com"
# BASE_URL = "http://localhost:3000"
TTS_URL = BASE_URL + "/v1/tts/"
STT_URL = BASE_URL + "/v1/stt/"
INTERPRET_URL = BASE_URL + "/v1/interpret/"
DIALOG_URL = BASE_URL + "/v1/dialog/"

class APIException(Exception):
	""" Raise an exception when querying the API """
	def __init__(self, id=None, status=None, code=None, type=None, message=None):
		self.id = id
		self.status = status
		self.code = code
		self.type = type
		self.message = message
		super(APIException, self).__init__("[{}] {}".format(code if code != None else status, message))
	
	def __repr__(self):
		return json.dumps({ 
			"id": self.id,
			"status": self.status,
			"code": self.code,
			"type": self.type,
			"message": self.message
		}, indent=2)

def get_headers():
	return {
		"X-Application-ID": _config.app_id,
		"X-Application-Token": _config.app_token,
		"X-Device-ID": _config.device_id,
	}

def handle_error(r):
	if r.status_code != requests.codes.ok:
		if "application/json" in r.headers["content-type"]:
			raise APIException(**r.json())
		if r.status_code == 413:
			raise APIException(code="RequestEntityTooLarge", message="Request entity too large", status=413, type="RequestEntityTooLarge")
		raise APIException(message=r.text, status=r.status_code)

def get_tts(text):
	r = requests.get(TTS_URL, params=[("text", text)], headers=get_headers(), stream=True)
	handle_error(r)

	r.raw.read = functools.partial(r.raw.read, decode_content=True)
	return AudioFile(r.raw.read())

def get_interpret(text, model):
	r = requests.get(INTERPRET_URL, params=[("text", text), ("model", model)], headers=get_headers())
	handle_error(r)
	return r.json()

def get_stt(audio, stream=False):
	# audio can either be an AudioFile (in case the all of the data is known) or
	# it can be a generator function, which emits data as it gets known. We need
	# to modify the request based on whether stream is True, in which case we assume
	# that audio is a generator function

	d = audio() if stream else audio.get_wav()
	r = requests.post(STT_URL, data=d, headers=get_headers())
	handle_error(r)
	return r.json()

def get_dialog(id):
	r = requests.get(DIALOG_URL + id, headers=get_headers())
	handle_error(r)
	return r.json()
