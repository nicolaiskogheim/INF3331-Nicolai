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
        error_lines = re.compile(r'^..?\/[\w/.]+:[\d]+:.*$')
        output = ""

        output_lines = out.split("\n")

        for line in output_lines:
            if error_lines.match(line):
                output += line + "\n"

        # Append last two lines of output from pdflatex
        output += output_lines[len(output_lines) - 3] + "\n"
        output += output_lines[len(output_lines) - 2]

        print "Output:"
        print output

    # print "OUT:"
    # print out

    # print "ERR:"
    # print err


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="Path to file to comiple")
    parser.add_argument("-i", "--interactive", help="turn on interaction",
                        default=False, action="store_true")


    args = parser.parse_args()

    source_file = args.source
    inter = args.interactive

    compile_latex(source_file, inter)
