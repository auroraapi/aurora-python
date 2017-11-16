import audio
import requests, functools

BASE_URL = "http://api.auroraapi.com"
TTS_URL = BASE_URL + "/v1/tts/"

def APIException(Exception):
	""" Raise an exception when querying the API """

def get_tts(app_id, app_token, text):
	headers = {
		"X-Application-ID": app_id,
		"X-Application-Token": app_token,
	}

	r = requests.get(TTS_URL, params=[("text", text)], headers=headers, stream=True)
	if r.status_code != 200:
		raise APIException(r.json()["message"])

	r.raw.read = functools.partial(r.raw.read, decode_content=True)
	return audio.AudioFile.create_from_http_stream(r.raw)