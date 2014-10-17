import pytest
import subprocess
from PreTeX.compile import compile_latex, parse_output
from PreTeX import line_number_map

dummyerrors="""
[1

{/usr/local/texlive/2013/texmf-var/fonts/map/pdftex/updmap/pdftex.map}]
\openout2 = `./preprocessed_tex_files_to_include/test_file_inclusion/errorfolde
r/tex_error.aux'.


(./test/errorfolder/tex_error.
tex
./test/errorfolder/tex_error.t
ex:5: Undefined control sequence.
l.5 Invalid command: \\asdf

The control sequence at the end of the top line
of your error message was never \def'ed. If you have

% last two lines
% will also be appended
"""

class TestCompile:
    def test_compile_runs_pdftex(self, monkeypatch):
        class monkeycommunicate:
            def communicate(self):
              return "called", None
        def monkeysub(args, stdout=None, stderr=None):
            if not "pdflatex" in args:
                fail(msg="compile should call pdflatex", pytrace=True)
            elif not "-file-line-error" in args:
                fail(msg="compile should call pdflatex with -file-line-error option",
                     pytrace=True)
            elif not "-interaction=nonstopmode" in args:
                fail(msg="compile should call pdflatex with -interaction=nonstopmode option",
                     pytrace=True)
            global dummytex
            return monkeycommunicate()

        monkeypatch.setattr(subprocess, 'Popen', monkeysub)


        result = compile_latex("test", interactive=False)

        assert result == "called"

    def test_compile_runs_pdftex(self, monkeypatch):
        class monkeycommunicate:
            def communicate(self):
              return "called", None
        def monkeysub(args, stdout=None, stderr=None):
            if not "pdflatex" in args:
                fail(msg="compile should call pdflatex", pytrace=True)
            elif not "-file-line-error" in args:
                fail(msg="compile should call pdflatex with -file-line-error option",
                     pytrace=True)
            elif not "-interaction=nonstopmode" in args:
                fail(msg="compile should call pdflatex with -interaction=nonstopmode option",
                     pytrace=True)
            global dummytex
            return monkeycommunicate()

        monkeypatch.setattr(subprocess, 'Popen', monkeysub)


        result = compile_latex("test", interactive=False)

        assert result == "called"

    def test_parse_output(self, monkeypatch):
        def monkeyNumbers(lnr,*args):
            return lnr
        monkeypatch.setattr(line_number_map, "getLineNumber", monkeyNumbers)
        result = parse_output(dummyerrors)

        expected = """./test/errorfolder/tex_error.tex:5: Undefined control sequence. l.5 Invalid command: \\asdf\n% last two lines\n% will also be appended\n"""

        assert result == expected
