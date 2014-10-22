import pytest
import os
import subprocess
from PreTeX import prepro

testfiles = 'testfiles'

test_file_in = 'tex_before.xtex'
test_file_out = 'tex_after.tex'
tmp_file_out = 'tex_processed.tmp'

preprocessor = '../../PreTeX/prepro.py'
command = 'python'
class TestShit():
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

    # def test_prepro_e2e_from_scanner(self):
    #     expected_result_fpath = os.path.join(testfiles, test_file_out)
    #     with open(expected_result_fpath) as f:
    #         expected = f.read()
    #
    #     unprocessed_fpath = os.path.join(testfiles, test_file_in)
    #     with open(unprocessed_fpath) as f:
    #         unprocessed = f.read()
    #
    #     actual = prepro.Scanner().scan(unprocessed)
    #
    #     assert actual == expected
