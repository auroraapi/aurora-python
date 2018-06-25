from auroraapi.api.backend.aurora import AuroraBackend

class Config(object):
	def __init__(self, app_id=None, app_token=None, device_id=None, backend=AuroraBackend()):
		self.app_id = app_id
		self.app_token = app_token
		self.device_id = device_id
		self.backend = backend

_config = Config()