from auroraapi.dialog.step import DIALOG_STEP_MAP

class GraphEdge(object):
  def __init__(self, left = "", right = "", prev = ""):
    self.left = left if len(left) > 0 else None
    self.right = right if len(right) > 0 else None
    self.prev = prev if len(prev) > 0 else None
  
  def next(self):
    if self.left != None:
      return self.left
    return self.right
  
  def next_cond(self, cond):
    return self.left if cond else self.right

class Graph(object):
  def __init__(self, graph):
    self.start = graph["start"]
    self.edges = { node_id: GraphEdge(**edges) for (node_id, edges) in graph["edges"].items() }
    self.nodes = { node_id: DIALOG_STEP_MAP[node["type"]](node) for (node_id, node) in graph["nodes"].items() }
