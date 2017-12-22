import audio, globals
import requests, functools

BASE_URL = "https://api.auroraapi.com"
TTS_URL = BASE_URL + "/v1/tts/"
STT_URL = BASE_URL + "/v1/stt/"
INTERPRET_URL = BASE_URL + "/v1/interpret/"

class APIException(Exception):
	""" Raise an exception when querying the API """

def get_headers():
	return {
		"X-Application-ID": globals.APP_ID,
		"X-Application-Token": globals.APP_TOKEN,
		"X-Device-ID": globals.DEVICE_ID,
	}

def get_tts(text):
	r = requests.get(TTS_URL, params=[("text", text)], headers=get_headers(), stream=True)
	if r.status_code != requests.codes.ok:
		if "application/json" in r.headers["content-type"]:
			raise APIException(r.json()["message"])
		raise APIException(r.text)

	r.raw.read = functools.partial(r.raw.read, decode_content=True)
	return audio.AudioFile.create_from_http_stream(r.raw)

def get_interpret(text):
	r = requests.get(INTERPRET_URL, params=[("text", text)], headers=get_headers())
	if r.status_code != requests.codes.ok:
		if "application/json" in r.headers["content-type"]:
			raise APIException(r.json()["message"])
		raise APIException(r.text)
	return r.json()

def get_stt(audio):
	r = requests.post(STT_URL, files={ "audio": audio.get_wav() }, headers=get_headers())
	if r.status_code != requests.codes.ok:
		if "application/json" in r.headers["content-type"]:
			raise APIException(r.json()["message"])
		if r.status_code == 413:
			raise APIException("Request entity too large")
		raise APIException(r.text)
	return r.json()
