from textwrap import dedent
simple=False

def mode(func):
    """
        Decorator for all the wrappers.
        If simple == True, then every call to a wrapper
        will result in a call to the regular verbatim one.
    """
    def inner(*args, **kwargs):
        if simple:
            return verbatim(*args, **kwargs)
        else:
            return func(*args, **kwargs)
    return inner

def verbatim(s, content):
    """
        Wraps content in regular verbatim latex blocks.
    """
    before="\\begin{Verbatim}"
    after="\\end{Verbatim}\n"

    return "\n".join([before, content, after])

@mode
def terminal(s, content):
    """
        Wraps content in terminal-looking latex.
    """
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
    """
        Wraps content in fancy verbatim latex with
        light blue background.
    """
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
    """
        Sets the latex mode that controls whether
        to wrap content in fancy styles, or fall back
        to standard verbatim.
    """
    global simple
    if simpleMode:
        simple = True
