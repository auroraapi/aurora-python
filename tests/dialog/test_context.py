from auroraapi.dialog.context import DialogContext

def on_update_creater():
  d = { "called": False }
  def on_update(ctx):
    d["called"] = True
  d["fn"] = on_update
  return d

class TestDialogContext(object):
  def test_create(self):
    d = DialogContext()
    assert d.on_update(0) == None

    d = DialogContext(lambda x: x)
    assert d.on_update(0) == 0
  
  def test_set_step(self):
    f = on_update_creater()
    d = DialogContext(on_update=f["fn"])
    d.set_step("test_id", 123)
    assert d.steps["test_id"] == 123
    assert f["called"]

  def test_get_step(self):
    d = DialogContext()
    d.set_step("test_id", 123)
    assert d.get_step("test_id") == 123

  def test_get_step_nonexistant(self):
    d = DialogContext()
    assert d.get_step("test_id") == None
    assert d.get_step("test_id", default=0) == 0
  
  def test_set_data(self):
    f = on_update_creater()
    d = DialogContext(on_update=f["fn"])
    d.set_data("test_id", 123)
    assert d.user["test_id"] == 123
    assert f["called"]

  def test_get_data(self):
    d = DialogContext()
    d.set_data("test_id", 123)
    assert d.get_data("test_id") == 123

  def test_get_data_nonexistant(self):
    d = DialogContext()
    assert d.get_data("test_id") == None
    assert d.get_data("test_id", default=0) == 0
  
  def test_set_current_step(self):
    d = DialogContext()
    d.set_current_step("test1")
    assert d.get_current_step() == "test1"
    assert d.get_previous_step() == None

    d.set_current_step("test2")
    assert d.get_current_step() == "test2"
    assert d.get_previous_step() == "test1"
