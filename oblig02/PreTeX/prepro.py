import argparse
import os
import re
import subprocess
import StringIO
from latex import Latex

class State:
    variables = {}

    @staticmethod
    def setVar(key, value):
        State.variables[key] = value

    @staticmethod
    def getVar(key):
        return State.variables.get(key)


class Handlers(object):

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
    def wants(self, input):
        acceptsLine = True if self.pattern.match(input) else False
        if acceptsLine:
            print self.__class__.__name__ + " takes care of: " + input
        return acceptsLine

    def handle(*args, **kwargs):
        raise NotImplementedError("Should have implemented handle method!")

    def output(*args, **kwargs):
        raise NotImplementedError("Should have implemented output method!")

class Import(Handler):

    endToken = None
    multiline = endToken != None
    pattern = re.compile(r'^import ([^\s]*) (.*)$')
    action = "Imorted"

    def handle(self, input):
        result = self.pattern.match(input)

        self.script_name = result.group(1)
        self.regex = result.group(2)

        file_contents = FileHelper().load(self.script_name)

        self.result = Helper().extract(file_contents, self.regex)

    def output(self, wrapper=Latex().fancyverb):
        if wrapper:
            return wrapper(self.result)
        else:
            return self.result

class InlineImport(Handler):
    endToken = "%@"
    multiline = endToken != None
    pattern = re.compile(r'^import\s*$')
    action = "Wrapped inline code"

    def handle(self, input):
        _, content = input.split("\n", 1)
        self.result = content

    def output(self, wrapper=Latex().fancyverb):
        if wrapper:
            return wrapper(self.result)
        else:
            return self.result

class Exec(Handler):
    endToken = None
    multiline = endToken != None
    pattern = re.compile(r'^exec ([^\s]+) (.*)$')
    action = "Executed"

    def handle(self, input):
        result = self.pattern.match(input)

        command = result.group(1)
        args = result.group(2)

        execution_result, err = Helper().execute("{0} {1}".format(command, args).split(" "))

        self.result = "$ " + command + " " + args + "\n" + execution_result

    def output(self, wrapper=Latex().terminal):
        if wrapper:
            return wrapper(self.result)
        else:
            return self.result

class FakeInlineExec(Handler):
    endToken = "%@"
    multiline = endToken != None
    pattern = re.compile(r'^exec\s*$')
    action = "Wrappen inline execution"

    def handle(self, input):
        _, content = input.split("\n", 1)
        self.result = content

    def output(self, wrapper=Latex().terminal):
        if wrapper:
            return wrapper(self.result)
        else:
            return self.result

class Verb(Handler):

      endToken = "%@"
      multiline = endToken != None
      pattern = re.compile(r'^verb$')
      action = "Wrapped in verbatim block"

      def handle(self, input):
          _, content = input.split("\n", 1)
          self.result = content

      def output(self, wrapper=Latex().verbatim):
          if wrapper:
              return wrapper(self.result)
          else:
              return self.result

class InlineShellCmd(Handler):

      endToken="%@"
      multiline = endToken != None
      pattern = re.compile(r'^(python|bash) .*$')
      action = "Ran inline code in shell"
      # Maybe format action message based on input to wants

      def handle(self, input):
          firstLine, code = input.split("\n",1)
          command, fakeargs = firstLine.split(" ", 1)

          executed, err = Helper().execute([command,'-c',"""\n{0}""".format(code)])

          firstLine = "$ {0} {1}".format(firstLine, fakeargs)
          self.result = "\n".join([firstLine, executed]).rstrip("\n")

      def output(self, wrapper=Latex().terminal):
          if wrapper:
              return wrapper(self.result)
          else:
              return self.result

class Var(Handler):
    endToken = None
    multiline = endToken != None
    pattern = re.compile(r'^var\s([A-Za-z0-9_:.-]+)\s*=\s*([A-Za-z0-9_:.-]+)$')
    action = "Assigned to variable"

    def handle(self, input):
        m = self.pattern.match(input)
        key, value = m.group(1), m.group(2)

        State.setVar(key,value)

    def output(self):
        return ""

class ShowHide(Handler):
    endToken = "%@fi"
    multiline = endToken != None
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

    ## Er det riktig med wrapper paa output?

    def output(self, wrapper=None):
        return self.result

class PreproIncluded(Handler):
    endToken = None
    multiline = endToken != None
    pattern = re.compile(r'include{([a-zA-Z_\-0-9\.][A-Za-z_\-\s0-9\.\/\\]*?)?([A-Za-z_\-\s0-9\.]+)(\.[a-zA-Z]+)}')
    action = "Preprocessed latex-included files"

    def handle(self, input):
        m = self.pattern.match(input)
        fpath, fname,  ext = m.group(1), m.group(2), m.group(3)
        originalFile = os.path.join(fpath, fname + ext)

        if not os.path.exists(originalFile):
            self.result = "\\include{"+ originalFile +"}"
            print "Error: '{0}' is not a file!".format(originalFile)
            return

        #if ext not "xtex": warn("Extension not xtex in {0}".format(fpath+ext))
        include_folder = "./preprocessed_tex_files_to_include"
        if not os.path.exists(include_folder):
            os.makedirs(include_folder)

        targetPath = os.path.join(include_folder,fpath, fname + ".tex")

        result, err = Helper().execute(["python","prepro.py", originalFile, targetPath])


        # if err: out err
        # newPath = os.path.join(include_folder, path)
        self.result = "\\include{"+ targetPath +"}"

    def output(self, wrapper=None):
        # Never use wrapper here
        return self.result

class BadInput(Handler):

      endToken = None
      multiline = endToken != None
      pattern = re.compile(r'.*')
      action = "Errored"

      def handle(self, input):
          if input:
              self.result = "% Preprocessor: did not understand %@{0}".format(input)
          else:
              self.result = "% Preprocessor: found stray closing tag %@"

      def output(self):
          return self.result

class Scanner:

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
                    newfile += scanForNestedBlocks
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
                else: # will never happen...
                    pass
            else:
                newfile += line + "\n"


        #Strip last newline and or trailing whitespace
        newfile = newfile.rstrip()

        # maybe strip out all line numbers if no errors

        return newfile

    def capture(self, line):
        self.captured += line + "\n"

    def release(self):
        x = self.captured.rstrip("\n")
        self.captured = ""
        return x


class Helper:
  def extract(self, content, regex):
      result = re.search(regex, content, re.M)
      if result:
          return result.group(0)
      else:
          return ""

  def execute(self, command):
      legalCommands = ["python"]
      # if command not in legalCommands:
      #     msg = "The command {0} is not in the list of allowed commands"
      #     msg += "Feel free to add it in if you want"
      #     msg = msg.format(command)
      #     raise Exception(msg)
      # else:
      if True:
          process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
          result, err = process.communicate()
          return str(result), str(err)

class FileHelper:

    def load(self, path):
        with open(path, 'r') as f:
            file_contents = f.read()
        return file_contents

    def write(self, path, content):
        dirPath = os.path.dirname(path)

        if not os.path.exists(dirPath) and dirPath != '':
            os.makedirs(dirPath)
        with open(path, 'w') as f:
            f.write(content)
        return content

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="path to xtex to preprocess")
    parser.add_argument("destination", help="path to preprocessed file")
    args = parser.parse_args()

    sourcefile = FileHelper().load(args.source)
    output = Scanner().scan(sourcefile)
    FileHelper().write(args.destination, output)

    # import doctest
    # doctest.testmod()
