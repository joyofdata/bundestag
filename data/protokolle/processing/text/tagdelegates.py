import json

jsonDelegatesFile = "F:\\git-repos\\bundestag\\data\\organizational\\BT18\\delegates.json"

f = open(jsonDelegatesFile, encoding="utf-8")
delegatesMap = json.load(f)
f.close()

for delegate in delegatesMap:
  for name in delegate["name"]:
    m = re.compile("([^,]+),([^,]+)").match("b, a")
    ln = m.group(1).strip()
    fn = m.group(2).strip()