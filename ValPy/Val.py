import datetime
import socket
import json
import pip._vendor.requests as requests
import re
from collections import OrderedDict
import urllib3


urllib3.disable_warnings()
class ValPy:

    def __init__(self):
        regions = ['eu', 'na', 'ap', 'ko']
        r = requests.get('https://valorant-api.com/v1/version')
        self.version = r.json()['data']
        self.authenticated = False

    def Authenticate(self, username, password, region):
        self.region = str(region).lower()
        self.username = str(username)
        self.password = str(password)

        if self.region.count(self.region) == 0:
            print('Invalid Region!')
            return 0
      
        if self.authenticated == False:

            # gets address info with "socket"
#            addrinfo = socket.getaddrinfo('auth.riotgames.com', 443)
#            (family, type, proto, canonname, (address, port)) = addrinfo[0]
            address = 'auth.riotgames.com'

            # Headers
            headers = OrderedDict({
                'Accept-Encoding': 'gzip, deflate, br',
                'Host': "auth.riotgames.com",
                'User-Agent': 'RiotClient/43.0.1.4195386.4190634 rso-auth (Windows;10;;Professional, x64)'
            })

            session = requests.session()
            session.headers = headers

            # Auth Cookies
            data = {
                'client_id': 'play-valorant-web-prod',
                'nonce': '1',
                'redirect_uri': 'https://playvalorant.com/opt_in',
                'response_type': 'token id_token',
            }

            r = session.post(f'https://{address}/api/v1/authorization', json=data, headers=headers)

            # Auth Request
            data = {
                'type': 'auth',
                'username': self.username,
                'password': self.password
            }
            r = session.put(f'https://{address}/api/v1/authorization', json=data, headers=headers)
            # 2 FAC
            if r.json()['type'] == "multifactor":
                email = r.json()['multifactor']['email']
                code = input(f'Please Enter The Code Sent to {email}: ')
                data = {
                    "type": "multifactor",
                    "code": code,
                    "rememberDevice": False
                }
                r = session.put(f'https://{address}/api/v1/authorization', json=data, headers=headers)
        
            pattern = re.compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
            data = pattern.findall(r.json()['response']['parameters']['uri'])[0] 
            access_token = data[0]
            
            # Entitlement
            headers = {
                'Accept-Encoding': 'gzip, deflate, br',
                'Host': "entitlements.auth.riotgames.com",
                'User-Agent': 'RiotClient/43.0.1.4195386.4190634 rso-auth (Windows;10;;Professional, x64)',
                'Authorization': f'Bearer {access_token}',
            }
            r = session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={})
            entitlements_token = r.json()['entitlements_token']
            # print('Entitlements Token: ' + entitlements_token)

            # Player Info
            headers = {
                'Accept-Encoding': 'gzip, deflate, br',
                'Host': "auth.riotgames.com",
                'User-Agent': 'RiotClient/43.0.1.4195386.4190634 rso-auth (Windows;10;;Professional, x64)',
                'Authorization': f'Bearer {access_token}',
            }

            r = session.post('https://auth.riotgames.com/userinfo', headers=headers, json={})
            userid = r.json()['sub']
            # print('User ID: ' + user_id)
            headers['X-Riot-Entitlements-JWT'] = entitlements_token
            del headers['Host']
            session.close()
            self.userid = userid
            self.headers = headers
            self.authenticated = True
        else:
            print('Authenticated already! Please create a new Object!')

    def GetVersion(self):
        return self.version

    def GetStore(self):
        if self.authenticated == False:
            print('Not Authenticated!, Use <classname>.Authenticate(<username>, <password>, <region>) first!')
            return 0

        r = requests.get(f'https://pd.{self.region}.a.pvp.net/store/v2/storefront/{self.userid}', headers=self.headers)
        r = json.dumps(r.json())
        return r

    def GetStoreJSON(self):
        if self.authenticated == False:
            print('Not Authenticated!, Use <classname>.Authenticate(<username>, <password>, <region>) first!')
            return 0

        r = requests.get(f'https://pd.{self.region}.a.pvp.net/store/v2/storefront/{self.userid}', headers=self.headers)
        r = r.json()
        return r
        
    def FetchWeapons(self):
        r = requests.get('https://valorant-api.com/v1/weapons')
        r = json.dumps(r.json()['data'])
        return r

    def FetchWeaponsJSON(self):
        r = requests.get('https://valorant-api.com/v1/weapons')
        r = r.json()['data']
        return r



