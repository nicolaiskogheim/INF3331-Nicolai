#!/usr/bin/env python

verbose=0

import random   # Random number generator
import os       # Crossplatform OS rutines
import sys      # interpreter tools


legal_chars = "abcdefghijklmnopqrstuvwxyz"+\
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"+"0123456789_"


def debug(msg):
  if verbose:
    print msg

def make_subfolder(root, width, depth):
  if depth < 0:
    return

  try:
    debug("Creating folder %s" % root)
    debug("Entering folder %s" % root)
    os.makedirs(root)
  except OSError:
    if not os.path.isdir(root):
      raise

  for _ in range(0, width):
    new_folder = os.path.join(root, random_string())
    make_subfolder(new_folder, width, depth-1)

  debug("Exiting folder %s" % root)


def random_string(length=6, prefix="", legal_chars=legal_chars):
    """
    Create a random string of text.

    Parameters
    ----------
    length : int
        Length of the string (not including the prefix part).
    prefix : string
        Prefix the string with some text.
    legal_chars : string
        A string of charracter that are allowed to be used in the
        output.

    Returns
    -------
    rnd_str : str
        A string of random charracters.
    """
    # Insert user code here
    if not legal_chars or not length:
      raise ValueError

    generated_string = "".join(random.choice(legal_chars) for _ in range(length))
    random_string = prefix + generated_string
    return random_string

def generate_tree(target, dirs=3, rec_depth=2):
    """
    Genereate a random folder structure with random names.

    Parameters
    ----------
    target : str
        Path to the root where folders are to be created.
    dirs : int
        Maximum number of directories to be created per directory.
    rec_depth : int
        Maximum directory depth.
    """


    make_subfolder(target, dirs, rec_depth)

def populate_tree(target, files=5, size=800, start_time=1388534400,
        end_time=1406851201000, verbose=False):
    """
Generate random files with random content.

Parameters
----------
target : str
    Path to the file tree where the files are being created.
files : int
    Maximum number of directories to be created.
size : int
    Maximum size in kilobyte for each file.
start_time : int
    Lower bound for access time (atime) and modified time (mtime)
    allowed in each file.
    Denoted in Unix time format.
end_time : int
    Same as start_time, but for upper bound.
verbose : bool
    Be loud about what to do.
    """

    def walk_function(arg, dirname, fnames):
        """
Function used in os.path.walk

Following the logic of Python scoping, this is a local function,
only visible inside of populate_tree.
This function should be passed to os.path.walk.

Parameters
----------
arg : obj
    Arbitrary argument specified at initialization.
dirname : str
    Name of a directory in file tree (changes with each call.
fnames : list
    List of filenames in file tree.
        """
        # Fill in code for walk function

    os.path.walk(target, walk_function, None)




# If-test to ensure code only executed if ran as stand-alone app.
if __name__ == "__main__":

    l = len(sys.argv)

    if l < 4:
        print "Not enough arguments included."
        print "usage: %s target dirs files " % sys.argv[0] +\
            "[size rec_depth start end seed verbose]"
        sys.exit(0)

    target = sys.argv[1]
    dirs = int(sys.argv[2])
    files = int(sys.argv[3])

    # And-or trick to use argv only if argv is long enough.
    size = 1000 if l<5 else int(sys.argv[4])
    rec_depth = 2 if l<6 else int(sys.argv[5])
    start = 1388534400 if l<7 else int(sys.argv[6])
    end = 1406851200 if l<8 else int(sys.argv[7])
    seed = "0" if l<9 else sys.argv[8]
    verbose = int("0") if l<10 else int(sys.argv[9])

    # Fix the random seed (if not None):
    random.seed(int(seed) or None)

    generate_tree(target, dirs, rec_depth)
    populate_tree(target, files, size, start, end)
