import os
import re
import subprocess

def extract(content, regex):
    """
        Given string and regex, returns the full match,
        with no respect to match groups.
    """
    result = re.search(regex, content, re.M)
    if result:
        return result.group(0)
    else:
        return ""

def execute(command):
    """
        Executes a shell command,
        returns result, error.
    """
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result, err = process.communicate()
    return str(result), str(err)



def load(path):
    """
        Returns file contents of path
    """
    with open(path, 'r') as f:
        file_contents = f.read()
    return file_contents

def write(path, content):
    """
        Writes content to path.
        Creates intermediary folders if missing.
    """
    dirPath = os.path.dirname(path)

    if not os.path.exists(dirPath) and dirPath != '':
        os.makedirs(dirPath)
    with open(path, 'w') as f:
        f.write(content)
    return content
