import pytest
from auroraapi.interpret import Interpret

class TestInterpret(object):
	def test_create_no_arguments(self):
		with pytest.raises(TypeError):
			Interpret()
	
	def test_create_wrong_type(self):
		with pytest.raises(TypeError):
			Interpret("test")
	
	def test_create(self):
		d = { "intent": "test", "entities": {} }
		i = Interpret(d)
		assert isinstance(i, Interpret)
		assert i.intent == "test"
		assert len(i.entities) == 0

		d = { "intent": "test", "entities": { "abc": "123" } }
		i = Interpret(d)
		assert isinstance(i, Interpret)
		assert i.intent == "test"
		assert len(i.entities) == 1
		assert i.entities["abc"] == "123"