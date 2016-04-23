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
        syncUpstream(config["LOCAL_BRANCH"])
        updateVersionFile(config["LOCAL_VERSION"], local, rObj.dict) #TODO: Update version file


if __name__ == '__main__':
    sys.exit(main())
