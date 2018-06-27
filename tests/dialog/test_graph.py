import pytest
from auroraapi.dialog.graph import Graph, GraphEdge
from auroraapi.dialog.step.udf import UDFStep

class TestGraphEdge(object):
  def test_create(self):
    g = GraphEdge("a","b","c")
    assert g.left == "a"
    assert g.right == "b"
    assert g.prev == "c"

  def test_next_with_only_left(self):
    g = GraphEdge("a")
    assert g.next() == "a"
  
  def test_next_with_only_right(self):
    g = GraphEdge("", "b")
    assert g.next() == "b"
  
  def test_next_with_both(self):
    g = GraphEdge("a", "b")
    assert g.next() == "a"
  
  def test_next_cond_with_only_left(self):
    g = GraphEdge("a")
    assert g.next_cond(True) == "a"
    assert g.next_cond(False) == None
  
  def test_next_cond_with_only_right(self):
    g = GraphEdge("", "b")
    assert g.next_cond(True) == None
    assert g.next_cond(False) == "b"
  
  def test_next_cond_with_both(self):
    g = GraphEdge("a", "b")
    assert g.next_cond(True) == "a"
    assert g.next_cond(False) == "b"

class TestGraph(object):
  def test_create_empty(self):
    g = Graph({
      "start": "",
      "edges": {},
      "nodes": {},
    })

    assert g.start == ""
    assert g.edges == {}
    assert g.nodes == {}
  
  def test_create_valid(self):
    g = Graph({
      "start": "a",
      "edges": {
        "a": {
          "left": "b",
          "right": "c",
          "prev": "",
        },
        "b": {
          "left": "d",
          "right": "",
          "prev": "a",
        },
        "c": {
          "left": "",
          "right": "",
          "prev": "a",
        },
        "d": {
          "left": "",
          "right": "",
          "prev": "b",
        },
      },
      "nodes": {
        "a": {
          "id": "a",
          "type": "udf",
          "data": {
            "stepName": "udf_a",
            "branchEnable": True,
          },
        },
        "b": {
          "id": "b",
          "type": "udf",
          "data": {
            "stepName": "udf_b",
            "branchEnable": False
          }
        },
        "c": {
          "id": "c",
          "type": "udf",
          "data": {
            "stepName": "udf_c",
            "branchEnable": False
          }
        },
        "d": {
          "id": "d",
          "type": "udf",
          "data": {
            "stepName": "udf_d",
            "branchEnable": False
          }
        },
      }
    })

    assert g.start == "a"
    assert len(g.edges) == 4
    assert len(g.nodes) == 4
    assert all(isinstance(e, GraphEdge) for e in g.edges.values())
    assert all(isinstance(n, UDFStep) for n in g.nodes.values())
  
  def test_create_invalid(self):
    with pytest.raises(KeyError):
      g = Graph({
        "start": "a",
        "edges": {
          "a": {
            "left": "",
            "right": "",
            "prev": "",
          },
        },
        "nodes": {
          "a": {
            "id": "a",
            "type": "invalid",
          },
        },
      })