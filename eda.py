from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import pandas as pd

# postgresql+psycopg2://postgres:@localhost/epi

# the `create_engine` function prepares a connection to the database
# should this info be public? 
engine = create_engine('postgresql+psycopg2://postgres:Silvana1005.@localhost:5432/epi')

# this object will automatically map our db entity into a Python class
Base = automap_base()

# get db into automapper
Base.prepare(engine, reflect=True)

# save classes as variables, prepare classes
epi_country = Base.classes.epi_country

# query our database (pull data and save into objects)
session = Session(engine)

rows = session.query(epi_country.country, epi_country.geo_subregion, epi_country.water_h, epi_country.forestry).all()

epi_df = pd.DataFrame(rows, columns=["Country", "geo_subregion", "water_h", "forestry"])


hdi_df = pd.read_csv("./HDI.csv")

#load the data contained in hdi dataframe to postgres
hdi_df.to_sql("hdi", engine)

#filter America
epi_am = epi_df[(epi_df["geo_subregion"] == "South America") | (epi_df["geo_subregion"] == "North America")]

#merge epi data and hdi
epi_hdi = pd.merge(epi_am, hdi_df, on="Country")

#clean data
epi_hdi.dropna(inplace=True)

#plot water_h by Country
epi_hdi.plot.bar(x="Country", y="water_h")

#plot forestry by Country
epi_hdi.plot.bar(x="Country", y="forestry")

#plot water_h and Life expectancy at birth Male
epi_hdi.plot.scatter(x='water_h', y='Life expectancy at birth Male', c='DarkBlue')

#plot water_h and Life expectancy at birth Female
epi_hdi.plot.scatter(x='water_h', y='Life expectancy at birth Female', c='DarkBlue')

