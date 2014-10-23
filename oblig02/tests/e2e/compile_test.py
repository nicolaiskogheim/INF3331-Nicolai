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
