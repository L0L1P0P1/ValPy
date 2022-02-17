import datetime
import pip._vendor.requests as requests
from VALauth import VALauth
from VALstore import VALstore

def VALpy():

    session = requests.session()
    ValAuth = VALauth("L0L4P0P4", "mina1343")
    userid, headers = ValAuth.authenticate()
    ValStore = VALstore(userid, headers, 'eu')
    ValStore.GetStore()




if  __name__ == "__main__":
    VALpy()
