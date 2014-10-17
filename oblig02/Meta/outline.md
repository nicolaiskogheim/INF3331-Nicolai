#PreTeX program outline

TOC:
  - Progress on assignment
  - Other stuff

### Progress on assignment

- [x] Oppgave 1: Kodeimport
- [x] Oppgave 2: Eksekvering av skript
- [x] Oppgave 3: Kodeformatering
- [x] Oppgave 5: Kode-eksekvering
- [x] Oppgave 6: Skjult tekst
- [x] Oppgave 7: Kompilering av preprosessert LATEX-fil
- [x] Oppgave 9: Filtre
- [x] Oppgave 10: Linjenummerering
- [x] Oppgave 11: Front-end til preprosessor
- [ ] Oppgave 12: Testing og dokumentasjon
  * ***prepro.py***
  - [ ] State
  - [ ] Handlers
  - [ ] Handler
  - [ ] Import
  - [ ] InlineImport
  - [ ] Exec
  - [ ] FakeInlineExec
  - [ ] Verb
  - [ ] InlineShellCmd
  - [ ] Var
  - [ ] ShowHide
  - [ ] PreproIncluded
  - [ ] BadInput
  - [ ] Scanner
  - [ ] main
  * ***helper.py***
  - [ ] extract
  - [ ] execute
  - [ ] load
  - [ ] write
  * ***compile.py***
  - [ ] compile_latex
  - [ ] main
  * ***line_number_map.py***
  - [ ] addPair
  - [ ] getEncoded
  - [ ] getDecoded
  - [ ] getLineNumber
  * ***latex***
  - [ ] mode
  - [ ] verbatim
  - [ ] terminal
  - [ ] fancyverb
- [ ] Oppgave 13: Rapport

###Notes
There are some things that needs to be done/considered before release
which I just haven't bothered fixing yet.

* define what extension this preprocessor operates on
  * xtex is chosen at leas one place. Enforce whatever is the result
    * No. It is not. sortof. Well yes. bah
  * remember to document why the \include{path/to/file} became
    %@include path/to/file
  * Make preprocessor die on warnings
    * Have an option to ignore this


Important topics:
* Single Responsibility Principle
* Open/Closed Principle
* Testability
* Configurability
  * Single entry point for customising token and
    what kind of latex to insert and what keywords
    to match on
  * Option to choose between few dependencies in latex
    or full-blown fancypants result.
* Extensibility
* Some support for configuration inside the latex-file
  * Setting variables for use with `show`-method
  * Basic expressions in `show`-module (not priority)
  * Configure the preprosessor from the input file
* Nestability
  * Point here to keep the program clean while
    allowing nested tags
* Error-reporting with reference to line in source file

--------------------------------------------------------

The preprosessor consists of three main parts:
  * Command handlers
  * Command-helpers
  * Scanner

###Command handlers
Methods for replacing markup with latex.
Implements a `wants(line) return boolean wants` that the
scanner uses to know where to send output, and a
`multiline` property to know whether to call
the function with the single line or with more lines until `endtoken` is met.
There will be an iterator that provides the scanner with these handlers.
See [PyDoc on iterators](https://docs.python.org/2/tutorial/classes.html#iterators)

###Command-helpers
Utility functions that is shared between the handlers,
like executing code, or loading or saving files.

###Scanner
Scans the unprocessed PreTeX file line by line,
and for each line iterates over the handlers till
a handler that wants the line is met.  
This function also takes care of building the
line number map which is for the compiler so that
it can know where each line in the new file originated from.


Additionally there should some functionality to support

  * Creating an output-file (duh..)
  * Logging
    * Successful prosessing
    * Errors
      * Option to ignore errors and continue
    * Different levels of output?
    * Option to suppress output (-q)


###Input and output files
The input file is read on program start
and the scanner is called with the contents as-is.
Upon successful termination, the scanner returns
the new content, which then will be written to
a new file.


###Side note on logging
  Each handler can have attributes `errMsg` and
  `sucMsg` which is a string to be interpolated
  by the scanner.
  Example:
```
errMsg="Error: Bad formatting at line {0}. Code: {1}"
sucMsg="From line {0} inserting execution result {1}"
```
Whatever part of this message that is not unique,
could be added in by a Logger-decorator.


## Scanner
This is the one place that I'm not satisfied with.
It's to much going on.
The scanner is supposed to scan, and make decisions
based on whether the line starts with a token, and maybe
that should be it.  
Let's list the cases:

* Line does not start with token : Just add current line to output-lines
* Line starts with token : Iterate over handlers, running their .wants()
method until one returns true.

When a handler wants a line, there are new scenarios:  
* The `handler.multiline` is `False`: line to write = `handler.handle(line).output()`
* `handler.multiline` is `True`: Set `capture` to `True`.
  - Each line from hereon is temporarily saved with calling `capture(line)`
  * Line starts with `handler.endtoken` : lines to write = `handler.handle(releaseCaptured()).output()`
  * Line does not start with `handler.endtoken` : `capture(line)`


The solution may be to have helper methods for many of the little
things that happens in the scanner.


**Note** about prepro code that wraps other prepro code
(like the `%@show` directive):  
Always when a multiline capture is handled and returned,
the scanner will call itself to process eventual code that
remains. This allows infinite levels of nesting.

# Hello about wrapping handler output in latex
The output method can take a wrapper function
that wraps stuff. This requires the scanner to
know something about what it has processed, which
is I don't want. Come back to this laetar.  
Laetar: Oh, yes, the output def's can have a default handler
