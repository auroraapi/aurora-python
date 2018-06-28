import json, pytest
from auroraapi.dialog.step.step import ContextWrapper, Step

STEP = {
  "id": "test",
  "type": "test",
  "data": {
    "stepName": "test_name",
  },
}

class TestContextWrapper(object):
  def test_create(self):
    c = ContextWrapper("value")
    assert c.value == "value"
  
  def test_context_dict(self):
    c = ContextWrapper({"a": 10})
    assert c.context_dict() == { "a": 10 }

class TestStep(object):
  def test_create(self):
    s = Step(STEP)

    assert s.id == STEP["id"]
    assert s.type == STEP["type"]
    assert s.raw == STEP
  
  def test___repr__(self):
    s = Step(STEP)
    assert repr(s) == json.dumps(STEP, indent=2)
  
  def test_execute(self):
    s = Step(STEP)
    with pytest.raises(NotImplementedError):
      s.execute(None, None)