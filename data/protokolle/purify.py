import re
import codecs
import sys
import os

if len(sys.argv) < 2:
  exit("purify.py [txt file to process]")

srcFile = sys.argv[1]

if not os.path.exists(srcFile):
  exit("source file not found.")

if not re.compile("reunited.txt$").findall(srcFile):
  exit("name of source file is supposed to end with .reunited.txt")

fileName = os.path.basename(srcFile)
purifiedFile = os.path.dirname(srcFile) + "/" + re.compile("reunited").sub("pure", fileName)


text = codecs.open(srcFile,"r","utf-8").read()

text = re.compile("%% NEW BLOCK %%").sub("",text)
text = re.compile("[^-A-ZÄÖÜa-zäöüáàéèß\\r\\n]").sub(" ",text)

f = open(purifiedFile, encoding="utf-8", mode="w")
f.write(text)
f.close()

