from auroraapi.dialog.step.step import ContextWrapper, Step

class UDFStep(Step):
  """ A Step implementing the UDF functionality
  
  Attributes:
    udf_id: the ID of the UDF that was set for this step in the Dialog Builder
    branch_enable: if enabled from the Dialog Builder, it will select a branch
      to take based on the truthiness of the value returned by the function
      registered for this UDF
  """
  def __init__(self, step):
    super().__init__(step)
    self.udf_id = step["data"]["stepName"]
    self.branch_enable = step["data"]["branchEnable"]
  
  def execute(self, context, edge):
    """ Executes the UDF and branches based on its return value
    
    This step executes the function that was registered for this UDF. If branching
    is enabled, it chooses a branch based on the boolean value of the function's
    return value. Otherwise it proceeds normally.

    This step also sets the value returned from the registered function in the
    dialog context under the UDF ID. For example, if you named this UDF `udf_1`,
    and your UDF returned a string, you can access it in the Dialog Builder using
    `${udf_1}`. Similarly, if your UDF returned the object `{ "a": 10 }`, you
    can access the value `10` using `${udf_1.a}`.

    Args:
      context: the dialog context
      edge: the GraphEdge connected to this step

    Returns:
      the ID of the next node to proceed to
    """
    if not self.udf_id in context.udfs:
      raise RuntimeError("No UDF registered for step '{}'".format(self.udf_id))
    
    val = context.udfs[self.udf_id](context)
    context.set_step(self.udf_id, val)
    if isinstance(val, (int, bool)) and self.branch_enable:
      return edge.next_cond(val)
    return edge.next()
