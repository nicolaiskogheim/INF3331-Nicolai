import argparse
import logging
import line_number_map
import re
import subprocess

def compile_latex(source, interactive=False):
    nonstopmode = not interactive

    args = []
    args.append("pdflatex")
    args.append("-file-line-error")
    if nonstopmode:
      args.append("-interaction=nonstopmode")
    args.append(source)

    proc = subprocess.Popen(args,
                            stdout=subprocess.PIPE
                            if nonstopmode
                            else None,
                            stderr=subprocess.PIPE)
    out, err = proc.communicate()

    if nonstopmode:
        error_lines_pattern = re.compile(r'(..?\/[\w/.]+(?:\n[\w/.]+)?):([\d]+(?:\n[\d]+)?):(.*(?:\n.*)?)')
        output = ""

        for line in error_lines_pattern.finditer(out):
            path = line.group(1).replace("\n", "")
            lnr  = line.group(2).replace("\n", "")
            msg  = line.group(3).replace("\n", "")

            origlnr = line_number_map.getLineNumber(lnr, path)
            output += "{0}:{1}:{2}\n".format(path, origlnr, msg)

        # Append last two lines of output from pdflatex
        outLines = out.split("\n")
        output += "\n".join(outLines[len(outLines) - 3:])

        logging.info("\n"+output)

    if err:
        logging.error(err)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("source",
                        help="Path to file to comiple")
    parser.add_argument("-i", "--interactive",
                        help="runs pdftex with -interaction=nonstopmode",
                        default=False,
                        action="store_true")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose",
                        help="Be verbose about what is going on",
                        default=False,
                        action="store_true")
    group.add_argument("-q", "--quiet",
                        help="Suppress normal output. Returns >0 on error, 0 otherwise.",
                        default=False,
                        action="store_true")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format='%(levelname)s:%(message)s',
                            level=logging.INFO)
    elif args.quiet:
        logging.basicConfig(format='%(levelname)s:%(message)s',
                            level=logging.CRITICAL)
    else:
        logging.basicConfig(format='%(levelname)s:%(message)s',
                            level=logging.INFO)


    compile_latex(args.source, args.interactive)
