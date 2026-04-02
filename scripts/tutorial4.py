"""
    EAS 501 - Sustainable Urban Systems
    Tutorial 4
    Noel Boland
    3/17/2026 🍀
"""

# install libraries
import matplotlib.pyplot as plt
import pandas as pd

# import files
raw_population_df = pd.read_csv("BostonPopulation_T4.csv")
raw_cal_cf_df = pd.read_csv("CaloricCF.txt", delimiter="\t")
raw_cal_intake_df = pd.read_excel("CaloricIntake.xlsx", 0)

# clean data: drop all rows with na values
# population data
population_df = raw_population_df.dropna()
# count how many rows we're dropping to keep track
count_na_population_dropped = len(raw_population_df) - len(population_df)
print(count_na_population_dropped, "number of rows dropped for population data")
# calorie cf data
cal_cf_df = raw_cal_cf_df.dropna()
# count how many rows we're dropping to keep track
count_na_cal_cf_dropped = len(raw_cal_cf_df) - len(cal_cf_df)
print(count_na_cal_cf_dropped, "number of rows dropped for calorie cf data")
# calorie intake data
cal_intake_df = raw_cal_intake_df.dropna()
count_na_cal_intake_dropped = len(raw_cal_intake_df) - len(cal_intake_df)
print(count_na_cal_intake_dropped, "number of rows dropped for calorie intake data")

# calculations for calorie cf data
# create a new colunn, called total, as a sum of production and transport data
cal_cf_df["Total"] = cal_cf_df["Production"] + cal_cf_df["Transport"]
# create a new column, called ratio, as a ratio between transport and total
cal_cf_df["Ratio"] = cal_cf_df["Transport"]/cal_cf_df["Total"]
# rescale the ratio values
cal_cf_df["Ratio"] = cal_cf_df["Ratio"]*100
# rename the columns
cal_cf_df.rename(columns={"Ratio": "Percent"}, inplace=True)

# do some grouping
# copied directly from the tutorial
food_group = ["Animal", "Fruit", "Fruit", "Animal", "Grain", 
              "Vegetable", "Animal", "Vegetable", "Fruit", "Nut", 
              "Animal", "Animal", "Beverage", "Beverage", "Vegetable", 
              "Vegetable", "Vegetable", "Oil", "Animal", "Animal"]
# insert this grouping into our df
cal_cf_df.insert(1, "Food Group", food_group, True)
# group the food groups and save this grouping as a series
group_cal_cf = cal_cf_df.groupby(["Food Group"])["Total"].mean()
# plot the series
group_cal_cf.plot.bar()
plt.title("Food Group Counts")
plt.xlabel("Food Group")
plt.ylabel("Avg Counts")
#plt.show()

# do some calculations
# sort by food for calorie cf data and reset index
cal_cf_df = cal_cf_df.sort_values(by=["Food"]).reset_index(drop=True)
# sort by item in calorie intake data and reset index
cal_intake_df = cal_intake_df.sort_values(by=["Item"]).reset_index(drop=-True)
# setup a new column name
impact_column = "Total"
# do some element-wise multiplication
diet_cf_df = cal_intake_df.iloc[:,1:].mul(cal_cf_df[impact_column], axis=0)
# sum up the totals
total = diet_cf_df.sum()
# transpose the data
total_df = pd.DataFrame(total).T
# index the total column
total_df.index = ["Total"]
# concat the data
diet_cf_df = pd.concat([diet_cf_df, total_df])

