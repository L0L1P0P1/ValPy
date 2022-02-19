import datetime
import pip._vendor.requests as requests
from VALauth import VALauth
from VALstore import VALstore


class VALpy:
    def __init__(self, userid, headers):
        r = requests.get('https://valorant-api.com/v1/version')
        self.version = r.json()        
        self.headers = {"X-Riot-ClientPlatform": "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9",
                        "X-Riot-ClientVersion": self.version['data']['riotClientVersion']}
        self.headers['Authorization'] = headers['Authorization']
        self.headers['X-Riot-Entitlements-JWT'] = headers['X-Riot-Entitlements-JWT']

    def GetVersion(self):
        return self.version

    def FetchWeapons(self):
        r = requests.get('https://valorant-api.com/v1/weapons',verify=False)
        weapons = open('weapons.txt', 'w')
        weapons.write(r.text)
        weapons.close()
        return r.text




if  __name__ == "__main__":

    ValAuth = VALauth("The0Rand0m", "Kayoun1388$")
    userid, headers = ValAuth.authenticate()
#    VAL = VALpy(userid, headers)
#    VAL.FetchWeapons()
    valstore = VALstore(userid, headers, 'eu')
    valstore.GetStore()
    


