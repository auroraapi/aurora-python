import datetime

def parse_date(date_str):
  """ Attempt to parse a string in 'YYYY-MM-DDTHH:MM:SS.sssZ' format
  
  Args:
    date_str: the string to parse
  
  Returns:
    A `datetime` object if parseable, otherwise the original string
  """
  try:
    return datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
  except:
    return date_str

def assert_callable(obj, message="The object is not a function"):
  """ Asserts if the given argument is callable and raises RuntimeError otherwise

  Args:
    obj: The object to check if is callable
    message: The message to raise RuntimeError with
  
  Raises:
    RuntimeError: raised if `obj` is not callable
  """
  if not callable(obj):
    raise RuntimeError(message)

def is_iterable(obj):
  """ Checks if the given argument is iterable

  Args:
    obj: The object to check if is iterable
  
  Returns:
    True if `obj` is iterable, False otherwise
  """
  try:
    _ = iter(obj)
  except TypeError:
    return False
  return True

def parse_optional(val, parser, default=None):
  """ Attempts to parse a value with a given parser

  Uses the given parser to parse the given value. If it is parseable (i.e. parsing
  does not cause an exception) then the parsed value if returned. Otherwise, the
  default value is returned (None by default).

  Args:
    val: the value to parse
    parser: the function to parse with. It should take one argment and return the
      parsed value if parseable and raise an exception otherwise
    default: the value to return if `val` is not parseable by `parser`
  
  Returns:
    The parsed value if parseable, otherwise the default value
  """
  try:
    return parser(val)
  except:
    return default