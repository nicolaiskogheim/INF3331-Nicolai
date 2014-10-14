import subprocess
from prepro import Helper

class TestHelper:
      def test_extract_extracts(self):
          content = "This is a test. I'm not a sk8er boi."
          regex = "sk[1-9][aeoir]{2} [\w]*\.$"

          result = Helper().extract(content, regex)

          assert result == "sk8er boi."

      def test_extract_returns_empty_sting_if_no_match(self):
          content = "Hello. This is a test."
          regex = "I will not match nothin'"

          result = Helper().extract(content, regex)

          assert result == ""

      def test_execute_executes(self, monkeypatch):
          class communicatemock:
              def communicate(*args):
                return 24.0, None
          def popenmock(*args, **kwargs):
              return communicatemock()

          monkeypatch.setattr(subprocess, 'Popen', popenmock)

          command = "python"
          args = "dummy.py 3"

          result = Helper().execute(command, args)

          assert result == "24.0"
