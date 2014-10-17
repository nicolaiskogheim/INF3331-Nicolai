from PreTeX.latex import *
from textwrap import dedent

#  Note:
#  Due to something I haven't figured out yet,
#+ there is being sent a 'self' to these wrappers
#+ from the scanner via the handlers.
#  That is why we am passing in arbitrary
#+ values as first argument.

class TestLatex:
    def test_verbatim_wrapper(self):
        result = verbatim('foo', "to be wrapped")

        expected = dedent("""\
            \\begin{Verbatim}
            to be wrapped
            \\end{Verbatim}\n""")

        assert result == expected

    def test_terminal_wrapper(self):
        result = terminal('bar', "to be wrapped")

        expected = dedent("""\
            \\begin{Verbatim}[numbers=none,frame=lines,label=\\fbox{{\\tiny Terminal}},fontsize=\\fontsize{9pt}{9pt},
            labelposition=topline,framesep=2.5mm,framerule=0.7pt]
            to be wrapped
            \\end{Verbatim}
            \\noindent\n""")

        assert result == expected

    def test_fancyverb_wrapper(self):
        result = fancyverb('baz', "to be wrapped")

        expected = dedent("""\
            \\begin{shadedquoteBlueBar}
            \\fontsize{9pt}{9pt}
            \\begin{Verbatim}
            to be wrapped
            \\end{Verbatim}
            \\end{shadedquoteBlueBar}
            \\noindent\n""")

    def test_all_wrappers_can_be_overridden(self):
        configure(simpleMode=True)

        result_verb = verbatim('i can', "to be wrapped")
        result_term = terminal('haz', "to be wrapped")
        result_fancy= fancyverb('cheezeburger', "to be wrapped")


        expected = dedent("""\
            \\begin{Verbatim}
            to be wrapped
            \\end{Verbatim}\n""")

        assert result_verb == expected
        assert result_term == expected
        assert result_fancy == expected
