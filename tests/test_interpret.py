import json, pytest
from auroraapi.interpret import Interpret

class TestInterpret(object):
	def test_create_no_arguments(self):
		with pytest.raises(TypeError):
			Interpret()
	
	def test_create_wrong_type(self):
		with pytest.raises(TypeError):
			Interpret("test")
	
	def test_create(self):
		d = { "text": "hello", "intent": "greeting", "entities": {} }
		i = Interpret(d)
		assert isinstance(i, Interpret)
		assert i.text == "hello"
		assert i.intent == "greeting"
		assert len(i.entities) == 0

		d = { "text": "remind me to eat", "intent": "set_reminder", "entities": { "task": "eat" } }
		i = Interpret(d)
		assert isinstance(i, Interpret)
		assert i.text == "remind me to eat"
		assert i.intent == "set_reminder"
		assert len(i.entities) == 1
		assert i.entities["task"] == "eat"

	def test___repr__(self):
		d = { "text": "remind me to eat", "intent": "set_reminder", "entities": { "task": "eat" } }
		i = Interpret(d)
		assert repr(i) == json.dumps(d, indent=2)

	def test_context_dict(self):
		d = { "text": "remind me to eat", "intent": "set_reminder", "entities": { "task": "eat" } }
		i = Interpret(d)
		assert json.dumps(i.context_dict()) == json.dumps(d)