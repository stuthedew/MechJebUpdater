import sys
from util import *
import requests

def main():
    local = getJson('MechJeb2.version')

    r = requests.get(config["URL"]["REMOTE_VERSION"])
    remoteVersion = parseMechJeb(r)
    #local = json.loads(requests.get(config["URL"]["LOCAL_VERSION"]).text)

    #print(remoteVersion)

    rObj = VersionData(string=remoteVersion)
    lObj = VersionData(d=local["VERSION"])
    #testObj(rObj)
    #testObj(lObj)

    if(compareVersions(lObj, rObj) is False):

        repPath = config["LOCAL_BRANCH"]
        tagCurrent(repPath)
        try:
            rStr = "{} is available. You currently have version {}".format(
                rObj.string, lObj.string)
            print(rStr)
            versionPath = repPath + "/MechJeb2.version"
            syncUpstream(repPath)
            updateVersionFile(versionPath, local, rObj.dict)
            commitVersion(repPath, rObj.string)
            o = requests.get(config["URL"]["REMOTE_VERSION"])
            originVersion = parseMechJeb(o)
            origObj = VersionData(string=originVersion)


            if(compareVersions(rObj, origObj) is False):
                raise AssertionError("Fork ({}) did not update to current MechJeb2 version({})!!!".format(origObj.string, rObj.string))


            pushUpdate(repPath, lObj.string)

        except Exception as e:
            print(e)
            rollbackCommit(repPath)
            sys.exit(1)

    else:
        print("You have the current version of MechJeb2 ({})".format(lObj.string))


if __name__ == '__main__':
    sys.exit(main())
