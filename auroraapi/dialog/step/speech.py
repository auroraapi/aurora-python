import re, functools
from auroraapi.text import Text
from auroraapi.dialog.step.step import Step
from auroraapi.dialog.util import is_iterable

def resolve_path(context, path):
  step, *components = path.split(".")
  obj = None
  if step == "user":
    obj = context.user
  elif step in context.step:
    obj = context.step[step].context_dict()
  if not is_iterable(obj):
    return None
  
  while len(components) > 0:
    curr = components.pop(0)
    # TODO: handle arrays
    if not is_iterable(obj) or curr not in obj:
      return None
    obj = obj[curr]
  return obj


class SpeechStep(Step):
  def __init__(self, step):
    super().__init__(step)
    self.text = step["data"]["text"]
    self.step_name = step["data"]["stepName"]

  def execute(self, context, edge):
    # upon execution, first find all templates and replace them with
    # the collected value in the conversation
    replacements = []
    for match in re.finditer(r'(\${(.+?)})', self.text):
      val = resolve_path(context, match.group(2))
      # TODO: do something on data not found
      replacements.append({ "original": match.group(1), "replacement": val })

    text = functools.reduce(lambda t, r: t.replace(r["original"], r["replacement"]), replacements, self.text)
    sp = Text(text).speech()
    context.set_step_data(self.step_name, sp)
    sp.audio.play()
    return edge.next()
