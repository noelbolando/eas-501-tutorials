"""
    EAS 501 - Sustainable Urban Systems
    Tutorial 3
    Noel Boland
    3/12/2026
"""

# import libraries and stuff
import matplotlib.pyplot as plt
import openpyxl as opxl
import pandas as pd

# import population data
population_data = pd.read_csv("BostonPopulation_T4.csv")
print(population_data)
print(population_data.head())
print(population_data["Females (31-50)"])

# import carbon footprint data
carbon_footprint_data = pd.read_csv("CaloricCF.txt", delimiter="\t")
print(carbon_footprint_data.head())

# import carloric intake data
caloric_intake_data = pd.read_excel("CaloricIntake.xlsx", 0)
print(caloric_intake_data.head())

# inspect the population data
print(population_data.tail())
# check the dtype of GEOID
print(population_data["GEOID"].dtype)
# change the dtype of the GEOID
population_data["GEOID"] = population_data["GEOID"].astype(str)
# check the dtype of GEOID
print(population_data["GEOID"].dtype)
# show all the dtypes in the population data
print(population_data.dtypes)

# loopin'
for row in population_data.iterrows():
    population = row[1]["Males (9-13)"]
    if pd.isna(population):
        print(row[0])
# one-liner to drop the rows with null values
population_data = population_data.dropna(subset=["Males (9-13)"])
# change the dytpe of this data to int
population_data["Males (9-13)"] = population_data["Males (9-13)"].astype(int)
print(population_data)

# reload the boston data
population_data = pd.read_csv("BostonPopulation_T4.csv")
# replace the string "Null" with NaN, then drop all rows containing NaN
population_data = population_data.replace("Null", pd.NA).dropna()
# drop duplicate rows
population_data = population_data.drop_duplicates()
print(population_data)

# do some calculations!
# convert all population columns to numeric (they may have been read as strings after replacing "Null")
population_columns = [c for c in population_data.columns if c != "GEOID"]
population_data[population_columns] = population_data[population_columns].apply(pd.to_numeric)

# stats on Males (31-50)
col = population_data["Males (31-50)"]
print(f"Males (31-50) mean:  {col.mean():.2f}")
print(f"Males (31-50) max:   {col.max()}")
print(f"Males (31-50) stdev: {col.std():.2f}")

# boolean logic: flag tracts where BOTH working-age male AND female populations
# exceed their respective column means (i.e. high-population working-age tracts)
male_mean   = population_data["Males (31-50)"].mean()
female_mean = population_data["Females (31-50)"].mean()

high_pop = (
    (population_data["Males (31-50)"]   > male_mean) &
    (population_data["Females (31-50)"] > female_mean)
)

population_data["high_working_age"] = high_pop
print(f"\nTracts with above-average working-age pop (31-50, both sexes): {high_pop.sum()}")
print(population_data[["GEOID", "Males (31-50)", "Females (31-50)", "high_working_age"]].head(10))

# make basic graphs with matplotlib
population_data["Females (31-50)"].hist()
plt.title("Population Data: Females (31-50)")
plt.show()
