import argparse
import logging
import re
import subprocess

def compile_latex(source, inter=False):

    args = []
    args.append("pdflatex")
    args.append("-file-line-error")
    if inter:
      args.append("-interaction=nonstopmode")
    args.append(source)

    proc = subprocess.Popen(args, stdout=subprocess.PIPE if inter else None, stderr=subprocess.PIPE)
    out, err = proc.communicate()

    if inter:
        error_lines_pattern = re.compile(r'(..?\/[\w/.]+(?:\n[\w/.]+)?):([\d]+(?:\n[\d]+)?):(.*(?:\n.*)?)')
        output = ""

        lnrs = {} #Map with lnr-maps
        for line in error_lines_pattern.finditer(out):
            path = line.group(1).replace("\n", "")
            lnr  = line.group(2).replace("\n", "")
            msg  = line.group(3).replace("\n", "")

            if not path in lnrs:
                lnrs[path] = getLnrMap(path)

            lnr = getRealLnr(lnr, lnrs[path])
            output += "{0}:{1}:{2}\n".format(path, lnr, msg)

        # Append last two lines of output from pdflatex
        out = out.split("\n")
        output += "\n".join(out[len(out) - 3:])

        logging.info("\n"+output)

        if err:
            logging.error(err)

def getLnrMap(path):
    mapPattern = re.compile(r'%\[((?:\d+:\d+,)*(?:\d+:\d+))\]')
    with open(path, 'r') as f:
        lastLine = f.read().rstrip().split("\n")[-1]

    match = mapPattern.match(lastLine)
    if not match:
        logging.error("Input file not properly formatted.")
        logging.error("\tPlease run it through the preprocessor again.")
        logging.error("This means that the linenumbers will point to")
        logging.error("the preprocessed file rather than the unprocessed one.")
        lnrMap = None
    else:
        lnrMap = match.group(1).split(",")

        return lnrMap

def getRealLnr(lnr, lnrMap):
    lnr = int(lnr)

    if not lnrMap:
      return lnr

    lastLnr = 0
    for m in lnrMap:
      orig, new = m.split(":")
      if lnr < int(new):
        return lastLnr
      else:
        lastLnr = orig


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="Path to file to comiple")
    parser.add_argument("-i", "--interactive", help="turn on interaction",
                        default=False, action="store_true")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true", default=False,
                        help="Be verbose about what is going on")
    group.add_argument("-q", "--quiet", action="store_true", default=False,
                        help="Suppress normal output. Returns >0 on error, 0 otherwise.")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    elif args.quiet:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.CRITICAL)
    else:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    source_file = args.source
    inter = args.interactive

    compile_latex(source_file, inter)
