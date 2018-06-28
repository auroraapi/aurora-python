from auroraapi.api import get_dialog
from auroraapi.dialog.context import DialogContext
from auroraapi.dialog.graph import Graph
from auroraapi.dialog.util import assert_callable, parse_date
from auroraapi.globals import _config

class DialogProperties(object):
  """ The properties of a Dialog object as returned by the Aurora API

  Attributes:
    id: the dialog ID
    name: the dialog name
    desc: the dialog description
    app_id: the app ID that this dialog belongs to
    run_forever: whether or not to re-run the dialog after completion or exit
    date_created: the date that the dialog was created
    date_modified: the date that the dialog was last modified
    graph: the deserialized graph of the dialog
  """
  def __init__(self, **kwargs):
    """ Initializes from the fields returned by the API """
    self.id = kwargs.get("id")
    self.name = kwargs.get("name")
    self.desc = kwargs.get("desc")
    self.app_id = kwargs.get("appId")
    self.run_forever = kwargs.get("runForever")
    self.date_created = parse_date(kwargs.get("dateCreated"))
    self.date_modified = parse_date(kwargs.get("dateModified"))
    self.graph = Graph(kwargs.get("graph"))

class Dialog(object):
  """ A Dialog built with the Dialog Builder

  This class represents the Dialog built with the Dialog Builder. When you create
  an object of this class, the ID you specify automatically fetches it from the
  server. Then all you have to do is run it. See the Dialog Builder documentation
  for more details.

  Attributes:
    dialog: the dialog information downloaded from the Aurora service
    context: information stored during the execution of the dialog
  """

  def __init__(self, id, on_context_update=None):
    """ Creates the Dialog Builder

    Args:
      id: the ID of the dialog to download and instantiated
      on_context_update: A function that takes one argument (the dialog context)
        and is called every time the current step changes or some data in the
        context is updated
    """
    self.dialog = DialogProperties(**get_dialog(_config, id)["dialog"])
    self.context = DialogContext()
    # Check if `on_context_update` is specified and a valid function
    if on_context_update != None:
      assert_callable(on_context_update, "The 'on_context_update' parameter must be a function that accepts one argument")
      self.context.on_update = on_context_update

  def set_function(self, id, func):
    """ Assigns a function to a UDF

    If you have any UDFs in the dialog builder, you need to assign a function that gets
    called when it's the UDF's turn to execute.

    Args:
      id: the UDF ID to assign this function to. This should be the name you give
        it in the Dialog Builder
      func: the function to run when this UDF runs. It should accept one argument
        (the dialog context). If the UDF needs to branch, it should return True to
        take the "checkmark"-icon branch and False to take the "cross"-icon branch.
        For a non-branching UDF, the value you return gets stored in the dialog
        context as '<STEPNAME>.value'
    """
    assert_callable(func, "Function argument to 'set_function' for ID '{}' must be callable and accept one argument".format(id))
    self.context.udfs[id] = func

  def run(self):
    """ Runs the dialog """
    first_run = True
    while first_run or self.dialog.run_forever:
      curr = self.dialog.graph.start
      while curr != None and curr in self.dialog.graph.nodes:
        step = self.dialog.graph.nodes[curr]
        edge = self.dialog.graph.edges[curr]
        self.context.set_current_step(step)
        curr = step.execute(self.context, edge)
      first_run = False
