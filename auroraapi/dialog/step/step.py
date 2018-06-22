import json

class Step(object):
  def __init__(self, step):
    self.id = step["id"]
    self.type = step["type"]
    self.raw = step
  
  def __repr__(self):
    return json.dumps(self.raw, indent=2)
  
  def execute(self, context, edge):
    raise NotImplementedError()
