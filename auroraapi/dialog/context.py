class DialogContext(object):
	def __init__(self, on_update = lambda ctx: None):
		self.step = {}
		self.user = {}
		self.udfs = {}
		self.current_step = None
		self.on_update = on_update
	
	def set_step_data(self, key, value):
		self.step[key] = value
		self.on_update(self)

	def get_step_data(self, key, default=None):
		if not key in self.step:
			return default
		return self.step[key]
	
	def set_user_data(self, key, value):
		self.user[key] = value
		self.on_update(self)
	
	def get_user_data(self, key, default=None):
		if not key in self.user:
			return default
		return self.user[key]
    
	def set_current_step(self, step):
		self.current_step = step
		self.on_update(self)
	
	def get_current_step(self):
		return self.current_step
