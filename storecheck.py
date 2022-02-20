from ValPy import Val


def main():
    username = input("Enter Account Username: ")
    password = input("Enter Account Password: ")
    region = input("Enter Account Region: ")

    val = Val.ValPy()
    val.Authenticate(username, password, region)
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