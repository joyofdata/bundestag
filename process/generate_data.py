import re
import json

jsonDelegatesFile = "F:\\git-repos\\bundestag\\data\\organizational\\BT18\\delegates.json"

f = open(jsonDelegatesFile, encoding="utf-8")
delegatesMap = json.load(f)
f.close()

data = open("F:/git-repos/bundestag/process/lastnames.txt", "w")

listOfChars = [
  "a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","","","","","",
  "","","","",""
]

listOfLastNames = []

for delegate in delegatesMap:
  for name in delegate["name"]:
    m = re.compile("([^,]+),([^,]+)").match(name)
    ln = m.group(1).strip().lower()
    fn = m.group(2).strip().lower()
    if(len(ln) >= 4):
      ln = re.compile("[éè]").sub("e",ln)
      ln = re.compile("[àá]").sub("a",ln)
      ln = re.compile("-").sub(" ",ln)
      ln = re.compile("[^a-zäöüß ]").sub("?",ln)
      listOfLastNames.append(ln)
      
listOfLastNames = list(set(listOfLastNames))
listOfLastNames.sort()

data.write("\n".join(listOfLastNames))