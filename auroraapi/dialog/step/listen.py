from auroraapi.text import Text
from auroraapi.speech import listen_and_transcribe

from auroraapi.dialog.step.step import Step
from auroraapi.dialog.util import parse_optional

class ListenStep(Step):
  """ A Step implementing the Listen functionality
  
  This step listens for audio from the user based on the settings from the
  Dialog Builder and converts it to text. If set in the Dialog Builder, it
  also interprets the text and makes the intent and entities available to
  future steps.

  Attributes:
    step_name: the ID that was set for this step in the Dialog Builder
    model: the model to use for interpret (if applicable)
    interpret: whether or not to interpret the text
    listen_settings: maps the Dialog Builder listen settings to the arguments
      required for the actual `listen_and_transcribe` function. It also sets
      default values if invalid values were specified in the Dialog Builder.
  """

  def __init__(self, step):
    """ Creates the step from the data from the Dialog Builder """
    super().__init__(step)
    data = step["data"]
    self.model = data["model"]
    self.interpret = data["interpret"]
    self.step_name = data["stepName"]
    self.listen_settings = {
      "length": parse_optional(data["length"], float, 0),
      "silence_len": parse_optional(data["silenceLen"], float, 0.5),
    }

  def execute(self, context, edge):
    """ Listens to the user and transcribes and/or interprets their speech
    
    This step first listens until the user says something and then transcribes
    their speech to text. If specified in the Dialog Builder, it will interpret
    the text with the given model. If `intepret` was NOT enabled, then this step
    sets a `Text` object with the transcribed text in the context. If it WAS
    enabled, then it sets an `Interpret` object with the text, intent, and entities.
    Either way, the results of this step are made available in the dialog context
    for future use.

    Args:
      context: the dialog context
      edge: the GraphEdge connected to this step

    Returns:
      the ID of the next node to proceed to
    """
    text = Text()
    while len(text.text) == 0:
      text = listen_and_transcribe(**self.listen_settings)
    res = text.interpret(model=self.model) if self.interpret else text
    context.set_step(self.step_name, res)
    return edge.next()
