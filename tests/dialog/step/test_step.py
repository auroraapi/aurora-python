import json, pytest
from auroraapi.dialog.step.step import Step

STEP = {
  "id": "test",
  "type": "test",
  "data": {
    "stepName": "test_name",
  },
}

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