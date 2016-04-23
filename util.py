import json
import os
import re
import subprocess
from collections import OrderedDict


def getJson(path):
    with open(path) as f:
        j = json.loads(f.read())

    return j

os.chdir(os.path.dirname(__file__))
local_path = os.getcwd()
config = getJson(local_path + '/updater.config')


class VersionData:

    def __init__(self, d=None, string=None):
        self.string = None
        self.dict = OrderedDict.fromkeys(['MAJOR', 'MINOR', 'PATCH', 'BUILD'])

        if d is not None:
            self._loadDict(d)
            self.string = makeStr(self.dict)

        elif(string is not None):
            self.string = string
            self._loadDict(self._makeDict(self.string))

        else:
            raise Exception

    def _makeStr(self, d):
        return "{}.{}.{}.{}".format(
            d['MAJOR'],
            d['MINOR'],
            d['PATCH'],
            d['BUILD'])

    def _makeDict(self, str):
        s = str.split(".")

        _d = {"MAJOR": int(s[0]), "MINOR": int(
            s[1]), "PATCH": int(s[2]), "BUILD": int(s[3])}
        return _d

    def _loadDict(self, oldDict):
        for key in self.dict:
            self.dict[key] = oldDict[key]


def validateVersionFile(file):
    pass


def makeStr(d):
    return "{}.{}.{}.{}".format(
        d['MAJOR'],
        d['MINOR'],
        d['PATCH'],
        d['BUILD'])

def updateVersionFile(path, localData, newVersion):
    localData["VERSION"] = newVersion

    print(json.dumps(localData, sort_keys=False, indent=4, separators=(',', ': ')))
    try:
        with open(path, 'w') as f:
            json.dump(localData, f, sort_keys=False, indent=4,
                      separators=(',', ': '), ensure_ascii=False)
    except Exception as e:
        raise e

    print("Updated to {}!".format(makeStr(newVersion)))

def parseMechJeb(r):
    d = re.search("AssemblyFileVersion\((.*)\)]", r.text).group(1)
    return d.strip("\"")


def syncUpstream(repPath, version, lBranch="master", uBranch="MuMech"):

    subprocess.check_output(["git", "-C", repPath, "fetch", "upstream"])
    subprocess.check_output(["git", "-C", repPath, "checkout", lBranch])
    subprocess.check_output(
        ["git", "-C", repPath, "rebase", "upstream/" + lBranch])
    commitStr = "Updated to version {}!".format(version)
    subprocess.check_output(["git", "-C", repPath, "commit", "-m", commitStr])
    subprocess.check_output(["git", "-C", repPath, "push", "origin", lBranch])


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
