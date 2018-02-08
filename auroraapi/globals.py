class GlobalStore(object):
	def __init__(self):
		self.app_id = None
		self.app_token = None
		self.device_id = None

__store = GlobalStore()