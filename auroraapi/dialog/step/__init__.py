from auroraapi.dialog.step.speech import SpeechStep
from auroraapi.dialog.step.listen import ListenStep
from auroraapi.dialog.step.udf import UDFStep

DIALOG_STEP_MAP = {
  "speech": SpeechStep,
  "listen": ListenStep,
  "udf":    UDFStep,
}
