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
    obj = context.steps[step].context_dict()
  if not is_iterable(obj):
    return None
  
  while len(components) > 0:
    curr = components.pop(0)
    # Check if current path object is iterable
    if not is_iterable(obj):
      return None
    # Check if the obj is a dict and does not have the given key in it
    if isinstance(obj, dict) and curr not in obj:
      return None
    # Check if the object is a list and if the key is an integer
    if isinstance(obj, list) and parse_optional(curr, int, None) != None:
      curr = int(curr)
      # Check if the object type is a list, the key is an int, but is out of bounds
      if curr >= len(obj):
        return None
    obj = obj[curr]
  return obj


class SpeechStep(Step):
  def __init__(self, step):
    super().__init__(step)
    self.text = step["data"]["text"]
    self.step_name = step["data"]["stepName"]
  
  def get_text(self):
    # upon execution, first find all templates and replace them with
    # the collected value in the conversation
    replacements = []
    for match in re.finditer(r'(\${(.+?)})', self.text):
      val = resolve_path(context, match.group(2))
      # TODO: do something if val not found
      replacements.append((match.group(1), val))
    return reduce(lambda t, r: t.replace(r[0], r[1]), replacements, self.text)

  def execute(self, context, edge):
    sp = Text(self.get_text()).speech()
    context.set_step(self.step_name, sp)
    sp.audio.play()
    return edge.next()
