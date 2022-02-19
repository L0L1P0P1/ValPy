import pip._vendor.requests as requests
from collections import OrderedDict
import re
import socket

class VALauth:

    def __init__(self, username, password):
        self.username = str(username)
        self.password = str(password)

    def authenticate(self):

        # gets address info with "socket"
        addrinfo = socket.getaddrinfo('auth.riotgames.com', 443)
        (family, type, proto, canonname, (address, port)) = addrinfo[0]

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

        r = session.post(f'https://{address}/api/v1/authorization', json=data, headers=headers, verify=False)

        # Auth Request
        data = {
            'type': 'auth',
            'username': self.username,
            'password': self.password
        }
        r = session.put(f'https://{address}/api/v1/authorization', json=data, headers=headers, verify=False)
        if r.json()['data']['type'] == "multifactor":
            email = r.json()['data']['multifactor']['email']
            code = input(f'Please Enter The Code Sent to {email}: ')
            data = {
                "type": "multifactor",
                "code": code,
                "rememberDevice": False
            }
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
        user_id = r.json()['sub']
        # print('User ID: ' + user_id)
        headers['X-Riot-Entitlements-JWT'] = entitlements_token
        del headers['Host']
        session.close()
        return user_id, headers
