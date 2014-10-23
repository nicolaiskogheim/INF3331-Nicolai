import inspect
import subprocess
from PreTeX.cd import cd
import os
import logging
from textwrap import dedent
import sys

compiler = "../../PreTeX/compile.py"
in_file = "testfiles/tex_after.tex"
out_file = "testfiles/tex_after.pdf"

class TestCompile:

    def test_compile_e2e_from_main(self):

        thisScript = os.path.abspath(inspect.stack()[0][1])
        sourcefolder = thisScript.rsplit(os.path.sep,1)[0]
        # sys.exit("stopper her")


        with cd(sourcefolder):
            command, mode = "python", "-v"
            args = [command, compiler, in_file, mode]

            process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result, err = process.communicate()

            assert os.path.exists(out_file)
        expected_err_output = dedent("""\
            INFO:
            ./tex_after.tex:95: Undefined control sequence. l.110 \\bad
            ./pretex_includes/dirA/test.tex:2: LaTeX Error: Can be used only in preamble.
            ./pretex_includes/dirA/test.tex:8: Undefined control sequence. l.13 \\realbad
            ./pretex_includes/dirA/test.tex:30: You can't use `\spacefactor' in vertical mo de.
            ./pretex_includes/dirA/test.tex:30: Missing $ inserted. <inserted text>
            ./pretex_includes/dirA/test.tex:30: Missing $ inserted. <inserted text>
            Output written on tex_after.pdf (2 pages, 108846 bytes).
            Transcript written on tex_after.log.""")
