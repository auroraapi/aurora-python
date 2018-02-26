from auroraapi.globals import Config

class TestGlobals(object):
	def test_create_config(self):
		c = Config()
		assert isinstance(c, Config)
		assert c != None
	
	def test_assign_config(self):
		c = Config()
		c.app_id = "test"
		c.app_token = "test123"

		assert c.app_id == "test"
		assert c.app_token == "test123"
		assert c.device_id == None