class Credentials(object):
  """ Wrapper for passing credentials to the backend

  This class contains the credentials to be sent with each API request. Normally
  the credentials are specified by the developer through the globals._config object,
  but that must be converted to an object of this type to be passed to the backend
  because they need to be converted to headers

  Attributes:
    app_id:    the application ID ('X-Application-ID' header)
    app_token: the application token ('X-Application-Token' header)
    device_id: the device ID ('X-Device-ID' header)
  """
  def __init__(self, app_id=None, app_token=None, device_id=None):
    """ Creates an instance of Credentials with the given information """
    self.app_id = app_id
    self.app_token = app_token
    self.device_id = device_id
  
  @property
  def headers(self):
    """
    Returns:
      A dictionary representation of the credentials to be sent to the
      Aurora API service
    """
    return {
      "X-Application-ID": self.app_id,
      "X-Application-Token": self.app_token,
      "X-Device-ID": self.device_id,
    }

  @staticmethod
  def from_config(c):
    """ Creates a Credentials instance from a globals.Config instance """
    return Credentials(c.app_id, c.app_token, c.device_id)

class CallParams(object):
  """ Parameters to be used when constructed a call to the backend

  This class encapsulates the different parameters that can be used to configure
  a backend call and provides sensible defaults

  Attributes:
    method: the HTTP method to use (default "GET")
    path: the path relative to the base URL (default "/")
    credentials: an instance of Credentials providing the authorization
      credentials to be sent along with the request (default Credentials())
    headers: a dictionary of additional headers to be sent (default {})
    query: a dictionary of querystring paramters to be encoded into the URL
      and sent (default {})
    body: any encodeable object or generator function that provides the data
      to be sent in the body of the request. If a generator function is provided
      then the `chunked` attribute should also be set to True (default None)
    chunked: a boolean indicating whether or not to use Transfer-Encoding: chunked
      (default False)
    response_type: one of ['json', 'raw', 'text']. If 'json', then the call expects
      a JSON response and returns a python dictionary containing the JSON data. If 
      'raw', then the call reads the raw data from the stream and returns it. If
      'text', then the call returns the data as-is (default 'json')
  """
  def __init__(self, **kwargs):
    """ Creates a CallParams object from the given keyword arguments

    See the class docstring for the valid keyword arguments, their meanings, and 
    default values. The attributes and parameters correspond exactly.
    """
    self.method = kwargs.get("method", "GET")
    self.path = kwargs.get("path", "/")
    self.credentials = kwargs.get("credentials", Credentials())
    self.headers = kwargs.get("headers", {})
    self.query = kwargs.get("query", {})
    self.body = kwargs.get("body", None)
    self.chunked = kwargs.get("chunked", False)
    self.response_type = kwargs.get("response_type", "json")

class Backend(object):
  """ An abstract class describing how to execute a call on a particular backend

  This class is responsible for executing a call to an arbitary backend given a
  CallParams object. It is designed so that it can be swapped out to provide any
  kind of behavior and contact any kind of backend (mock, staging, production, etc)

  Attributes:
    base_url: The base URL of the service to reach
    timeout: the timeout (in seconds) to use for the request (default 60)

  """
  def __init__(self, base_url, timeout=60):
    """ Creates a Backend object and initializes its attributes """
    self.base_url = base_url
    self.timeout = timeout

  def call(self, params):
    """ Call the backend with the given parameters
    
    This method must be implemented in subclasses to actually handle a call. If
    left unimplemented, it will default to the base class implementation and
    raise an exception.

    Args:
      params: an instance of CallParams, the parameters to use to call the backend
    """
    raise NotImplementedError()
