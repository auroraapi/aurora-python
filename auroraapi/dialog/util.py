import datetime

def parse_date(date_str):
  try:
    return datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
  except:
    return date_str

def assert_callable(obj, message="The object is not a function"):
  if not callable(obj):
    raise RuntimeError(message)

def is_iterable(obj):
  try:
    _ = iter(obj)
  except TypeError:
    return False
  return True

def parse_optional(val, parser, default=None):
  try:
    return parser(val)
  except:
    return default