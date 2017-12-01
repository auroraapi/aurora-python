import audio
import requests, functools

BASE_URL = "https://api.auroraapi.com"
TTS_URL = BASE_URL + "/v1/tts/"
STT_URL = BASE_URL + "/v1/stt/"

class APIException(Exception):
	""" Raise an exception when querying the API """

def get_tts(app_id, app_token, text):
	headers = {
		"X-Application-ID": app_id,
		"X-Application-Token": app_token,
	}

	r = requests.get(TTS_URL, params=[("text", text)], headers=headers, stream=True)
	if r.status_code != requests.codes.ok:
		raise APIException(r.json()["message"])

	r.raw.read = functools.partial(r.raw.read, decode_content=True)
	return audio.AudioFile.create_from_http_stream(r.raw)

def get_stt(app_id, app_token, audio):
	headers = {
		"X-Application-ID": app_id,
		"X-Application-Token": app_token,
	}

	files = {
		"audio": audio.data
	}

	r = requests.post(STT_URL, headers=headers, files=files)
	if r.status_code != requests.codes.ok or r.json().has_key("message"):
		raise APIException(r.json()["message"])
	return r.json()
