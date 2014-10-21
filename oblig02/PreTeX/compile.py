import argparse
import logging
import line_number_map
import re
import subprocess

def parse_output(unparsed):
    error_lines_pattern = re.compile(r'(..?\/[\w/.]+(?:\n[\w/.]+)?):([\d]+(?:\n[\d]+)?):(.*(?:\n.*)?)')
    parsed = ""

    for line in error_lines_pattern.finditer(unparsed):
        path = line.group(1).replace("\n", "")
        lnr  = line.group(2).replace("\n", "")
        msg  = line.group(3).replace("\n", " ")

        origlnr = line_number_map.getLineNumber(lnr, path)
        parsed += "{0}:{1}:{2}\n".format(path, origlnr, msg)

    # Append last two lines of parsed from pdflatex
    outLines = unparsed.split("\n")
    parsed += "\n".join(outLines[len(outLines) - 3:])

    logging.info("\n"+parsed)


    return parsed

def compile_latex(source_path, interactive=False):
    nonstopmode = not interactive

    args = []
    args.append("pdflatex")
    args.append("-file-line-error")
    if nonstopmode:
        args.append("-interaction=nonstopmode")
    args.append(source_path)

    proc = subprocess.Popen(args,
                            stdout=subprocess.PIPE
                            if nonstopmode
                            else None,
                            stderr=subprocess.PIPE)
    out, err = proc.communicate()

    if err:
        logging.error(err)

    return out


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("source_path",
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


    output = compile_latex(args.source_path, args.interactive)
    if not args.interactive:
        parse_output(output)
