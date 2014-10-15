import argparse
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

        print "Output:"
        print output

        if err:
            print "\n\n"
            print err

def getLnrMap(path):
    mapPattern = re.compile(r'%\[((?:\d+:\d+,)*(?:\d+:\d+))\]')
    with open(path, 'r') as f:
        lastLine = f.read().rstrip().split("\n")[-1]

    match = mapPattern.match(lastLine)
    if not match:
        print "Error: input file not properly formatted."
        print "\tPlease run it through the preprocessor again."
        raise Exception
    else:
        lnrMap = match.group(1).split(",")

        return lnrMap

def getRealLnr(lnr, lnrMap):
    lnr = int(lnr)
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


    args = parser.parse_args()

    source_file = args.source
    inter = args.interactive

    compile_latex(source_file, inter)
