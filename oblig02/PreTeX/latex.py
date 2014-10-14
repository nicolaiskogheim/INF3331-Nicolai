class Latex(object):

      def verbatim(self, content):
          before="\\begin{Verbatim}"
          after="\\end{Verbatim}"

          return "\n".join([before, content, after])

      def terminal(self, content):
          before="""\\begin{Verbatim}[numbers=none,frame=lines,label=\\fbox{{\\tiny Terminal}},fontsize=\\fontsize{9pt}{9pt},
labelposition=topline,framesep=2.5mm,framerule=0.7pt]"""
          after="""\\end{Verbatim}
\\noindent"""

          return "\n".join([before, content, after])

      def fancyverb(self, content):
          before="""\\begin{shadedquoteBlueBar}
\\fontsize{9pt}{9pt}
\\begin{Verbatim}"""
          after="""\\end{Verbatim}
\\end{shadedquoteBlueBar}
\\noindent"""

          return "\n".join([before, content, after])
