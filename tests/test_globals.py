from auroraapi.globals import Config

class TestGlobals(object):
	def test_create_config(self):
		c = Config()
		assert isinstance(c, Config)
		assert c != None
	
	def test_assign_config(self):
		c = Config()
		c.app_id = "app_id"
		c.app_token = "app_token"

		assert c.app_id == "app_id"
		assert c.app_token == "app_token"
		assert c.device_id == None