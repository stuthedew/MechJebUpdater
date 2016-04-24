import sys
from util import *
import requests

def main():

    repPath = config["LOCAL_BRANCH"]
    versionPath = repPath + "MechJeb2.version"

    local = getJson(versionPath)


    u = requests.get(config["URL"]["UPSTREAM_VERSION"])
    upstreamVersion = parseMechJeb(u)
    remote = json.loads(requests.get(config["URL"]["REMOTE_VERSION"]).text)

    #print(upstreamVersion)
    lObj = VersionData(d=local["VERSION"])
    uObj = VersionData(string=upstreamVersion)
    rObj = VersionData(d=remote["VERSION"])
    #testObj(uObj)
    #testObj(rObj)

    if(compareVersions(lObj, uObj) is False):
        tagCurrent(repPath)
        try:
            rStr = "{} is available. You currently have version {} locally".format(
                uObj.string, lObj.string)
            print(rStr)

            syncUpstream(repPath)
            updateVersionFile(versionPath, remote, uObj.dict)


            '''
            o = requests.get(config["URL"]["UPSTREAM_VERSION"])
            originVersion = parseMechJeb(o)
            origObj = VersionData(string=originVersion)

            if(compareVersions(uObj, origObj) is False):
                raise AssertionError("Fork ({}) did not update to current MechJeb2 version({})!!!".format(origObj.string, uObj.string))
            '''

            commitVersion(repPath, uObj.string)
            removeTag(repPath)

        except Exception as e:
            print(e)
            rollbackCommit(repPath)
            sys.exit(1)

    else:
        print("You have the current version of MechJeb2 ({}) locally".format(uObj.string))

    try:
        if(compareVersions(uObj, rObj) is False):
            print("Updating remote to {}...".format(lObj.string)),
            pushUpdate(repPath, lObj.string)
            print("done!")

        else:
            print("You have the current version of MechJeb2 ({}) remotely".format(lObj.string))

    except Exception as e:
        print(e)
        sys.exit(1)



if __name__ == '__main__':
    sys.exit(main())
