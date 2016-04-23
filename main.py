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
            versionPath = repPath + "/MechJeb2.version"
            syncUpstream(repPath)
            updateVersionFile(versionPath, local, rObj.dict)
            commitVersion(repPath, rObj.string)
            o = requests.get(config["URL"]["REMOTE_VERSION"])
            originVersion = parseMechJeb(o)
            origObj = VersionData(string=originVersion)


            if(compareVersions(rObj, originVersion)):
                raise AssertionError("Fork ({}) did not update to current MechJeb2 version({})!!!".format(rObj.string, originVersion.string))

            pushUpdate(repPath)

        except Exception as e:
            print(e)
            rollbackCommit(repPath)

        finally:
            pass




if __name__ == '__main__':
    sys.exit(main())
