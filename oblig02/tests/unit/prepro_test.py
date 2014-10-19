import pytest
import os
import tempfile
from shutil import rmtree
from PreTeX.prepro import Scanner, Handler, Handlers, Import, InlineImport, Exec, FakeInlineExec, Verb, InlineShellCmd, ShowHide, State, BadInput, PreproIncluded, Var
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

class TestHandler:
    def test_state(self):
        State.setVar("foo", "bar")

        assert State.getVar("foo") == "bar"
        assert not State.getVar("baz")

    def test_handler(self):
        handler = Handler()

        assert handler.wants

        with pytest.raises(NotImplementedError):
            handler.handle()

        assert handler.output

    def test_handlers(self):
        handler_iterator = Handlers()

        # test that handler iterator iterates over handlers,
        # and only handlers
        for handler in handler_iterator:
            foundOne = True
            assert handler.wants
            assert handler.handle
            assert handler.output

        assert foundOne, "No handlers available. Without them, the program cannot run."

    def test_inlineimport(self):
        handler = InlineImport()

        assert handler.multiline
        assert handler.wants("import")
        assert handler.wants("import        ")
        assert not handler.wants("import file.py args")

        handler.handle("import\ndummy content")
        assert handler.output(wrapper=None) == "dummy content"

    def test_fakeinlineexec(self):
        handler = FakeInlineExec()

        assert handler.multiline
        assert handler.wants("exec")
        assert handler.wants("exec      ")
        assert not handler.wants("exec filename.py")

        handler.handle("exec\nbash 4\n24")
        assert handler.output(wrapper=None) == "bash 4\n24"

    def test_inlineshellcmd(self, monkeypatch):
        def executeMock(*args):
            return str(24), str(None)

        monkeypatch.setattr(helper, 'execute', executeMock)
        handler = InlineShellCmd()

        assert handler.multiline
        assert handler.wants("python test.py 4")
        assert handler.wants("bash hello.sh -e")
        assert not handler.wants("rm args")

        handler.handle("fake 4\nfoocmd -l")
        assert handler.output(wrapper=None) == "fake 4\n24"

    def test_showhide(self, monkeypatch):
        x = {"this":"true"}
        @staticmethod
        def stateMock(key):
            return x.get(key)

        monkeypatch.setattr(State, 'getVar', stateMock)
        handler = ShowHide()

        assert handler.multiline
        assert handler.wants("show foo==bar")
        assert handler.wants("hide baz==bat")
        assert not handler.wants("help me==now")
        assert not handler.wants("show picz")

        handler.handle("show var==false\nThis is nothing\n")
        assert handler.output(wrapper=None) == ""

        handler.handle("hide var==false\nThis is something\n")
        assert handler.output(wrapper=None) == "This is something\n"

        handler.handle("show this==true\nThis is something\n")
        assert handler.output(wrapper=None) == "This is something\n"

        handler.handle("hide this==true\nThis is nothing\n")
        assert handler.output(wrapper=None) == ""

    def test_preproincluded(self, monkeypatch):
        def monkeyExists(*args):
            return True
        def monkeyMakedirs(*args):
            pass
        def monkeyExecute(*args):
            return "dummy content", None
        monkeypatch.setattr(os.path, 'exists', monkeyExists)
        monkeypatch.setattr(os, 'makedirs', monkeyMakedirs)
        monkeypatch.setattr(helper, 'execute', monkeyExecute)
        handler = PreproIncluded()

        assert not handler.multiline
        assert handler.wants("include{/absolute/path/to/file.xtex}")
        assert handler.wants("include{relative/path/to/file.tex}")
        assert handler.wants("include{any_file.actually}")
        assert not handler.wants("include my/file.tex")
        assert not handler.wants("include(this.file)")

        handler.handle("include{dummy/file.tex}")
        assert "dummy/file" in handler.output()

    def test_var(self, monkeypatch):
        key, value = "foo", "bar"
        @staticmethod
        def monkeySetVar(left, right):
            if not left == key \
            or not right == value:
                pystest.fail("var did not call state with right params")
        monkeypatch.setattr(State, 'setVar', monkeySetVar)

        handler = Var()

        assert not handler.multiline
        assert handler.wants("var hello=true")
        assert handler.wants("var for = realz")
        assert not handler.wants("var for == realz")
        assert not handler.wants("where am = i")

        handler.handle("var foo=bar")

    def test_badinput(self):
        handler = BadInput()

        assert not handler.multiline
        assert handler.wants("This handler eats everything")
        assert handler.wants("$That is the purpose")
        assert handler.wants("of this %$2934789 handler.")

        handler.handle("test")
        assert handler.output().find("test")
        assert handler.output().find("did not understand")
