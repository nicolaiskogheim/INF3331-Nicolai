import os

def subfolder_count(path, map = {}):
  """
    Count subfolders in path

    Origin
    ------
    http://stackoverflow.com/questions/19747408/how-get-number-of-subfolders-and-folders-using-python-os-walks
  """
  count = 0
  for f in os.listdir(path):
    child = os.path.join(path, f)
    if os.path.isdir(child):
      child_count = subfolder_count(child, map)
      count += child_count + 1 # unless include self
  map[path] = count
  return count


def calculate_tree_size(width, depth):
  """
  Calculate the numbers of folders
  supposed to be created by
  generate_tree

  Parameters
  ----------
  width : int
    Num folders in each folder
  depth : int
    How long to recurse
  """
  sum = 0
  for i in range(1, depth+1):
     sum += width**i
  return sum


import os, os.path

def files_count(path):
  """
    Count files in folder (non-recursively)

    Parameters
    ----------
    path : string
      Path to folder to count files in.
  """
  return len(os.walk(path).next()[2])

def files_count_rec(path):
  """
    Recursicve count of files in path

    Parameters
    ----------
    path : string
      Path to folder where counting starts
  """
  file_count = sum((len(f) for _, _, f in os.walk(path)))
  return file_count
