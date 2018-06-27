import pytest
from auroraapi.dialog.context import DialogContext
from auroraapi.dialog.graph import GraphEdge
from auroraapi.dialog.step.udf import UDFResponse, UDFStep

UDF = {
  "id": "udf_id",
  "type": "udf",
  "data": {
    "stepName": "udf_name",
    "branchEnable": False,
  },
}

class TestUDFResponse(object):
  def test_create(self):
    r = UDFResponse("value")
    assert r.value == "value"
  
  def test_context_dict(self):
    r = UDFResponse("value")
    d = r.context_dict()
    assert len(d) == 1
    assert d["value"] == r.value

class TestUDFStep(object):
  def test_create(self):
    u = UDFStep(UDF)
    assert u.id == UDF["id"]
    assert u.type == UDF["type"]
    assert u.udf_id == UDF["data"]["stepName"]
    assert u.branch_enable == UDF["data"]["branchEnable"]
  
  def test_execute_no_function_registered(self):
    c = DialogContext()
    u = UDFStep(UDF)
    with pytest.raises(RuntimeError):
      u.execute(c, GraphEdge())
  
  def test_execute_branch_disabled(self):
    e = GraphEdge("left", "right", "prev")
    c = DialogContext()
    c.udfs[UDF["data"]["stepName"]] = lambda ctx: False
    u = UDFStep(UDF)
    assert u.execute(c, e) == e.left
    assert c.get_step(UDF["data"]["stepName"]).value == False
  
  def test_execute_branch_enabled_left(self):
    e = GraphEdge("left", "right", "prev")
    c = DialogContext()
    c.udfs[UDF["data"]["stepName"]] = lambda ctx: True
    UDF["data"]["branchEnable"] = True
    u = UDFStep(UDF)
    assert u.execute(c, e) == e.left
    assert c.get_step(UDF["data"]["stepName"]).value == True
  
  def test_execute_branch_enabled_left(self):
    e = GraphEdge("left", "right", "prev")
    c = DialogContext()
    c.udfs[UDF["data"]["stepName"]] = lambda ctx: False
    UDF["data"]["branchEnable"] = True
    u = UDFStep(UDF)
    assert u.execute(c, e) == e.right
    assert c.get_step(UDF["data"]["stepName"]).value == False
