from auroraapi.dialog.step.step import Step

class UDFStep(Step):
  def __init__(self, step):
    super().__init__(step)
    self.udf_id = step["data"]["stepName"]
  
  def execute(self, context):
    if not self.udf_id in context.udfs:
      raise RuntimeError("No UDF registered for step '{}'".format(self.udf_id))
    context.udfs[self.udf_id](context)
