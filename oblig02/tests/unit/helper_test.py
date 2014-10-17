import os
import tempfile
import subprocess
from PreTeX import helper
from PreTeX import helper

def setup_module(module):
    tmpdir = tempfile.mkdtemp()
    os.chdir(tmpdir)

class TestHelper:
    def test_extract_extracts(self):
        content = "This is a test. I'm not a sk8er boi."
        regex = "sk[1-9][aeoir]{2} [\w]*\.$"

        result = helper.extract(content, regex)

        assert result == "sk8er boi."

    def test_extract_returns_empty_sting_if_no_match(self):
        content = "Hello. This is a test."
        regex = "I will not match nothin'"

        result = helper.extract(content, regex)

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

        result = helper.execute([command, args])

        assert result[0] == "24.0"

    def test_helper_can_load_file(self):
        file_name = 'testefil'
        file_contents = 'tekst'
        file = open(file_name, 'w')
        file.write(file_contents)
        file.close()

        result = helper.load(file_name)

        assert result == file_contents

    def test_helper_can_write_file(self):
        file_name = 'testefil2'
        file_contents = 'tekst'

        helper.write(file_name,file_contents)

        with open(file_name, 'r') as f:
            read_contents = f.read()

        assert read_contents == file_contents
