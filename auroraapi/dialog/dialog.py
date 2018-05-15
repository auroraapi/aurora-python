import json
from auroraapi.api import get_dialog
from auroraapi.dialog.step import DIALOG_STEP_MAP
from auroraapi.dialog.context import DialogContext
from auroraapi.dialog.util import assert_callable, parse_date

class DialogProperties(object):
	def __init__(self, id, name, desc, appId, dateCreated, dateModified, steps, **kwargs):
		self.id = id
		self.name = name
		self.desc = desc
		self.app_id = appId
		self.date_created = parse_date(dateCreated)
		self.date_modified = parse_date(dateModified)
		self.steps = [DIALOG_STEP_MAP[step["type"]](step) for step in steps]

class Dialog(object):
	def __init__(self, id, on_context_update=None):
		self.dialog = DialogProperties(**get_dialog(id)["dialog"])
		self.context = DialogContext()
		if on_context_update != None:
			assert_callable(on_context_update, "The 'on_context_update' parameter must be a function that accepts one argument")
			self.context.on_update = on_context_update

	def set_function(self, id, func):
		assert_callable(func, "Function argument to 'set_function' for ID '{}' must be callable and accept one argument".format(id))
		self.context.udfs[id] = func

	def run(self):
		for step in self.dialog.steps:
			self.context.set_current_step(step)
			step.execute(self.context)
