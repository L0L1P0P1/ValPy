from ValPy import Val


def main():

    val.Authenticate('YOUR USERNAME', 'YOUR PASSWORD', 'YOUR ACCOUNT REGION')
    val = Val.ValPy() 
    
    store = val.GetStoreJSON()
    weapons = val.FetchWeaponsJSON()
    storeskin = []

    for i in store["SkinsPanelLayout"]["SingleItemOffers"]:
        for w in weapons:
            for s in w["skins"]:
                if i == s["levels"][0]["uuid"]:
                    storeskin.append(s["displayName"])

    print(storeskin)






if __name__ == '__main__':
    main()