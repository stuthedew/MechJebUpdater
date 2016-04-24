import sys
from util import *
import requests

def main():

    repPath = config["LOCAL_BRANCH"]
    versionPath = repPath + "MechJeb2.version"

    remote = getJson(versionPath)


    u = requests.get(config["URL"]["UPSTREAM_VERSION"])
    upstreamVersion = parseMechJeb(u)
    remote = json.loads(requests.get(config["URL"]["REMOTE_VERSION"]).text)

    #print(upstreamVersion)
    uObj = VersionData(string=upstreamVersion)
    rObj = VersionData(d=remote["VERSION"])
    #testObj(uObj)
    #testObj(rObj)

    if(compareVersions(rObj, uObj) is False):
        tagCurrent(repPath)
        try:
            rStr = "{} is available. You currently have version {}".format(
                uObj.string, rObj.string)
            print(rStr)

            syncUpstream(repPath)
            updateVersionFile(versionPath, remote, uObj.dict)
            commitVersion(repPath, uObj.string)
            '''
            o = requests.get(config["URL"]["UPSTREAM_VERSION"])
            originVersion = parseMechJeb(o)
            origObj = VersionData(string=originVersion)

            if(compareVersions(uObj, origObj) is False):
                raise AssertionError("Fork ({}) did not update to current MechJeb2 version({})!!!".format(origObj.string, uObj.string))
            '''
            pushUpdate(repPath, uObj.string)
            removeTag(repPath)

        except Exception as e:
            print(e)
            rollbackCommit(repPath)
            sys.exit(1)

    else:
        print("You have the current version of MechJeb2 ({})".format(uObj.string))


if __name__ == '__main__':
    sys.exit(main())
