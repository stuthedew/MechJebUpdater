import sys
from util import *
import requests

def main():

    config = getJson('updater.config')
    local = getJson('MechJeb2.version')

    r = requests.get(config["URL"]["REMOTE_VERSION"])
    remoteVersion = parseMechJeb(r)
    local = json.loads(requests.get(config["URL"]["LOCAL_VERSION"]).text)

    #print(remoteVersion)
    pass
    rObj = VersionData(string=remoteVersion)
    lObj = VersionData(dict=local["VERSION"])
    #testObj(rObj)
    #testObj(lObj)
    if(compareVersions(lObj, rObj) is False):
        syncUpstream(config["LOCAL_PATH"])


if __name__ == '__main__':
    sys.exit(main())
