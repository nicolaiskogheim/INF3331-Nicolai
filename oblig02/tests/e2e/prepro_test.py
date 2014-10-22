import pytest
import os
import subprocess
from PreTeX import prepro
from PreTeX.cd import cd
import inspect

testfiles = 'testfiles'

test_file_in = 'tex_before.xtex'
test_file_out = 'tex_after.tex'
scanner_test_file_out = 'scanner_after.tex'
tmp_file_out = 'tex_processed.tmp'

preprocessor = '../../PreTeX/prepro.py'
command = 'python'
class TestPrepro():
    def test_prepro_e2e_from_main(self):
        try:
            expected_result_fpath = os.path.join(testfiles, test_file_out)
            with open(expected_result_fpath) as f:
                expected = f.read()

            unprocessed_fpath = os.path.join(testfiles, test_file_in)
            actual_result_fpath = os.path.join(testfiles, tmp_file_out)
            args = [command, preprocessor, unprocessed_fpath, actual_result_fpath]

            print args

            process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result, error = process.communicate()

            with open(actual_result_fpath) as f:
                actual = f.read()

                assert actual == expected
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        except ValueError:
            print "Could not convert data to an integer."
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise



# Faar error med stier

    def test_prepro_e2e_from_scanner(self):
        thisScript = os.path.abspath(inspect.stack()[0][1])
        sourcefolder = thisScript.rsplit(os.path.sep,1)[0]
        with cd(sourcefolder):

            expected_result_fpath = os.path.join(testfiles, scanner_test_file_out)
            with open(expected_result_fpath) as f:
                expected = f.read()

            unprocessed_fpath = os.path.join(testfiles, test_file_in)
            with open(unprocessed_fpath) as f:
                unprocessed = f.read()

            with cd(testfiles):
                actual = prepro.Scanner().scan(unprocessed)

            assert actual == expected
