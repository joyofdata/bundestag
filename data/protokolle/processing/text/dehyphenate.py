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


text = codecs.open(srcFile,"r","utf-8").read()

# second part all uncapitalized > simple word
text = re.compile("([a-zA-ZáàéèßÄÖÜäöü]+)-\\r?\\n([a-záàéèßäöü]+)").sub("\\1\\2\\n",text)
# all characters capitalized > simple word
text = re.compile(u"([A-ZÄÖÜ]+)-\\r?\\n([A-ZÄÖÜ]+)").sub("\\1\\2\\n",text)
# first and second part start capitalized then turn uncapitalized > composite - keep hyphens
text = re.compile(u"([A-ZÄÖÜ][A-ZÄÖÜa-záàéèßäöü]+)-\\r?\\n([A-ZÄÖÜ][A-ZÄÖÜa-záàéèßäöü]+)").sub("\\1-\\2\\n",text)

text = re.compile(u"([a-zA-ZáàéèßÄÖÜäöü]+)-( +\([CD]\))\\r?\\n([a-záàéèßäöü]+)").sub("\\1\\3\\2\\n",text)
text = re.compile(u"([A-ZÄÖÜ]+)-( +\([CD]\))\\r?\\n([A-ZÄÖÜ]+)").sub("\\1\\3\\2\\n",text)
text = re.compile(u"([A-ZÄÖÜ][A-ZÄÖÜa-záàéèßäöü]+)-( +\([CD]\))\\r?\\n([A-ZÄÖÜ][A-ZÄÖÜa-záàéèßäöü]+)").sub("\\1-\\3\\2\\n",text)

f = open(reunionFile, encoding="utf-8", mode="w")
f.write(text)
f.close()

