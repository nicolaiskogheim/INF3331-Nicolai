from textwrap import dedent
simple=False

def mode(func):
    def inner(*args, **kwargs):
        if simple:
            return verbatim(*args, **kwargs)
        else:
            return func(*args, **kwargs)
    return inner

def verbatim(s, content):
    before="\\begin{Verbatim}"
    after="\\end{Verbatim}\n"

    return "\n".join([before, content, after])

@mode
def terminal(s, content):
    before = dedent("""\
        \\begin{Verbatim}[numbers=none,frame=lines,label=\\fbox{{\\tiny Terminal}},fontsize=\\fontsize{9pt}{9pt},
        labelposition=topline,framesep=2.5mm,framerule=0.7pt]""")
    after=dedent("""\
        \\end{Verbatim}
        \\noindent
        """)

    return "\n".join([before, content, after])
@mode
def fancyverb(s, content):
    before=dedent("""\
        \\begin{shadedquoteBlueBar}
        \\fontsize{9pt}{9pt}
        \\begin{Verbatim}""")
    after=dedent("""\
        \\end{Verbatim}
        \\end{shadedquoteBlueBar}
        \\noindent
        """)

    return "\n".join([before, content, after])

def configure(simpleMode=False):
    global simple
    if simpleMode:
        simple = True
