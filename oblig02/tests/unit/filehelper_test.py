import os
import tempfile
from PreTeX import helper

def setup_module(module):
    tmpdir = tempfile.mkdtemp()
    os.chdir(tmpdir)

class TestFileHelper:
    def test_file_helper_can_load_file(self):
        file_name = 'testefil'
        file_contents = 'tekst'
        file = open(file_name, 'w')
        file.write(file_contents)
        file.close()

        result = helper.load(file_name)

        assert result == file_contents

    def test_file_helper_can_write_file(self):
        file_name = 'testefil2'
        file_contents = 'tekst'

        helper.write(file_name,file_contents)

        with open(file_name, 'r') as f:
            read_contents = f.read()

        assert read_contents == file_contents
