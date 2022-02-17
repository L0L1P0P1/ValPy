import pip._vendor.requests as requests
from collections import OrderedDict
import re
import socket

class VALstore:

    def __init__(self, userid, headers, region):
        self.userid = userid
        self.headers = headers
        self.region = region

    def GetStore(self):
        session = requests.session()
        session.headers = self.headers

        r = session.get(f'https://pd.{self.region}.a.pvp.net/store/v2/storefront/{self.userid}', verify=False)
        print(r.text)



















        