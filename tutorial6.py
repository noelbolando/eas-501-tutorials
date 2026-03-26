"""
    EAS 501 - Sustainable Urban Systems
    Tutorial 6
    Noel Boland
    3/26/2026
"""

# bring it allllll in
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd

from tutorial_5 import load_data, clean_data

# import carbon foodprint data
boston_foodprint = pd.read_excel("Boston_CF.xlsx", 0)
boston_foodprint["GEOID"] = boston_foodprint["GEOID"].astype(str)
#print(boston_foodprint.head())

# import population data
raw_population_df, raw_cal_cf_df, raw_cal_intake_df = load_data()
population_df, cal_cf_df, cal_intake_df = clean_data(raw_population_df, raw_cal_cf_df, raw_cal_intake_df)
population_df["GEOID"] = population_df["GEOID"].astype(str)
population_df["Total_Pop"] = population_df.sum(numeric_only=True, axis=1)
population_df = population_df.filter(["GEOID", "Total_Pop"])
#print(population_df)

# join population and foodprint dataframe based on GEOID
boston_foodprint = boston_foodprint.merge(population_df, on="GEOID")
boston_foodprint = boston_foodprint.drop(columns=[col for col in boston_foodprint.columns if col.startswith("Unnamed")])
#print(boston_foodprint.head())

# load in the Boston shapefile
boston = gpd.read_file("Census2020_BlockGroups/Census2020_BlockGroups.shp")
#print(boston.info())
# plot boston!
boston.plot(color="white", edgecolor="black")
plt.axis("off")
plt.title("Boston, Massachusetts")
plt.show()

# view per capita impacts of Boston
boston = boston.join(boston_foodprint.set_index("GEOID"), on="GEOID20")
print(boston)
boston["Per Capita"] = boston["Total"]/boston["Total_Pop"]
print(boston)
# view histogram
boston["Per Capita"].hist()
plt.title("Foodprint per Capita in Boston, MA")
plt.xlabel("Per Capita")
plt.ylabel("Counts")
plt.show()

# plot foodprint basic
boston.plot(
    column = "Per Capita",
    legend = True,
    scheme = "fisherjenks",
    missing_kwds={
        "color": "lightgrey",
        "label": "Missing values"
        },
    legend_kwds={
        "loc": "lower right"
    }
)
plt.title("Carbon Footprint Emissions per Capita in Boston, MA")
plt.axis("off")
plt.show()

# plot foodprin


