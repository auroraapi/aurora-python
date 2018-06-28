import json

class ContextWrapper(object):
  """ Wraps a value in a class that has a context_dict function
  
  For steps that don't save objects with a `context_dict` into the dialog
  context, this class provides such a functionality.
  
  Attributes:
    value: the value to wrap
  """
  def __init__(self, value):
    """ Creates a ContextWrapper for the given value """
    self.value = value
  
  def context_dict(self):
    """ Returns the value in a dictionary similar to other steps """
    return self.value


class Step(object):
  """ The abstract base Step class

  Each step in the Dialog Builder is a subclass of this class. It provides
  the structure for each step and ensures consistency when the developer
  needs to access a step.

  Attributes:
    id: the internal ID of the step (this is NOT the step name)
    type: the type of node (string representation, e.g. "listen", "speech", "udf")
    raw: the raw step JSON from the Dialog Builder
  """
  def __init__(self, step):
    """ Creates a Step from the JSON returned for a particular step """
    self.id = step["id"]
    self.type = step["type"]
    self.raw = step
  
  def __repr__(self):
    return json.dumps(self.raw, indent=2)
  
  def execute(self, context, edge):
    raise NotImplementedError()
