import re
import codecs
import sys
import os

if len(sys.argv) < 2:
  exit("dehyphenate.py [txt file to process]")

srcFile = sys.argv[1]

if not os.path.exists(srcFile):
  exit("source file not found.")

if not re.compile("long.txt$").findall(srcFile):
  exit("name of source file is supposed to end with .long.txt")

fileName = os.path.basename(srcFile)
reunionFile = os.path.dirname(srcFile) + "/" + re.compile("long").sub("reunited", fileName)


text = codecs.open(fileName,"r","utf-8").read()

text = re.compile("([a-zA-ZáàéèßÄÖÜäöü]+)-\\r\\n([a-záàéèßäöü]+)").sub("\\1\\2\\r\\n",text)
text = re.compile("([a-zA-ZáàéèßÄÖÜäöü]+)-\\r\\n([A-ZÄÖÜ]+)").sub("\\1-\\2\\r\\n",text)

text = re.compile("([a-zA-ZáàéèßÄÖÜäöü]+)-( +\([CD]\))\\r\\n([a-záàéèßäöü]+)").sub("\\1\\3\\2\\r\\n",text)
text = re.compile("([a-zA-ZáàéèßÄÖÜäöü]+)-( +\([CD]\))\\r\\n([A-ZÄÖÜ]+)").sub("\\1-\\3\\2\\r\\n",text)

f = open(reunionFile, encoding="utf-8", mode="w")
f.write(text)
f.close()

