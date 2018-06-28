from auroraapi.api.backend.aurora import AuroraBackend

class Config(object):
  """ Global configuration for the SDK
  
  This class encapsulates the various parameters to be used throughout the SDK,
  including the Aurora credentials and backend to use.

  Attributes:
    app_id:    the Aurora application ID ('X-Application-ID' header)
    app_token: the Aurora application token ('X-Application-Token' header)
    device_id: the ID uniquely identifies this device ('X-Device-ID' header)
    backend:   the backend to use (default is AuroraBackend, the production server)
  """
  
  def __init__(self, app_id=None, app_token=None, device_id=None, backend=AuroraBackend()):
    """ Creates a Config with the given arguments """
    self.app_id = app_id
    self.app_token = app_token
    self.device_id = device_id
    self.backend = backend

# The global configuration used throughout the SDK
_config = Config()