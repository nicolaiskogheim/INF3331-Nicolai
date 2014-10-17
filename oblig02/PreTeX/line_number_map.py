import logging
import re
rawmap = []
realmap = {}

def addPair(origLnr, newLnr):
    global rawmap
    rawmap.append("{0}:{1}".format(origLnr, newLnr))

def getEncoded():
    global rawmap
    return "\n\n%PreTex data. Ignore following line.\n"+\
           "%[{0}]".format(",".join(rawmap))

def getDecoded(path):
    global realmap
    if not path in realmap:
        helper.load(path).rstrip().split("\n")[-1]

        mapPattern = re.compile(r'%\[((?:\d+:\d+,)*(?:\d+:\d+))\]')
        match = mapPattern.match(lastLine)
        if not match:
            logging.error("Input file not properly formatted.")
            logging.error("\tPlease run it through the preprocessor again.")
            logging.error("This means that the linenumbers will point to")
            logging.error("the preprocessed file rather than the unprocessed one.")
            realmap[path] = "not found"
        else:
            realmap[path] = match.group(1).split(",")

    return realmap[path]

def getLineNumber(lnr, path):
    global realmap
    lnr = int(lnr)

    if realmap.get(path) == "not found":
        return lnr

    elif not path in realmap:
      realmap[path] = getDecoded(path)


    lastLnr = 0
    for m in realmap[path]:
      orig, new = m.split(":")
      if lnr < int(new):
        return lastLnr
      else:
        lastLnr = orig
