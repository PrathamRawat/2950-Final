import pandas as pd

senate = pd.read_csv("data/raw/all_transactions.csv")  # senate

senate = senate.loc[senate.asset_type == "Stock"].loc[senate.ticker != "--"].dropna()
senate = senate.drop(columns=["ptr_link", "asset_type", "disclosure_date", "asset_description"])

senate["transaction_date"] = pd.to_datetime(senate["transaction_date"])
senate['transaction_year'] = pd.DatetimeIndex(senate['transaction_date']).year
senate['transaction_month'] = pd.DatetimeIndex(senate['transaction_date']).month
senate['transaction_day'] = pd.DatetimeIndex(senate['transaction_date']).day
senate.sort_values("transaction_date", ascending=False).head()

senate["amount_lower"] = pd.to_numeric(
    senate["amount"].replace("Over ", "", regex=True).replace("\$", "", regex=True).replace(" -.*$", "",
                                                                                            regex=True).replace(",", "",
                                                                                                                regex=True))
senate["amount_upper"] = pd.to_numeric(
    senate["amount"].replace("Over ", "", regex=True).replace(".* - ", "", regex=True).replace("\$", "",
                                                                                               regex=True).replace(",",
                                                                                                                   "",
                                                                                                                   regex=True))

senate.to_csv("data/cleaned/all_transactions_senate.csv")

house = pd.read_csv("data/raw/all_transactions_house.csv")  # house

house = house.drop([1956, 3381, 8975, 8976])

house = house.loc[house.ticker != "--"].dropna()
house = house.drop(columns=["ptr_link", "disclosure_date", "disclosure_year", "asset_description"])

house['transaction_date'] = pd.to_datetime(house['transaction_date'])
house['transaction_year'] = pd.DatetimeIndex(house['transaction_date']).year
house['transaction_month'] = pd.DatetimeIndex(house['transaction_date']).month
house['transaction_day'] = pd.DatetimeIndex(house['transaction_date']).day
house["amount_lower"] = pd.to_numeric(
    house["amount"].replace("Over ", "", regex=True).replace("\$", "", regex=True).replace(" -.*$", "",
                                                                                           regex=True).replace(",", "",
                                                                                                               regex=True))
house["amount_upper"] = pd.to_numeric(
    house["amount"].replace("Over ", "", regex=True).replace("-$", "- 0", regex=True).replace(".* - ", "",
                                                                                              regex=True).replace("\$",
                                                                                                                  "",
                                                                                                                  regex=True).replace(
        ",", "", regex=True))

house.to_csv("data/cleaned/all_transactions_house.csv")

legislators_current = pd.read_csv("data/raw/legislators-current.csv")
legislators_historical = pd.read_csv("data/raw/legislators-historical.csv")

legislators = legislators_historical.append(legislators_current)
legislators = legislators[
    ["last_name", "first_name", "middle_name", "gender", "type", "party", "state", "district", "senate_class"]]

senators = legislators[legislators['type'] == "sen"]
representatives = legislators[legislators['type'] == "rep"]

senators["name"] = pd.DataFrame.copy(senators.apply(
    lambda r: "{}{}{}".format(r["first_name"], " " if pd.isna(r["middle_name"]) else " {} ".format(r["middle_name"][0]),
                              r["last_name"]), axis=1))

senators.loc[senators["name"] == "Angus S King", "name"] = "Angus S King, Jr."
senators.loc[senators["name"] == "Tommy H Tuberville", "name"] = "Thomas H Tuberville"
senators.loc[senators["name"] == "Bill F Hagerty", "name"] = "William F Hagerty, Iv"
senators.loc[senators["name"] == "Mitch McConnell", "name"] = "A. Mitchell Mcconnell, Jr."
senators.loc[senators["name"] == "Jerry Moran", "name"] = "Jerry Moran,"
senators.loc[senators["name"] == "Ron Wyden", "name"] = "Ron L Wyden"
senators.loc[senators["name"] == "Dan Sullivan", "name"] = "Daniel S Sullivan"
senators.loc[senators["name"] == "Jacky Rosen", "name"] = "Jacklyn S Rosen"
senators.loc[senators["name"] == "Bill Cassidy", "name"] = "William Cassidy"
senators.loc[senators["name"] == "Timothy Kaine", "name"] = "Timothy M Kaine"
senators.loc[senators["name"] == "David Perdue", "name"] = "David A Perdue , Jr"
senators.loc[senators["name"] == "Tina F Smith", "name"] = "Tina Smith"
senators.loc[senators["name"] == "Ted Cruz", "name"] = "Rafael E Cruz"
senators.loc[senators["name"] == "Tom S Udall", "name"] = "Thomas Udall"
senators.loc[senators["name"] == "Thom Tillis", "name"] = "Thomas R Tillis"
senators.loc[senators["name"] == "Robert P Casey", "name"] = "Robert P Casey, Jr."
senators.loc[senators["name"] == "Joe Manchin", "name"] = "Joseph Manchin, Iii"

representatives["name"] = pd.DataFrame.copy(representatives.apply(
    lambda r: "{}{}{}".format(r["first_name"], " " if pd.isna(r["middle_name"]) else " {} ".format(r["middle_name"][0]),
                              r["last_name"]), axis=1))


def get_senator(name):
    if name == "Ladda Tammy Duckworth":
        name = "Tammy Duckworth"
    if name == "Michael  B Enzi":
        name = "Michael B Enzi"
    return indexed_senators.loc[name]


indexed_senators = senators.set_index("name")
indexed_senators["name"] = indexed_senators.index
trading_senators = senate["senator"].apply(get_senator)
trading_senators = trading_senators.drop_duplicates()
trading_senators = trading_senators.reset_index()
trading_senators = trading_senators.drop("index", axis=1)

trading_senators.to_csv("data/cleaned/senators.csv")