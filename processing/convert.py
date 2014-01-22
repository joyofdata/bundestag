# the source text file has to be UTF-8 encoded. text files
# created by xpdf are not UTF-8 endoded.

from numpy import zeros
from random import randrange
import re
import sys
import os

if len(sys.argv) < 2:
  exit("convert.py [txt file to process]");

srcFile = sys.argv[1]
 
if not os.path.exists(srcFile):
  exit("source txt file not found.")
  
if not srcFile[len(srcFile)-4:len(srcFile)] == ".txt":
  exit("source file needs to end with '.txt'.")
  
fileName = os.path.basename(srcFile)
fileName = fileName[0:len(fileName)-4]
  
layoutFile = os.path.dirname(srcFile) + "/" + fileName + ".layout.txt"
longFile = os.path.dirname(srcFile) + "/" + fileName + ".long.txt"

lines = []
dummies = []

f = open(srcFile, encoding="utf-8")

R = 0 # num of lines / rows
C = 0 # num of columns / chars in longest row

for line in f:
  line = line.rstrip('\n')
  
  # \x0c aka F(eed)F(orward) indicates a new page in case of
  # PDF to text conversion using xpdf.
  # In case of Bundestag protocols the first line of a page 
  # gets dangerously close sometimes to the previous page's last
  # or current page's second. To prevent confusion I just safety
  # wrap it with blank lines.
  if re.compile("\x0c").search(line):
    lines.append("")
    lines.append("")
    lines.append(re.compile("\x0c").sub("",line))
    lines.append("")
    lines.append("")
    R = R + 4
  else:
    lines.append(line)

  if len(line) > C:
    C = len(line)
  R = R + 1

f.close()
  
# M keeps whether a position in a text is considered as
# belonging to content or to empty space. The content
# (all True values in M) finally comprises a set of 
# rectangles which can be treated sequentially.

M = zeros((R, C), dtype=bool)
txt = [[" " for c in range(C)] for r in range(R)]

# set up text and boolean data matrix
for l in range(R):
  for c in range(len(lines[l])):
    M[l][c] = (lines[l][c] != " ")
    txt[l][c] = lines[l][c]

# some content indicates locations that would not be handled
# propperly with the cellular rules alone. Because only positive
# rules are applied (True never becomes False) I can help out by
# switching specific positions to True.
for r in range(R):

  ths = re.compile('Abgeordnete\(r\) +einschließlich').finditer(lines[r])
  if ths:
    for th in ths:
      th = th.span()
      for c in range(th[0],th[1]+1):
        M[r][c] = True
      if r+1 < R:
        M[r+1][th[1]] = True
      
  th = re.compile('Abgegebene Stimmen: +\d').search(lines[r])
  if th:
    th = th.span()
    for c in range(th[0],th[1]+1):
      M[r][c] = True  
      
  th = re.compile('Abgeordnete/r +ja +nein +enthalten +ungültig').search(lines[r])
  if th:
    th = th.span()
    for c in range(th[0],th[1]+1):
      M[r][c] = True
    
  ds = re.compile('\. \. \. +[0-9]').finditer(lines[r])
  for d in ds:
    d = d.span()
    for c in range(d[0],d[1]+1):
      M[r][c] = True
  
  th = re.compile('(Mündliche Frage \d)|(Anlage \d)|(Tagesordnungspunkt \d)').search(lines[r])
  if th:
    th = th.span()
    for c in range(th[0],th[1]+1):
      M[r][c] = True
    if r > 0:
      M[r-1][th[0]] = True

# apply cellular rules until stable state is reached
# the idea is explained on my web-site:
# http://www.joyofdata.de/blog/segmenting-text-document-using-idea-cellular-automata-text-mining/
altered = True
while altered:
  altered = False
  for r in range(R):
    for c in range(C):
      if not M[r][c]:
        if (
          (r > 0 and r < R-1 and M[r-1][c] and M[r+1][c])
          or (c > 0 and c < C-1 and M[r][c-1] and M[r][c+1])
          
          or (r > 0   and c > 0   and M[r-1][c] and M[r-1][c-1] and M[r][c-1])
          or (r > 0   and c < C-1 and M[r-1][c] and M[r-1][c+1] and M[r][c+1])
          or (r < R-1 and c > 0   and M[r+1][c] and M[r+1][c-1] and M[r][c-1])
          or (r < R-1 and c < C-1 and M[r+1][c] and M[r+1][c+1] and M[r][c+1])
          
          or (r > 0   and M[r-1][c] and M[r][randrange(C)])
          or (r < R-1 and M[r+1][c] and M[r][randrange(C)])
        ):
          M[r][c] = True
          altered = True

# output text with layout highlighted
f = open(layoutFile, encoding="utf-8", mode="w+")

for r in range(R):
  # copy by value:
  line = list(txt[r])
  for c in range(C):
    if M[r][c] and txt[r][c] == " ":
        line[c] = "-"
  f.write("".join(line)+'\n')

f.close()

f = open(longFile, encoding="utf-8", mode="w+")

# identify rectangles
for r in range(R):
  for c in range(C):
      if M[r][c] and (
           (r > 0  and c > 0  and not M[r][c-1] and not M[r-1][c] and not M[r-1][c-1])
        or (r > 0  and c == 0                   and not M[r-1][c]                    )
        or (r == 0 and c > 0  and not M[r][c-1]                                      )
        or (r == 0 and c == 0                                                        )
        ):
        for r2 in range(r,R):
          if M[r2][c] and (r2+1 == R or not M[r2+1][c]):
            break
        for c2 in range(c,C):
          if M[r2][c2] and (c2+1 == C or not M[r2][c2+1]):
            break
        
        f.write("\n%% NEW BLOCK %%\n")
        for i in range(r,r2+1):
          line = "".join(txt[i][c:(c2+1)])
          if len(line.strip()) > 0:
            f.write(line.strip()+"\n")

f.close()
