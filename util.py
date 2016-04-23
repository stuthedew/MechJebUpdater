import re
import json
import subprocess

class VersionData:
    string = None
    dict = None

    def __init__(self, dict=None, string=None):
        if dict is not None:
            self.dict = dict
            self.string = self._makeStr(self.dict)

        elif(string is not None):
            self.string = string
            self.dict = self._makeDict(self.string)

    def _makeStr(self, d):
        return "{}.{}.{}.{}".format(
            d['MAJOR'],
            d['MINOR'],
            d['PATCH'],
            d['BUILD'])

    def _makeDict(self, str):
        s = str.split(".")
        d = {"MAJOR": int(s[0]), "MINOR" : int(s[1]), "PATCH": int(s[2]), "BUILD": int(s[3])}
        return d

def validateVersionFile(file):
    pass


def parseMechJeb(r):
    d = re.search("AssemblyFileVersion\((.*)\)]", r.text).group(1)
    return d.strip("\"")


def syncUpstream(local_path, lBranch="master", uBranch="MuMech"):
    bString = "git -C " + local_path + " fetch " + uBranch
    subprocess.run(bString, shell=True)
    bString = "git -C " + local_path + " checkout "  + lBranch
    subprocess.run(bString, shell=True)
    bString = "git -C " + local_path + " rebase " + uBranch + "/" + lBranch
    subprocess.run(bString, shell=True)
    bString = "git -C " + local_path + " push origin " + lBranch
    subprocess.run(bString, shell=True)

def compareVersions(local, remote):
    if(local.dict == remote.dict):
        print("You have the current version of MechJeb2 ({})".format(remote.string))
        return True
    else:
        rStr = "{} is available. You currently have version {}".format(
            remote.string, local.string)
        print(rStr)
        return False

def testObj(t):
    print("Testing {}".format(t))
    print(t.string)
    print(t.dict)


def getJson(path):
    with open(path) as f:
        j = json.loads(f.read())

    return j
