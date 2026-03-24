"""
    EAS 501 - Sustainable Urban Systems
    Tutorial 5
    Noel Boland
    3/24/2026
"""

# install libraries
import matplotlib.pyplot as plt
import pandas as pd


def load_data():
    """
        Loads our data and returns the raw dataframes for each file.
    """
    raw_population_df = pd.read_csv("BostonPopulation_T4.csv")
    raw_cal_cf_df = pd.read_csv("CaloricCF.txt", delimiter="\t")
    raw_cal_intake_df = pd.read_excel("CaloricIntake.xlsx", 0)
    
    return raw_population_df, raw_cal_cf_df, raw_cal_intake_df


def clean_data(raw_population_df, raw_cal_cf_df, raw_cal_intake_df):
    """
        Cleans our data and returns the cleaned dataframes for each file.
    """
    
    # drop all rows with na values and duplicates
    population_df = raw_population_df.dropna().drop_duplicates()
    cal_cf_df = raw_cal_cf_df.dropna().drop_duplicates()
    cal_intake_df = raw_cal_intake_df.dropna().drop_duplicates()
    
    # counter output to check how many records we're dropping
    count_na_population_dropped = len(raw_population_df) - len(population_df)
    count_na_cal_cf_dropped = len(raw_cal_cf_df) - len(cal_cf_df)
    count_na_cal_intake_dropped = len(raw_cal_intake_df) - len(cal_intake_df)
    
    # print out the counter results
    print(count_na_population_dropped, "number of rows dropped for population data")
    print(count_na_cal_cf_dropped, "number of rows dropped for calorie cf data")
    print(count_na_cal_intake_dropped, "number of rows dropped for calorie intake data")
    
    return population_df, cal_cf_df, cal_intake_df


def calculate_cal_cf(cal_cf_df):
    """
        Calculates the total carbon footprint of calories consumed across food groups.
    """
    # create a new colunn, called total, as a sum of production and transport data
    cal_cf_df["Total"] = cal_cf_df["Production"] + cal_cf_df["Transport"]
    # create a new column, called ratio, as a ratio between transport and total
    cal_cf_df["Ratio"] = cal_cf_df["Transport"]/cal_cf_df["Total"]
    # rescale the ratio values
    cal_cf_df["Ratio"] = cal_cf_df["Ratio"]*100
    # rename the columns
    cal_cf_df.rename(columns={"Ratio": "Percent"}, inplace=True)

    # do some grouping by food groups
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
    plt.show()

    return cal_cf_df


def calculate_diet_cf(cal_cf_df, cal_intake_df):
    """
        Calculates the carbon footprint across the calorie intake data by food group.
    """
    # sort by food for calorie cf data and reset index
    cal_cf_df = cal_cf_df.sort_values(by=["Food"]).reset_index(drop=True)
    # sort by item in calorie intake data and reset index
    cal_intake_df = cal_intake_df.sort_values(by=["Item"]).reset_index(drop=True)
    # setup a new column name
    impact_column = "Total"
    # do some element-wise multiplication (this is the demo data df)
    diet_cf_df = cal_intake_df.iloc[:,1:].mul(cal_cf_df[impact_column], axis=0)
    # sum up the totals
    total = diet_cf_df.sum()
    # transpose the data
    total_df = pd.DataFrame(total).T
    # index the total column
    total_df.index = ["Total"]
    # concat the data (this is the diet cf df)
    diet_cf_df = pd.concat([diet_cf_df, total_df])
    
    return diet_cf_df


def calculate_demo_df(cal_cf_df, cal_intake_df):
    """
        Calculate the carbon footprint of calories consumed across demographic data by food group. 
    """
    cal_cf_df["Total"] = cal_cf_df["Production"] + cal_cf_df["Transport"]
    cal_cf_df = cal_cf_df.sort_values(by=["Food"]).reset_index(drop=True)
    cal_intake_df = cal_intake_df.sort_values(by=["Item"]).reset_index(drop=True)

    impact_column = "Total"
    diet_cf_df = cal_intake_df.iloc[:, 1:].mul(cal_cf_df[impact_column], axis=0)

    total = diet_cf_df.sum()
    total_df = pd.DataFrame(total).T
    total_df.index = ["Total"]

    return total_df


def calculate_df_pd(population_df, total_cf, demo_group):
    """
        Calculate the carbon footprint for a given population of a demo group.
    """

    multiplier = total_cf[demo_group].iloc[0]
    impacts = population_df * multiplier

    return impacts


# main, don't touch
def main():
    
    raw_population_df, raw_cal_cf_df, raw_cal_intake_df = load_data()
    population_df, cal_cf_df, cal_intake_df = clean_data(raw_population_df, raw_cal_cf_df, raw_cal_intake_df)
    cal_cf_df = calculate_cal_cf(cal_cf_df)
    diet_cf_df = calculate_diet_cf(cal_cf_df, cal_intake_df)
    total_df = calculate_demo_df(cal_cf_df, cal_intake_df)
    impacts = calculate_df_pd(population_df, total_df, demo_group="Males (1-3)")

    # method 1 - loop through columns
    m1_results = pd.DataFrame({})
    for column in population_df:
        if column == "GEOID":
            m1_results[column] = population_df[column]
        else:
            m1_results[column+"_CF"] = population_df[column] * total_df[column].iloc[0]
    m1_results["Total"] = m1_results.sum(axis=1, numeric_only=True)
    print(m1_results)

    # method 2
    m2_results = pd.DataFrame({})
    m2_results["GEOID"] = population_df["GEOID"]
    demo_groups = population_df.columns.to_list()[1:]
    for demo in demo_groups:
        m2_results[demo+"_CF"] = population_df[demo].apply(
            calculate_df_pd, args=(total_df, demo)
        )
    m2_results["Total"] = m2_results.sum(axis=1, numeric_only=True)
    print(m2_results)

    # method 3 - mul function
    m3_results = pd.DataFrame({})
    m3_results["GEOID"] = population_df["GEOID"]
    multipliers = total_df.to_dict()
    for key in multipliers:
        multipliers[key] = multipliers[key]["Total"]
    m3_results["Total"] = population_df.iloc[:,1:].mul(multipliers).sum(axis=1)
    print(m3_results)

main()
