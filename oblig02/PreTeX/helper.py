import os
import re
import subprocess

def extract(content, regex):
    result = re.search(regex, content, re.M)
    if result:
        return result.group(0)
    else:
        return ""

def execute(command):
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



def load(path):
    with open(path, 'r') as f:
        file_contents = f.read()
    return file_contents

def write(path, content):
    dirPath = os.path.dirname(path)

    if not os.path.exists(dirPath) and dirPath != '':
        os.makedirs(dirPath)
    with open(path, 'w') as f:
        f.write(content)
    return content
