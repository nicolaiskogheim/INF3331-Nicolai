import re
import random
import pytest
from my_generate_file_tree import GFT

random_string = GFT.random_string

legal_chars = "abcdefghijklmnopqrstuvwxyz"+\
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"+"0123456789_"

config = {}
config["files"] = 2
config["dirs"] = 2
config["verbose"] = 0
config["start"] = 1388534400
config["end"] = 1406851200
config["size"] = 20

@pytest.fixture(scope="module")
def instance(request):
  return GFT(config)



def test_random_string_returns_string(instance):
  alphanumeric = re.compile(r'^[a-zA-Z0-9_]+$')
  value = instance.random_string()
  is_alphanumeric = alphanumeric.match(value)
  assert is_alphanumeric != None, "random_string should return a string"

def test_random_string_param_length(instance):
  assert len(instance.random_string(5)) <= 5, 'random_string(5) should return string of length beetween 5 and 1 inclusive'
  assert len(instance.random_string(10)) <= 10, 'random_string(10) should return string of length between 10 and 1 inclusive'

def test_random_string_param_prefix(instance):
  prefix = "pre"
  result = instance.random_string(5, prefix)

  assert "pre" in result, "return value should start with prefix"

  prefix_plus_alphanumeric_pattern = re.compile(r'^'+prefix+'[a-zA-Z0-9_]+$')
  is_prefixed_alphanumeric = prefix_plus_alphanumeric_pattern.match(result)

  assert is_prefixed_alphanumeric != None, "random_string should prefix the returned string"


def test_random_string_is_somewhat_random(instance):
  result1 = instance.random_string()
  result2 = instance.random_string()

  assert result1 != result2, "random_string should generate random output"

def test_random_string_raises_exception_on_empty_legal_chars(instance):
  with pytest.raises(ValueError):
    instance.random_string(legal_chars='')

def test_random_string_raises_exception_on_null_length(instance):
  with pytest.raises(ValueError):
    instance.random_string(max_length=0)
