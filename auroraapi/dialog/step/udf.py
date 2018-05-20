from auroraapi.dialog.step.step import Step

class UDFStep(Step):
  def __init__(self, step):
    super().__init__(step)
    self.udf_id = step["data"]["stepName"]
    self.branch_enable = step["data"]["branchEnable"]
  
  def execute(self, context, edge):
    if not self.udf_id in context.udfs:
      raise RuntimeError("No UDF registered for step '{}'".format(self.udf_id))
    val = context.udfs[self.udf_id](context)
    if isinstance(val, (int, bool)) and self.branch_enable:
      return edge.next_cond(val)
    return edge.next()
