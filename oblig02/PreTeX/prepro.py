import argparse
import helper
import inspect
import logging
import line_number_map
from os import path, makedirs
import re
import latex

class State:
    """
        Maintains program state
        Used by handlers to keep track of variables
    """
    variables = {}

    @staticmethod
    def setVar(key, value):
        State.variables[key] = value

    @staticmethod
    def getVar(key):
        return State.variables.get(key)


class Handlers(object):
    """
        A simple iterator.
        Iterates over every subclass of Handler
    """
    def __init__(self):
        self.handlers = []
        for cls in Handler.__subclasses__():
          self.handlers.append(cls)

    def __iter__(self):
        self.index = -1

        return self

    def next(self):
        self.index = self.index + 1
        if self.index == len(self.handlers):
            raise StopIteration
        return self.handlers[self.index]

class Handler(object):
    """
        Handler base class / interface.
        Inheriting classes must implement the handle() method,
        and can override wants(), and output() if necessary.
    """
    def wants(self, input):
        """
            Test input on this method to know if the handler
            can handle the input.
        """
        acceptsLine = True if self.pattern.match(input) else False
        if acceptsLine:
            logging.info("  "+self.__class__.__name__+" handler processes: "+input)
        return acceptsLine

    def handle(*args, **kwargs):
        """
            This is the method doing all the lifting
        """
        raise NotImplementedError("Should have implemented handle method!")

    def output(self, wrapper="default"):
        """
            Returns handled input.
            Wrapper is a function that wraps the output,
            before it is returned. Defaults to setting in each handler.
        """
        if wrapper == "default":
            if self.defaultWrapper:
                return self.defaultWrapper(self.result)
            else:
                return self.result
        elif wrapper:
            return wrapper(self.result)
        else:
            return self.result

class Import(Handler):
    """
        Imports content from filename matching regex:
        import filename (regex)
    """
    endToken = None
    multiline = endToken != None
    defaultWrapper = latex.fancyverb
    pattern = re.compile(r'^import ([^\s]*) (.*)$')
    action = "Imorted"

    def handle(self, input):
        result = self.pattern.match(input)

        self.script_name = result.group(1)
        self.regex = result.group(2)

        file_contents = helper.load(self.script_name)

        self.result =helper.extract(file_contents, self.regex)

class InlineImport(Handler):
    """
        Imports content between import and endtoken.

        import
        content
        endtoken

        Default is to wrap
    """
    endToken = "%@"
    multiline = endToken != None
    defaultWrapper = latex.fancyverb
    pattern = re.compile(r'^import\s*$')
    action = "Wrapped inline code"

    def handle(self, input):
        _, content = input.split("\n", 1)
        self.result = content

class Exec(Handler):
    """
        Executes command and args, returns result
        exec command args
    """
    endToken = None
    multiline = endToken != None
    defaultWrapper = latex.terminal
    pattern = re.compile(r'^exec ([^\s]+) (.*)$')
    action = "Executed"

    def handle(self, input):
        result = self.pattern.match(input)

        command = result.group(1)
        args = result.group(2)

        execution_result, err =helper.execute("{0} {1}".format(command, args).split(" "))

        self.result = "$ " + command + " " + args + "\n" + execution_result

class FakeInlineExec(Handler):
    """
        Returns text between exec and endtoken
        exec
        content
        endtoken
    """
    endToken = "%@"
    multiline = endToken != None
    defaultWrapper = latex.terminal
    pattern = re.compile(r'^exec\s*$')
    action = "Wrapped inline execution"

    def handle(self, input):
        _, content = input.split("\n", 1)
        self.result = content

class Verb(Handler):
    """
        Returns content between verbatim and endtoken
        verbatim
        content
        endtoken
    """
    endToken = "%@"
    multiline = endToken != None
    defaultWrapper = latex.verbatim
    pattern = re.compile(r'^verb$')
    action = "Wrapped in verbatim block"

    def handle(self, input):
        _, content = input.split("\n", 1)
        self.result = content

class InlineShellCmd(Handler):
    """
        Executes code like a shell, and returns it.
        Allowed commands is python and bash.
        Ex:
        bash cat file.txt
    """
    endToken="%@"
    multiline = endToken != None
    defaultWrapper = latex.terminal
    pattern = re.compile(r'^(python|bash) .*$')
    action = "Ran inline code in shell"

    def handle(self, input):
        firstLine, code = input.split("\n",1)
        command, fakeargs = firstLine.split(" ", 1)

        executed, err =helper.execute([command,'-c',"""\n{0}""".format(code)])

        self.result = "\n".join([firstLine, executed]).rstrip("\n")

class Var(Handler):
    """
        Declares and assigns a value to a variable
        var name = value
        This handler uses State to save the variable.
    """
    endToken = None
    multiline = endToken != None
    defaultWrapper = None
    pattern = re.compile(r'^var\s([A-Za-z0-9_:.-]+)\s*=\s*([A-Za-z0-9_:.-]+)$')
    action = "Assigned to variable"

    def handle(self, input):
        m = self.pattern.match(input)
        key, value = m.group(1), m.group(2)

        State.setVar(key,value)
        self.result = ""

class ShowHide(Handler):
    """
        Controls visibility of block.
        show name == value
        returns content if name equals value
        hide name == value
        returns empty string if name equals value
        and vice versa
    """
    endToken = "%@fi"
    multiline = endToken != None
    defaultWrapper = None
    pattern = re.compile(r'^(show|hide)\s([A-Za-z0-9_:.-]+)\s*==\s*([A-Za-z0-9_:.-]+)$')
    action = "Controlled visibility"

    def handle(self, input):
        firstLine, block = input.split("\n", 1)
        m = self.pattern.match(firstLine)
        visibility, key, value = m.group(1), m.group(2), m.group(3)

        show = True if visibility == "show" else False

        if show:
            if State.getVar(key) == value:
                self.result = block
            else:
                self.result = ""
        else:
            if State.getVar(key) == value:
                self.result = ""
            else:
                self.result = block

class PreproIncluded(Handler):
    """
        Runs filepath in
        include{filepath}
        through the preprocessor, and copies file to dedicated
        to-be-included folder.
        Returns path to preprocessed file.
    """
    endToken = None
    multiline = endToken != None
    defaultWrapper = None
    pattern = re.compile(r'include{([a-zA-Z_\-0-9\.\/\\][A-Za-z_\-\s0-9\.\/\\]*?)?([A-Za-z_\-\s0-9\.]+)(\.[a-zA-Z]+)}')
    action = "Preprocessed latex-included files"

    def handle(self, input):
        m = self.pattern.match(input)
        fpath, fname,  ext = m.group(1), m.group(2), m.group(3)
        originalFile = path.join(fpath, fname + ext)

        if not path.exists(originalFile):
            self.result = "" #"\\include{"+ originalFile +"}"
            logging.warn("'{0}' is not a file!".format(originalFile))
            logging.warn("It will not be included in the resulting .tex file.")
            return

        #if ext not "xtex": warn("Extension not xtex in {0}".format(fpath+ext))
        include_folder = "./preprocessed_tex_files_to_include"
        if not path.exists(include_folder):
            makedirs(include_folder)

        targetPath = path.join(include_folder,fpath, fname)

        thisScript = inspect.stack()[0][1]
        result, err= helper.execute(["python",thisScript, originalFile, targetPath+".tex"])


        # if err: out err
        # newPath = path.join(include_folder, path)
        self.result = "\\include{"+ targetPath +"}"

class BadInput(Handler):
    """
        "Catch all" handler.
        If no other handler has accepted the input,
        this one will, and returns comments about it
        in the preprocessed file.

        And yes, this one runs last because it is placed
        last in this file.
    """
    endToken = None
    multiline = endToken != None
    defaultWrapper = None
    pattern = re.compile(r'.*')
    action = "Errored"

    def handle(self, input):
        if input:
            self.result = "% Preprocessor: did not understand %@{0}".format(input)
        else:
            self.result = "% Preprocessor: found stray closing tag %@"

class Scanner:
    """
        Similar to a lexer/tokenizer.
        This class' responsibility is to iterate over the input
        and for each line "asking" a handler to handle that line.
        If yes, the scanner asks if the handler wants multiple lines,
        and if true then the scanner captures lines until the handlers
        endtoken is found.
    """

    def __init__(self):
        self.captured = ""

    def scan(self,content, token="%@", startLine=0):
        lines = content.split("\n")

        self.capturing = False
        newfile = ""
        for i, line in enumerate(lines):
            if self.capturing:
                if line == self.handler.endToken:
                    self.capturing = False
                    self.handler.handle(self.release())
                    scanForNestedBlocks = Scanner().scan(self.handler.output(), token=token, startLine=i)
                    newfile += scanForNestedBlocks + "\n"
                    line_number_map.addPair(i+1+startLine, len(newfile.split('\n')) + startLine)

                    continue
                else:
                    self.capture(line)

            elif line.startswith(token):
                line = line[2:]
                for handler in Handlers():
                    self.handler = handler()
                    if self.handler.wants(line):
                        newfile += "% {0} from line {1}\n".format(handler.action,i+1+startLine)
                        if self.handler.multiline:
                            self.capturing = True
                            self.capture(line)
                        else:
                            self.handler.handle(line)
                            newfile += self.handler.output()
                        break
                else:
                    logging.error("No handlers to parse file with. Aborting..")
                    sys.exit(1)
            else:
                newfile += line + "\n"
                line_number_map.addPair(1+i+startLine,
                                        len(newfile.split('\n')) -1 + startLine)


        newfile = newfile.rstrip()

        #Add  line number map if not recursincg
        if startLine == 0:
            newfile += line_number_map.getEncoded()

        return newfile

    def capture(self, line):
        self.captured += line + "\n"

    def release(self):
        x = self.captured.rstrip("\n")
        self.captured = ""
        return x

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="path to xtex to preprocess")
    parser.add_argument("destination", help="path to preprocessed file")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true", default=False,
                        help="Be verbose about what is going on")
    group.add_argument("-q", "--quiet", action="store_true", default=False,
                        help="Suppress normal output. Returns >0 on error, 0 otherwise.")

    parser.add_argument("-s", "--simple", action="store_true", default=False,
                        help="Keeps formatting to a minimum, using only the standard"+\
                        " verbatim latex environment.")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    elif args.quiet:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.CRITICAL)
    else:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARNING)

    if args.simple:
        latex.configure(simpleMode=True)


    sourcefile = helper.load(args.source)
    output = Scanner().scan(sourcefile)
    helper.write(args.destination, output)
