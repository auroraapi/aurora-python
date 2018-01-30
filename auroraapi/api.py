import audio, globals
import requests, functools, json

BASE_URL = "https://api.auroraapi.com"
TTS_URL = BASE_URL + "/v1/tts/"
STT_URL = BASE_URL + "/v1/stt/"
INTERPRET_URL = BASE_URL + "/v1/interpret/"

class APIException(Exception):
	""" Raise an exception when querying the API """
	def __init__(self, id, status, code, type, message):
		self.id = id
		self.status = status
		self.code = code
		self.type = type
		self.message = message
		super(APIException, self).__init__("[{}] {}".format(code, message))
	
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
		"X-Application-ID": globals.APP_ID,
		"X-Application-Token": globals.APP_TOKEN,
		"X-Device-ID": globals.DEVICE_ID,
	}

def handle_error(r):
	if r.status_code != requests.codes.ok:
		if "application/json" in r.headers["content-type"]:
			raise APIException(**r.json())
		if r.status_code == 413:
			raise APIException(code="RequestEntityTooLarge", message="Request entity too large")
		raise APIException(r.text)

def get_tts(text):
	r = requests.get(TTS_URL, params=[("text", text)], headers=get_headers(), stream=True)
	handle_error(r)

	r.raw.read = functools.partial(r.raw.read, decode_content=True)
	return audio.AudioFile.create_from_http_stream(r.raw)

def get_interpret(text):
	r = requests.get(INTERPRET_URL, params=[("text", text)], headers=get_headers())
	handle_error(r)
	return r.json()

def get_stt(audio):
	r = requests.post(STT_URL, files={ "audio": audio.get_wav() }, headers=get_headers())
	handle_error(r)
	return r.json()
