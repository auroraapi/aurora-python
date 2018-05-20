from auroraapi.text import Text
from auroraapi.dialog.step.step import Step

class SpeechStep(Step):
  def __init__(self, step):
    super().__init__(step)
    self.text = step["data"]["text"]
    self.step_name = step["data"]["stepName"]

  def execute(self, context, edge):
    sp = Text(self.text).speech()
    context.set_step_data(self.step_name, sp)
    sp.audio.play()
    return edge.next()
