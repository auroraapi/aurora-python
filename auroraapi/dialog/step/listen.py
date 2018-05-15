from auroraapi.text import Text
from auroraapi.speech import listen_and_transcribe

from auroraapi.dialog.step.step import Step
from auroraapi.dialog.util import parse_optional

class ListenStep(Step):
  def __init__(self, step):
    super().__init__(step)
    data = step["data"]
    self.model = data["model"]
    self.interpret = data["interpret"]
    self.step_name = data["stepName"]
    self.listen_settings = {
      "length": parse_optional(data["length"], float, 0),
      "silence_len": parse_optional(data["silenceLen"], float, 0.5),
    }
    print(self.listen_settings)

  def execute(self, context):
    text = Text()
    while len(text.text) == 0:
      print(**self.listen_settings)
      text = listen_and_transcribe(**self.listen_settings)
    res = text.interpret(model=self.model) if self.interpret else text
    context.set_step_data(self.step_name, res)