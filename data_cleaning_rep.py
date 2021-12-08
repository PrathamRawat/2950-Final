import pandas as pd

house = pd.read_csv("data/raw/all_transactions_house.csv")
legislators_current = pd.read_csv("data/raw/legislators-current.csv")
legislators_historical = pd.read_csv("data/raw/legislators-historical.csv")

legislators = legislators_historical.append(legislators_current)
legislators = legislators[
    ["last_name", "first_name", "middle_name", "gender", "type", "party", "state", "district", "senate_class"]]

representatives = legislators[legislators['type'] == "rep"]

representatives["name"] = pd.DataFrame.copy(representatives.apply(
    lambda r: "{}{}{}".format(r["first_name"], " " if pd.isna(r["middle_name"]) else " {} ".format(r["middle_name"][0]),
                              r["last_name"]), axis=1))

# senators.loc[senators["name"] == "Angus S King", "name"] = "Angus S King, Jr."

representatives["name"] = pd.DataFrame.copy(representatives.apply(
    lambda r: "{}{}{}".format(r["first_name"], " " if pd.isna(r["middle_name"]) else " {} ".format(r["middle_name"][0]),
                              r["last_name"]), axis=1))


def get_senator(name):
    if name == "Ladda Tammy Duckworth":
        name = "Tammy Duckworth"
    if name == "Michael  B Enzi":
        name = "Michael B Enzi"
    return indexed_representatives.loc[name]


indexed_representatives = representatives.set_index("name")
indexed_representatives["name"] = indexed_representatives.index
trading_representatives = house["representative"].apply(get_senator)
trading_representatives = trading_representatives.drop_duplicates().reset_index().drop("index", axis=1)

trading_representatives.to_csv("data/cleaned/representatives.csv")
