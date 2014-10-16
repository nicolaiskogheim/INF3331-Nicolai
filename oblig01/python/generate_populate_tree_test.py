import os
import random
import tempfile
from shutil import rmtree
import pytest
from test_helpers import subfolder_count, calculate_tree_size, files_count_rec
from my_generate_file_tree import GFT

generate_tree = GFT.generate_tree
populate_tree = GFT.populate_tree

config = {}
config["files"] = 2
config["dirs"] = 2
config["verbose"] = 0
config["start"] = 1388534400
config["end"] = 1406851200
config["size"] = 20

random.seed(7732);

@pytest.fixture(scope="module")
def instance(request):
  return GFT(config);

@pytest.fixture(scope="function")
def root_folder(request):
  empty_folder = tempfile.mkdtemp()
  os.chdir(empty_folder)

  folder_name = "fSEdfjGHFksief325sffsFs93fsSGG"

  def fin():
    rmtree(empty_folder)
  request.addfinalizer(fin)

  return folder_name

@pytest.fixture(scope="function")
def folder_tree(request, instance, root_folder):
  config["target"] = root_folder
  generate_tree(instance)
  return root_folder;

class TestGenerateTree:

  @pytest.mark.parametrize("width, depth, expected", [
      (1,1,1), (2,2,2), (3,3,5), (9,2,55), (4,6,209)
  ])
  def test_creates_folder_tree(self, instance, root_folder, width, depth, expected):

    instance.config["target"] = root_folder;
    instance.config["dirs"] = width;
    instance.config["rec_depth"] = depth
    generate_tree(instance)
    msg1 = "generate_tree: expected {0} folders, but got {1}."
    msg2 = "generate_tree: expected less than {0} (abs max) folders, but got {1}."

    calculated_max_folder_count = calculate_tree_size(width, depth)
    actual_folder_count = subfolder_count(root_folder)

    print "->", actual_folder_count, "folders"
    assert actual_folder_count == expected, msg1.format(expected, actual_folder_count)
    assert actual_folder_count <= calculated_max_folder_count, msg2.format(calculated_max_folder_count, actual_folder_count)

class TestPopulateTree:

  def test_creates_files(self, instance, folder_tree):
    instance.config["target"] = folder_tree;
    populate_tree(instance)

    actual_files_count = files_count_rec(folder_tree)

    assert int(actual_files_count) > 0, "%d files were created" % actual_files_count
