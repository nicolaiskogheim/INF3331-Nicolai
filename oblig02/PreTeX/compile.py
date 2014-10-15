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
        error_lines = re.compile(r'(..?\/[\w/.]+(?:\n[\w/.]+)?):([\d]+(?:\n[\d]+)?):(.*(?:\n.*)?)')
        output = ""

        output_lines = out.split("\n")
        lnrMap = getLnrMap(source)

        for line in output_lines:
            match = error_lines.match(line)
            if match:
                path = match.group(1)
                lnr  = match.group(2)
                msg  = match.group(3)
                lnr = getRealLnr(lnr, lnrMap)
                output += path+lnr+msg + "\n"

        # Append last two lines of output from pdflatex
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
