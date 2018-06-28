import re
from functools import reduce
from auroraapi.text import Text
from auroraapi.dialog.step.step import Step
from auroraapi.dialog.util import is_iterable, parse_optional

def resolve_path(context, path):
  step, *components = path.split(".")
  obj = None
  if step == "user":
    obj = context.user
  elif step in context.steps:
    try:
      obj = context.steps[step].context_dict()
    except:
      obj = context.steps[step]
  if not is_iterable(obj):
    return None
  
  while len(components) > 0:
    print(obj, components)
    curr = components.pop(0)
    # Check if current path object is iterable
    if not is_iterable(obj):
      return None
    # Check if the obj is a dict and does not have the given key in it
    if isinstance(obj, dict) and curr not in obj:
      return None
    # Check if the object is a list or string
    if isinstance(obj, (list, str)):
      # If the object is a list, the key must be an integer
      curr = parse_optional(curr, int, None)
      if curr == None:
        return None
      # Check if the object type is a list, the key is an int, but is out of bounds
      if curr >= len(obj):
        return None
    obj = obj[curr]
  return obj


class SpeechStep(Step):
  """ A Step implementing the Speech functionality
  
  Attributes:
    step_name: the ID that was set for this step in the Dialog Builder
    text: the text string to speak (from the Dialog Builder). If it contains
      templates, they aren't evaluated until this step's `execute` function is
      called (lazy evaluation).
  """

  def __init__(self, step):
    """ Creates the step from the data from the Dialog Builder """
    super().__init__(step)
    self.text = step["data"]["text"]
    self.step_name = step["data"]["stepName"]
  
  def get_text(self, context):
    """
    Helper function that evaluates all templates in the text and returns the
    new constructed string
    """
    # upon execution, first find all templates and replace them with
    # the collected value in the conversation
    replacements = []
    for match in re.finditer(r'(\${(.+?)})', self.text):
      val = resolve_path(context, match.group(2))
      # TODO: do something if val not found
      replacements.append((match.group(1), str(val)))
      print(match.group(1), val)
    return reduce(lambda t, r: t.replace(r[0], r[1]), replacements, self.text)

  def execute(self, context, edge):
    """ Converts the text to speech and speaks it
    
    This step first calls the helper function to evaluate the template strings
    in the text based on values stored in the context just as it is about ro run.
    Then it converts that text to speech and plays the resulting audio.

    Args:
      context: the dialog context
      edge: the GraphEdge connected to this step

    Returns:
      the ID of the next node to proceed to
    """
    sp = Text(self.get_text(context)).speech()
    context.set_step(self.step_name, sp)
    sp.audio.play()
    return edge.next()
