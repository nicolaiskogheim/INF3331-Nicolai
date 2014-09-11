import os
import tempfile
from shutil import rmtree
from test_helpers import subfolder_count, calculate_tree_size
from my_generate_file_tree import generate_tree
import pytest

@pytest.fixture(scope="function")
def root_folder(request):
  empty_folder = tempfile.mkdtemp()
  os.chdir(empty_folder)

  folder_name = "fSEdfjGHFksief325sffsFs93fsSGG"

  def fin():
    rmtree(folder_name)
  request.addfinalizer(fin)

  return folder_name


class TestGenerateTree:

  @pytest.mark.parametrize("width, depth", [
      (1,1), (2,2), (3,3), (9,2), (3,7)
  ])
  def test_creates_folder_tree(self, root_folder, width, depth):
    # Remove/edit this assertion to be able to run high values.
    assert width+depth < 12, "Warning, running high width and depth values is extremely slow."

    generate_tree(root_folder, width, depth)
    msg = "generate_tree: expected {0} folders, but got {1}."

    expected_folder_count = calculate_tree_size(width, depth)
    actual_folder_count = subfolder_count(root_folder)

    assert actual_folder_count == expected_folder_count, msg.format(expected_folder_count, actual_folder_count)
