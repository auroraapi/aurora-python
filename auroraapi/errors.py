import json

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
