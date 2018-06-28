from auroraapi.dialog.step import DIALOG_STEP_MAP

class GraphEdge(object):
  """ An edge in the Dialog graph
  
  This class keeps track of the left and right node IDs for each node, as well
  as the previous node ID.

  Attributes:
    left: the default next node ID (or the "checkmark"-icon branch if applicable)
    right: the "cross"-icon branch node ID (if applicable)
    prev: the node ID of the previous node
  """
  def __init__(self, left = "", right = "", prev = ""):
    """ Initializes a GraphEdge with the given left, right, prev node IDs """
    self.left = left if len(left) > 0 else None
    self.right = right if len(right) > 0 else None
    self.prev = prev if len(prev) > 0 else None
  
  def next(self):
    """ Gets the next node

    Returns:
      By default, the next node will be the `left` one. If for some reason there
      isn't a left node, it picks the `right` node. If neither node exists (no
      more nodes left in the dialog), it returns None.
    """
    if self.left != None:
      return self.left
    return self.right
  
  def next_cond(self, cond):
    """ Gets a node based on a condition

    Args:
      cond: whether a particular condition is True or False

    Returns:
      If the condition was True, it returns the `left` node ID (the one
      corresponding to the "checkmark"-icon branch. Otherwise it returns
      the one corresponding to the "cross"-icon branch.
    """
    return self.left if cond else self.right

class Graph(object):
  """ A deserialized representation of the Dialog graph

  This class takes the serialized JSON representation of the graph built with
  the Dialog Builder and deserializes the nodes and edges into python objects
  with corresponding properties and methods to execute them.

  Attributes:
    start: the ID of the node that starts the dialog
    edges: a mapping of node IDs to `GraphEdge` objects. Each `GraphEdge` object
      keeps track of the node IDs that are connected to this one.
    nodes: a mapping of node IDs to a Step that implements the behavior required
      for that node type.
  """
  def __init__(self, graph):
    """ Initializes a Graph from the graph returned by the Dialog API """
    self.start = graph["start"]
    self.edges = { node_id: GraphEdge(**edges) for (node_id, edges) in graph["edges"].items() }
    self.nodes = { node_id: DIALOG_STEP_MAP[node["type"]](node) for (node_id, node) in graph["nodes"].items() }
