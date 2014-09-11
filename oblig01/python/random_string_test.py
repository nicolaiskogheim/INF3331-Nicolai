import re
from my_generate_file_tree import random_string
import random
import pytest

legal_chars = "abcdefghijklmnopqrstuvwxyz"+\
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"+"0123456789_"


def test_random_string_returns_string():
  alphanumeric = re.compile(r'^[a-zA-Z0-9_]+$')
  value = random_string()
  is_alphanumeric = alphanumeric.match(value)
  assert is_alphanumeric != None, "random_string should return a string"

def test_random_string_param_length():
  assert len(random_string(5)) == 5, 'random_string(5) should return string of length 5'
  assert len(random_string(10)) == 10, 'random_string(10) should return string of length 10'

def test_random_string_param_prefix():
  prefix = "pre"
  result = random_string(5, prefix)

  assert len(result) == 8, "length of return value from random_string should be length + len(prefix)"

  prefix_plus_alphanumeric_pattern = re.compile(r'^'+prefix+'[a-zA-Z0-9_]+$')
  is_prefixed_alphanumeric = prefix_plus_alphanumeric_pattern.match(result)

  assert is_prefixed_alphanumeric != None, "random_string should prefix the returned string"


def test_random_string_is_random():
  result1 = random_string()
  result2 = random_string()

  assert result1 != result2, "random_string should generate random output"

def test_random_string_raises_exception_on_empty_legal_chars():
  with pytest.raises(ValueError):
    random_string(legal_chars='')

def test_random_string_raises_exception_on_null_length():
  with pytest.raises(ValueError):
    random_string(length=0)
