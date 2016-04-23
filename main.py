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
        versionPath = repPath + "/MechJeb2.version"
        updateVersionFile(versionPath, local, rObj.dict)
        commitVersion(repPath, rObj.string)
        syncUpstream(repPath)


if __name__ == '__main__':
    sys.exit(main())
