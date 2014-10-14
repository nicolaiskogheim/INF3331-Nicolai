import os
import tempfile
from prepro import FileHelper

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

        result = FileHelper().load(file_name)

        assert result == file_contents

    def test_file_helper_can_write_file(self):
        file_name = 'testefil2'
        file_contents = 'tekst'

        FileHelper().write(file_name,file_contents)

        with open(file_name, 'r') as f:
            read_contents = f.read()

        assert read_contents == file_contents
