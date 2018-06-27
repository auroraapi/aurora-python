import datetime, pytest
from auroraapi.dialog.util import *

class TestParseDate(object):
  def test_valid_date(self):
    d = parse_date("2015-10-14T12:25:32.333Z")
    assert isinstance(d, datetime.datetime)
  
  def test_invalid_date(self):
    d = parse_date("2015-10-14 12:25:32.333Z")
    assert isinstance(d, str)
    assert d == "2015-10-14 12:25:32.333Z"

class TestAssertCallable(object):
  def test_callable(self):
    assert assert_callable(lambda: None) != ""
  
  def test_not_callable(self):
    with pytest.raises(RuntimeError) as e:
      assert_callable([])

class TestIsIterable(object):
  def test_iterable(self):
    iters = [list(), set(), dict(), str()]
    for i in iters:
      assert is_iterable(i)
  
  def test_not_iterable(self):
    niters = [lambda: None]
    for i in niters:
      assert not is_iterable(i)

class TestParseOptional(object):
  def test_valid(self):
    parse = [
      ("34", int, 34),
      (34, str, "34"),
      ((1,2,3), list, [1,2,3]),
    ]
    for i in parse:
      assert parse_optional(i[0], i[1]) == i[2]
  
  def test_invalid_default(self):
    parse = [
      ("abc", int, None),
      (123, list, None),
    ]
    for i in parse:
      assert parse_optional(i[0], i[1]) == i[2]

  def test_invalid_custom(self):
    parse = [
      ("abc", int, 0),
      (123, list, [1,2,3]),
    ]
    for i in parse:
      assert parse_optional(i[0], i[1], default=i[2]) == i[2]
