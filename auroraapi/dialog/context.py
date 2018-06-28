class DialogContext(object):
  """ The current context of the dialog

  DialogContext stores all of the results of the steps in the dialog up until
  a point in time. You can access the data stored in the context to find out
  the current step, previous step, look at data stored by a previous step, and
  store and access your own data. You can access this data both in the Dialog
  Builder as well as programatically through UDFs or the context update handler.

  Attributes:
    steps: a map of step names to data stored by that step. This varies based on the
      step so make sure to look at the documentation for each step to see what gets
      stored and how to access it
    user: a map of key/value pairs for custom data you manually set through UDFs
    udfs: a map of UDF IDs (set from the Dialog Builder) to their handler functions
    previous_step: the specific Step subclass that executed in the previous step
    current_step: the specific Step subclass that is currently executing
    on_update: the function that is called every time the context changes
  """

  def __init__(self, on_update = lambda ctx: None):
    """ Initializes a DialogContext object """
    self.steps = {}
    self.user = {}
    self.udfs = {}
    self.previous_step = None
    self.current_step = None
    self.on_update = on_update
  
  def set_step(self, step, value):
    """ Sets data for a particular step by its name
    
    Args:
      step: the step name
      value: the data resulting from running the step
    """
    self.steps[step] = value
    self.on_update(self)

  def get_step(self, step, default=None):
    """ Gets the data for a particular step by its name
    
    Args:
      step: the step name to retrieve the data for
      default: (optional) the value to return if the step was not found
    
    Returns:
      The data that resulted from executing the given step name
    """
    if not step in self.steps:
      return default
    return self.steps[step]
  
  def set_data(self, key, value):
    """ Sets some custom data for a particular key that can be accessed later
    
    Args:
      key: the key of the data
      value: the value to store for this key
    """
    self.user[key] = value
    self.on_update(self)
  
  def get_data(self, key, default=None):
    """ Gets the custom data that was set for the given key
    
    Args:
      key: the key of the data to retrieve
      default: (optional) the value to return if the key was not found
    
    Returns:
      The data that was set for the given key
    """
    if not key in self.user:
      return default
    return self.user[key]
    
  def set_current_step(self, step):
    """ Sets a particular Step to be the currently executing step """
    self.previous_step = self.current_step
    self.current_step = step
    self.on_update(self)
  
  def get_current_step(self):
    """ Gets the currently executing Step """
    return self.current_step

  def get_previous_step(self):
    """ Gets the last executed Step """
    return self.previous_step