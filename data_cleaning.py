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
house["amount_lower"] = pd.to_numeric( house["amount"].replace("Over ", "", regex=True).replace("\$", "", regex=True).replace(" -.*$", "", regex=True).replace(",", "", regex=True))
house["amount_upper"] = pd.to_numeric( house["amount"].replace("Over ", "", regex=True).replace("-$", "- 0", regex=True).replace(".* - ", "", regex=True).replace("\$", "", regex=True).replace( ",", "", regex=True))

house["representative"] = house["representative"].str.split(" ", 1).str[1]

house.to_csv("data/cleaned/all_transactions_house.csv")

legislators_current = pd.read_csv("data/raw/legislators-current.csv")
legislators_historical = pd.read_csv("data/raw/legislators-historical.csv")

legislators = legislators_historical.append(legislators_current)
legislators = legislators[["last_name", "first_name", "middle_name", "gender", "type", "party", "state", "district", "senate_class"]]

senators = legislators[legislators['type'] == "sen"]
representatives = legislators[(legislators['type'] == "rep") | ((legislators["first_name"] == "Roger") & (legislators["last_name"] == "Marshall"))]

senators["name"] = pd.DataFrame.copy(senators.apply(lambda r: "{}{}{}".format(r["first_name"], " " if pd.isna(r["middle_name"]) else " {} ".format(r["middle_name"][0]), r["last_name"]), axis=1))

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

representatives["name"] = pd.DataFrame.copy(representatives.apply( lambda r: "{}{}{}".format(r["first_name"], " " if pd.isna(r["middle_name"]) else " {} ".format(r["middle_name"]), r["last_name"]), axis=1))

representatives.loc[representatives["name"] == "Abigail Davis Spanberger", "name"] = "Abigail Spanberger"
representatives.loc[representatives["name"] == "Andrew R. Garbarino", "name"] = "Andrew Garbarino"
representatives.loc[representatives["name"] == "Anthony Gonzalez", "name"] = "Anthony E. Gonzalez"
representatives.loc[representatives["name"] == "Ashley Hinson", "name"] = "Ashley Hinson Arenholz"
representatives.loc[representatives["name"] == "Barry Moore", "name"] = "Felix Barry Moore"
representatives.loc[representatives["name"] == "Bill J. Pascrell", "name"] = "Bill Pascrell"
representatives.loc[representatives["name"] == "Blake David Moore", "name"] = "Blake Moore"
representatives.loc[representatives["name"] == "Bradley Scott Schneider", "name"] = "Bradley S. Schneider"
representatives.loc[representatives["name"] == "Brian J. Mast", "name"] = "Brian Mast"
representatives.loc[representatives["name"] == "Brian M. Higgins", "name"] = "Brian Higgins"
representatives.loc[representatives["name"] == "C. Scott Franklin", "name"] = "Scott Franklin"
representatives.loc[representatives["name"] == "Carol D. Miller", "name"] = "Carol Devine Miller"
representatives.loc[representatives["name"] == "Charles J. Fleischmann", "name"] = 'Charles J. "Chuck" Fleischmann'
representatives.loc[representatives["name"] == "Chris Jacobs", "name"] = "Christopher L. Jacobs"
representatives.loc[representatives["name"] == "Dan Crenshaw", "name"] = "Daniel Crenshaw"
representatives.loc[representatives["name"] == "David J. Trone", "name"] = "David Trone"
representatives.loc[representatives["name"] == "David Rouzer", "name"] = "David Cheston Rouzer"
representatives.loc[representatives["name"] == "Deborah Koff Ross", "name"] = "Deborah K. Ross"
representatives.loc[representatives["name"] == "Donna E. Shalala", "name"] = "Donna Shalala"
representatives.loc[representatives["name"] == "Earl L. Carter", "name"] = "Earl Leroy Carter"
representatives.loc[representatives["name"] == "Elaine G. Luria", "name"] = "Elaine Luria"
representatives.loc[representatives["name"] == "Frank J. Pallone", "name"] = "Frank Pallone"
representatives.loc[representatives["name"] == "Fred Stephen Upton", "name"] = "Fred Upton"
representatives.loc[representatives["name"] == "Gilbert Ray Cisneros", "name"] = "Gilbert Cisneros"
representatives.loc[representatives["name"] == "Harley Rouda", "name"] = "Harley E. Rouda"
representatives.loc[representatives["name"] == "Harold Rogers", "name"] = "Harold Dallas Rogers"
representatives.loc[representatives["name"] == "J. French Hill", "name"] = "James French Hill"
representatives.loc[representatives["name"] == "Jim Hagedorn", "name"] = "James Hagedorn"
representatives.loc[representatives["name"] == "John H. Rutherford", "name"] = "John Rutherford"
representatives.loc[representatives["name"] == "John R. Curtis", "name"] = "John Curtis"
representatives.loc[representatives["name"] == "Judy M. Chu", "name"] = "Judy Chu"
representatives.loc[representatives["name"] == "Kathy Ellen Manning", "name"] = "Kathy Manning"
representatives.loc[representatives["name"] == "Kenny Ewell Marchant", "name"] = "Kenny Marchant"
representatives.loc[representatives["name"] == "Kevin R. Hern", "name"] = "Kevin Hern"
representatives.loc[representatives["name"] == "Linda T. Sánchez", "name"] = "Linda T. Sanchez"
representatives.loc[representatives["name"] == "Lloyd A. Doggett", "name"] = "Lloyd Doggett"
representatives.loc[representatives["name"] == "Lloyd Smucker", "name"] = "Lloyd K. Smucker"
representatives.loc[representatives["name"] == "Michael Guest", "name"] = "Michael Patrick Guest"
representatives.loc[representatives["name"] == "Mike Gallagher", "name"] = "Michael John Gallagher"
representatives.loc[representatives["name"] == "Mike Garcia", "name"] = "Michael Garcia"
representatives.loc[representatives["name"] == "Patrick Edward Fallon", "name"] = "Patrick Fallon"
representatives.loc[representatives["name"] == "Pete A. Sessions", "name"] = "Pete Sessions"
representatives.loc[representatives["name"] == "Peter James Meijer", "name"] = "Peter Meijer"
representatives.loc[representatives["name"] == "Raja Krishnamoorthi", "name"] = "S. Raja Krishnamoorthi"
representatives.loc[representatives["name"] == "Rick W. Allen", "name"] = "Richard W. Allen"
representatives.loc[representatives["name"] == "Ro Khanna", "name"] = "Rohit Khanna"
representatives.loc[representatives["name"] == "Robert C. Scott", "name"] = 'Robert C. "Bobby" Scott'
representatives.loc[representatives["name"] == "Roger Marshall", "name"] = "Roger W. Marshall"
representatives.loc[representatives["name"] == "Stephanie I. Bice", "name"] = "Stephanie Bice"
representatives.loc[representatives["name"] == "Steve J. Chabot", "name"] = "Steve Chabot"
representatives.loc[representatives["name"] == "TJ Cox", "name"] = "TJ John (Tj) Cox"
representatives.loc[representatives["name"] == "Thomas R. Suozzi", "name"] = "Thomas Suozzi"
representatives.loc[representatives["name"] == "Tom O’Halleran", "name"] = "Tom O'Halleran"
representatives.loc[representatives["name"] == "Van Taylor", "name"] = "Nicholas Van Taylor"

representatives.loc[representatives["name"] == "W. Gregory Steube", "name"] = "Greg Steube"
representatives.loc[representatives["name"] == "Mark E. Green", "name"] = "Mark Green"
representatives.loc[representatives["name"] == "Jim Banks", "name"] = "James E. Banks"
representatives.loc[representatives["name"] == "Donald S. Beyer", "name"] = "Donald Sternoff Beyer"

house.loc[house["representative"] == "W. Greg Steube"] = "Greg Steube"
house.loc[house["representative"] == "Neal Patrick Dunn MD, FACS"] = "Neal P. Dunn"
house.loc[house["representative"] == "Neal Patrick MD, FACS Dunn"] = "Neal P. Dunn"
house.loc[house["representative"] == "Neal Patrick MD, Facs Dunn"] = "Neal P. Dunn"
house.loc[house["representative"] == "Mark Dr Green"] = "Mark Green"
house.loc[house["representative"] == "James E Hon Banks"] = "James E. Banks"
house.loc[house["representative"] == "Donald Sternoff Honorable Beyer"] = "Donald Sternoff Beyer"

def get_senator(name):
    if name == "Ladda Tammy Duckworth":
        name = "Tammy Duckworth"
    if name == "Michael  B Enzi":
        name = "Michael B Enzi"
    return indexed_senators.loc[name]

def get_rep(name):
    return indexed_representatives.loc[name]

indexed_senators = senators.set_index("name")
indexed_senators["name"] = indexed_senators.index
trading_senators = senate["senator"].apply(get_senator)
trading_senators = trading_senators.drop_duplicates()
trading_senators = trading_senators.reset_index()
trading_senators = trading_senators.drop("index", axis=1)

trading_senators.to_csv("data/cleaned/senators.csv")

indexed_representatives = representatives.set_index("name")
indexed_representatives["name"] = indexed_representatives.index
trading_representatives = house["representative"].apply(get_rep)
trading_representatives = trading_representatives.drop_duplicates()
trading_representatives = trading_representatives.reset_index()
trading_representatives = trading_representatives.drop("index", axis=1)

trading_representatives.to_csv("data/cleaned/representatives.csv")
