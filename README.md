Added 02/26/2023 for EPI vs HDI Lab.

I contrasted the "% of Employment in Agriculture" and the "% Employment in Services" variables. There is no available
information for countries as the US or Russia. However, for the rest of countries, is interesting how some of them
have a high percentage of employment in agriculture or services. This can give an idea of how those type of economies
can affect other economic or social variables.

I used the total population variable to easily see how big can be the population in certain countries as China and India.

In the fourth chart I related the "Avg. Child malnutrinion stunting" with the "Life expectancy" variables. It shows that
the higher is the child malnutrition, the lower is the life expectancy.

End of 02/26/2023 comments.



# epi-hdi

# eda.py was included as required and eda.ipynb to test and save plots.
# HDI.csv contains Human Development Indicators

# Libraries used to solve the requirenments

from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import pandas as pd



# postgresql+psycopg2://postgres:@localhost/epi

# the `create_engine` function prepares a connection to the database
# should this info be public? 
engine = create_engine('postgresql+psycopg2://postgres:<password>.@localhost:5432/epi')

# this object will automatically map our db entity into a Python class
Base = automap_base()

# get db into automapper
Base.prepare(engine, reflect=True)

# save classes as variables, prepare classes
epi_country = Base.classes.epi_country

# query our database (pull data and save into objects)
session = Session(engine)

# retrieve data from postgres database, epi_country table
rows = session.query(epi_country.country, epi_country.geo_subregion, epi_country.water_h, epi_country.forestry).all()

# create a DataFrame (Pandas)
epi_df = pd.DataFrame(rows, columns=["Country", "geo_subregion", "water_h", "forestry"])

# create a DataFrame from HDI.csv file
hdi_df = pd.read_csv("./HDI.csv")

# load the data contained in hdi dataframe to postgres
#hdi_df.to_sql("hdi", engine)

# filter countries from America
epi_am = epi_df[(epi_df["geo_subregion"] == "South America") | (epi_df["geo_subregion"] == "North America")]

# merge epi data and hdi
epi_hdi = pd.merge(epi_am, hdi_df, on="Country")

# clean the data frame
epi_hdi.dropna(inplace=True)

# plot water_h by Country
epi_hdi.plot.bar(x="Country", y="water_h")

# plot forestry by Country
epi_hdi.plot.bar(x="Country", y="forestry")

# plot water_h and Life expectancy at birth Male
epi_hdi.plot.scatter(x='water_h', y='Life expectancy at birth Male', c='DarkBlue')

# plot water_h and Life expectancy at birth Female
epi_hdi.plot.scatter(x='water_h', y='Life expectancy at birth Female', c='DarkBlue')

# findings
# scatter plots for Male and Female, show that Life expentancy is affecting more Female than Male population

