import pytest
from auroraapi.dialog.dialog import Dialog, DialogProperties
from auroraapi.dialog.graph import Graph, GraphEdge
from auroraapi.dialog.step.udf import UDFStep
from auroraapi.dialog.util import parse_date
from auroraapi.globals import _config
from tests.mocks.backend import MockBackend

EMPTY_GRAPH = {
  "dialog": {
    "id": "id",
    "name": "Test",
    "desc": "Test",
    "appId": "appId",
    "runForever": False,
    "dateCreated": "2015-10-14T12:25:32.333Z",
    "dateModified": "2015-10-14T12:25:32.333Z",
    "graph": {
      "start": "",
      "edges": {},
      "nodes": {},
    },
  },
}

TEST_GRAPH = {
  "dialog": {
    **EMPTY_GRAPH["dialog"],
    "graph": {
      "start": "test",
      "edges": {
        "test": {},
      },
      "nodes": {
        "test": {
          "id": "test",
          "type": "udf",
          "data": {
            "stepName": "test_udf",
            "branchEnable": False,
          }
        }
      }
    }
  }
}

class TestDialog(object):
  def setup(self):
    self.orig_backend = _config.backend
    _config.backend = MockBackend()
    _config.backend.set_expected_response(200, EMPTY_GRAPH)
    
  def teardown(self):
    _config.backend = self.orig_backend
  
  def test_create(self):
    d = Dialog("id")

    assert isinstance(d.dialog, DialogProperties)
    assert d.dialog.id == EMPTY_GRAPH["dialog"]["id"]
    assert d.dialog.name == EMPTY_GRAPH["dialog"]["name"]
    assert d.dialog.desc == EMPTY_GRAPH["dialog"]["desc"]
    assert d.dialog.app_id == EMPTY_GRAPH["dialog"]["appId"]
    assert d.dialog.run_forever == EMPTY_GRAPH["dialog"]["runForever"]
    assert d.dialog.date_created == parse_date(EMPTY_GRAPH["dialog"]["dateCreated"])
    assert d.dialog.date_modified == parse_date(EMPTY_GRAPH["dialog"]["dateModified"])

    assert isinstance(d.dialog.graph, Graph)
    assert d.dialog.graph.start == EMPTY_GRAPH["dialog"]["graph"]["start"]
    assert d.dialog.graph.edges == EMPTY_GRAPH["dialog"]["graph"]["edges"]
    assert d.dialog.graph.nodes == EMPTY_GRAPH["dialog"]["graph"]["nodes"]

  def test_create_with_context_fn(self):
    update_fn = lambda ctx: 1
    d = Dialog("id", on_context_update=update_fn)

    assert d.context.on_update == update_fn
  
  def test_create_with_invalid_fn(self):
    with pytest.raises(RuntimeError):
      d = Dialog("id", on_context_update=[])

  def test_set_function(self):
    f = lambda ctx: None
    d = Dialog("id")
    d.set_function("test", f)
    assert d.context.udfs["test"] == f

  def test_set_function_invalid(self):
    d = Dialog("id")
    with pytest.raises(RuntimeError):
      d.set_function("test", [])
  
  def test_run(self):
    _config.backend.set_expected_response(200, TEST_GRAPH)
    d = Dialog("id")
    d.set_function("test_udf", lambda ctx: None)
    d.run()
