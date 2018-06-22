import json
from auroraapi.api import get_dialog
from auroraapi.dialog.context import DialogContext
from auroraapi.dialog.graph import Graph
from auroraapi.dialog.util import assert_callable, parse_date

class DialogProperties(object):
	def __init__(self, id, name, desc, appId, dateCreated, dateModified, graph, **kwargs):
		self.id = id
		self.name = name
		self.desc = desc
		self.app_id = appId
		self.date_created = parse_date(dateCreated)
		self.date_modified = parse_date(dateModified)
		self.graph = Graph(graph)

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
		curr = self.dialog.graph.start
		while curr != None and curr in self.dialog.graph.nodes:
			step = self.dialog.graph.nodes[curr]
			edge = self.dialog.graph.edges[curr]
			self.context.set_current_step(step)
			curr = step.execute(self.context, edge)
