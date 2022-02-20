from ValPy import Val


def main():
    val = Val.ValPy()
    val.Authenticate('L0L4P0P4', 'mina1343', 'eu')
    store = val.GetStoreJSON()
    weapons = val.FetchWeaponsJSON()

    itemindex = 0
    weaponindex = 0
    skinindex = 0
    storeskin = []

    for i in store["SkinsPanelLayout"]["SingleItemOffers"]:
        for w in weapons:
            for s in w["skins"]:
#                print(s["displayName"])
                if i == s["levels"][0]["uuid"]:
                    storeskin.append(s["displayName"])

    print(storeskin)






if __name__ == '__main__':
    main()