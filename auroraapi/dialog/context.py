class DialogContext(object):
	def __init__(self, on_update = lambda ctx: None):
		self.steps = {}
		self.user = {}
		self.udfs = {}
		self.previous_step = None
		self.current_step = None
		self.on_update = on_update
	
	def set_step(self, key, value):
		self.steps[key] = value
		self.on_update(self)

	def get_step(self, key, default=None):
		if not key in self.steps:
			return default
		return self.steps[key]
	
	def set_data(self, key, value):
		self.user[key] = value
		self.on_update(self)
	
	def get_data(self, key, default=None):
		if not key in self.user:
			return default
		return self.user[key]
    
	def set_current_step(self, step):
		self.previous_step = self.current_step
		self.current_step = step
		self.on_update(self)
	
	def get_current_step(self):
		return self.current_step
