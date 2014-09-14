#!/usr/bin/env python


config = {}

import random   # Random number generator
import os       # Crossplatform OS rutines
import sys      # interpreter tools
import argparse # Tool for argument parsing

legal_chars = "abcdefghijklmnopqrstuvwxyz"+\
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"+"0123456789_"

green="92"
yellow="93"
red="91"
blue="96"
white="0"

def debug(msg, color=white):
  if config["verbose"]:
    print "\033["+color+"m"+msg+"\033[0m"



def random_string(max_length=10, prefix="", legal_chars=legal_chars):
    """
      Create a random string of text.

      Parameters
      ----------
      length : int
          Maxlength of the string (not including the prefix part).
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

    if not legal_chars or not max_length:
      raise ValueError

    length = random.choice(xrange(1,max_length))

    rnd_str = prefix + "".join(random.choice(legal_chars) for _ in xrange(length))

    return rnd_str

def generate_tree():
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
    def make_subfolder(path, width, depth):
      if depth < 0:
        return

      try:
        os.makedirs(path)
        debug("Creating folder %s" % path, green)
      except OSError:
        if not os.path.isdir(path):
          raise

      rndWidth = random.choice(xrange(width))
      for _ in xrange(rndWidth):
        new_folder = os.path.join(path, random_string())
        while(os.path.isdir(new_folder)):
          new_folder = os.path.join(path, random_string())
        make_subfolder(new_folder, width, depth-1)


    make_subfolder(config["target"], config["dirs"], config["rec_depth"])

def populate_tree():
    """
      Generate random files with random content.

      Parameters
      ----------
      target : str
          Path to the file tree where the files are being created.
      max_files : int
          Maximum number of files to be created.
      max_size : int
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

    def create_file(root):
      """
        Function used in os.walk via create_files

        Parameters
        ----------
        root : string
            This is where the files will be written
        max_size : int
          Maximum file size
      """


      name = random_string()
      path = os.path.join(root, name)
      delta_time = config["end"] - config["start"]
      atime = config["start"] + int(random.choice(xrange(delta_time)))
      mtime = config["start"] + int(random.choice(xrange(delta_time)))

      debug("Creating file %s" % path, blue)
      file = open(path, 'w')

      max_size = config["size"] * 1#024
      chars_to_use = legal_chars + "\n"
      content = random_string(config["size"],legal_chars=chars_to_use)
      file.write(content)

      file.close()
      os.utime(path, (atime, mtime))

    def create_files(root):
        """
          Function used in os.walk to manage creation of files

          Parameters
          ----------
          root : string
              Current root
          dirs : list
              Names of the subdirectories in root (excluding '.' and '..')
          files : list
              Names of the non-directory files in dirpath.
        """

        num_files_to_create = random.choice(xrange(config["files"]))
        for _ in xrange(0, num_files_to_create):
          create_file(root)

    for root, _ , _ in os.walk(config["target"]):
        create_files(root)




# If-test to ensure code only executed if ran as stand-alone app.
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="folder to create files in")
    parser.add_argument("dirs", help="maximum number of folders in each folder",
                        type=int)
    parser.add_argument("files", help="maximun number of files in each folder",
                        type=int)
    parser.add_argument("-s", "--size", help="maximum file size",
                        default=600, type=int)
    parser.add_argument("-r", "--rec-depth", help="how deep to recurse",
                        default=2, type=int)
    parser.add_argument("-a", "--start", help="start limit for atime and mtime",
                        default=1388534400, type=int)
    parser.add_argument("-e", "--end", help="end limit for atime and mtime",
                        default=1406851200, type=int)
    parser.add_argument("-z", "--seed", help="seed to random", default=0, type=int)
    parser.add_argument("-v", "--verbose", default=False)

    args = parser.parse_args()
    config["target"] = args.target
    config["dirs"] = args.dirs
    config["files"] = args.files
    config["size"] = args.size
    config["rec_depth"] = args.rec_depth
    config["start"] = args.start
    config["end"] = args.end
    config["seed"] = args.seed
    config["verbose"] = args.verbose

    random.seed(args.seed or None)


    generate_tree()
    populate_tree()
