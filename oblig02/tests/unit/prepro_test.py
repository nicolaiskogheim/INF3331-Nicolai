import pytest
import os.path
import tempfile
from shutil import rmtree
from PreTeX.prepro import Scanner, Handler, Handlers, Import, Exec, Verb
from PreTeX import helper


class TestScanner:

    def test_returns_identical_if_no_tokens_found(self):
        text = "This is\n a test with\n\\begin{latex} that sould not get altered"

        result = Scanner().scan(text)

        # Assert that the result begins with `text`
        # This is because the scanner adds a line number map
        # at the bottom
        assert result.startswith(text) == True


class TestImportHandler:

      def test_import_handler_wants_preprocessor_code(self):
          goodHandlerInput = "import fakepath.py (regex)"
          badHandlerInput = "exec fakepath.py"

          x = Import().wants(goodHandlerInput)
          y = Import().wants(badHandlerInput)

          assert x == True
          assert y == False

      def test_import_handler_is_a_single_line_handler(self):
          x = Import().multiline

          assert x == False

      def test_import_handler_extracts_path_and_regex(self, monkeypatch):
          def extractmock(*args):
              pass
          def filehelpermock(*args):
              pass
          monkeypatch.setattr(helper, 'extract', extractmock)
          monkeypatch.setattr(helper, 'load', filehelpermock)

          fakepath = "faketest.py"
          fakeregex = "(^some [arbitraty] regex)"
          handlerInput="import {0} {1}".format(fakepath, fakeregex)
          importhandler = Import()

          importhandler.handle(handlerInput)

          x = importhandler.script_name
          y = importhandler.regex

          assert x == fakepath
          assert y == fakeregex

      def test_import_handler_imports_content_with_respect_to_regex(self, monkeypatch):
          handlerInput = "import fakepath.py (\t*this$)"

          def FileHelperMock(*args):
              return "\t\tthat\n\t\tthis not\n\t\tthis"
          def extractMock(content, regex):
              if content not in "\t\tthat\n\t\tthis not\n\t\tthis" \
              or regex not in "(\t*this$)":
                raise AssertionError
              return "\t\tthis"

          monkeypatch.setattr(helper, 'load', FileHelperMock)
          monkeypatch.setattr(helper, 'extract', extractMock)
          x = Import()
          x.handle(handlerInput)

          assert x.output(wrapper=None) == "\t\tthis"

class TestExecHandler:

      def test_exec_handler_wants_preprocessor_code(self):
          goodHandlerInput = "exec python script_example.py 4"
          badHandlerInput  = "import python script_example.py 4"

          x = Exec().wants(goodHandlerInput)
          y = Exec().wants(badHandlerInput)

          assert x == True
          assert y == False

      def test_exec_handler_is_a_single_line_handler(self):
          x = Exec().multiline

          assert x == False

      def test_exec_handler_executes_code(self, monkeypatch):
          def execmock(*args):
              return "24.0", ""
          monkeypatch.setattr(helper, 'execute', execmock)

          handlerInput = "exec python script_example.py 4"
          handler = Exec()

          handler.handle(handlerInput)

          assert handler.output(wrapper=None) == "$ python script_example.py 4\n24.0"



class TestVerbHandler:

      def test_verb_handler_wants_preprocessor_code(self):
          goodHandlerInput = "verb"
          badHandlerInput  = "verb bad stuff"

          x = Verb().wants(goodHandlerInput)
          y = Verb().wants(badHandlerInput)

          assert x == True
          assert y == False

      def test_exec_handler_is_a_multi_line_handler(self):
          x = Verb().multiline

          assert x == True
