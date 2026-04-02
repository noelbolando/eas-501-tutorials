"""
    EAS 501 - Sustainable Urban Systems
    Tutorial 7
    Noel Boland
    4/2/2026
"""

# bring it all in
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# load in the data
boston_parcels_df = gpd.read_file("Parcels_2022/Parcels_2022.shp")
#print(boston_parcels_df.crs)
boston_BGs_df = gpd.read_file("boston_foodprint/boston_foodprint.shp")
#print(boston_BGs_df.crs)
boston_BGs_df = boston_BGs_df.to_crs(boston_parcels_df.crs)
#print(boston_parcels_df.crs)
tax_data_df = pd.read_csv("tax_data_2022.csv")
land_uses = (tax_data_df["LU_DESC"].unique())

# plotting!
fig, ax = plt.subplots(figsize=(10,10))
boston_BGs_df.plot(ax=ax,
                   color="white",
                   edgecolor="black")
boston_parcels_df.plot(ax=ax,
                       color="grey",
                       edgecolor="black")
plt.axis("off")
#plt.show()

boston_parcels_df["centroid"] = boston_parcels_df.centroid

fig2, ax2 = plt.subplots(figsize=(10,10))
boston_BGs_df.plot(ax=ax2,
                   color="white",
                   edgecolor="black")

boston_parcels_df["centroid"].plot(ax=ax2,
                                   marker="*",
                                   color="green",
                                   markersize=0.5)
plt.axis("off")
#plt.show()

# loop through and identify parking uses
parking_uses = []
for use in land_uses:
    if "PARKING" in use.upper() or "PKG" in use.upper():
        parking_uses.append(use)

# filter out the parking uses we want
parking_uses = [parking_uses[0], parking_uses[1], parking_uses[7]]

# create a new parking_df
parking_df = tax_data_df[tax_data_df["LU_DESC"].isin(parking_uses)]
# change types
parking_df["GIS_ID"] = parking_df["GIS_ID"].astype(int)
parking_df["GIS_ID"] = parking_df["GIS_ID"].astype(str)

# createa function to append GIS_ID
def append_zero(s):
    if len(s) < 10:
        return "0" + s
    else:
        return s

# apply appending function for GIS_ID
parking_df["GIS_ID"] = parking_df["GIS_ID"].apply(append_zero)

# drop the columns we don't need
parking_df = parking_df.filter(["GIS_ID", "LAND_SF", "GROSS_AREA"])

# join the two dataframes
boston_parcels_df.rename(columns={"MAP_PAR_ID":"GIS_ID"}, inplace=True)
parking_parcels_df = pd.merge(boston_parcels_df, parking_df, on="GIS_ID", how="inner")

# plot parking lots as centroids
fig, ax = plt.subplots(figsize=(10,10))
boston_BGs_df.plot(ax=ax,
                   color="white",
                   edgecolor="black")
parking_parcels_df["centroid"].plot(ax=ax,
                                    color="black",
                                    edgecolor="black",
                                    markersize=5)
plt.axis("off")
#plt.show()

# join BG GEOID to the parking parcels
parking_parcels_df = gpd.sjoin(parking_parcels_df, boston_BGs_df[["GEOID20", "geometry"]],
                            how="inner",
                            predicate="intersects")
parking_totals_df = parking_parcels_df.groupby(["GEOID20"])["ShapeSTAre"].sum()
parking_totals_df = pd.DataFrame(parking_totals_df)
parking_totals_df["m2"] = parking_totals_df["ShapeSTAre"]/3.28**2

# 🎉 scenario time 🎉
# making a dict 'crops':
crops = {"crop":
         ["beet", "pepper", "carrot", "cucumber", "kale", "lettuce", "tomato"],
         "yield":
         [2.26, 2.30, 1.63, 3.34, 4.72, 0.80, 2.94],
        "climate_shift":
        [-0.57, -2.29, -0.51, -2.46, -4.24, -0.90, -2.50]
        }
crops_df = pd.DataFrame(crops)
# calculate the mean yield and climate shift for our crop
mean_yield = crops_df["yield"].mean()
mean_climate_shift = crops_df["climate_shift"].mean()
# calculate total yield and cliamte shift for each BG
parking_totals_df["harvest"] = parking_totals_df["m2"]*mean_yield
parking_totals_df["climate_shift"] = parking_totals_df["m2"]*mean_climate_shift

# join scenario result to the parcel polygons
boston_BGs_df = boston_BGs_df.join(parking_totals_df, on="GEOID20")
print(parking_totals_df["climate_shift"].sum()/1000)

# plot climate shift
fix, ax = plt.subplots(figsize=(10,10))
boston_BGs_df.plot(ax=ax,
                   column="climate_shift",
                   legend=True,
                   missing_kwds={
                       "color": "lightgrey"
                       }
                    )
plt.axis("off")
plt.show()

# plot harvest
fix, ax = plt.subplots(figsize=(10,10))
boston_BGs_df.plot(ax=ax,
                   column="harvest",
                   legend=True,
                   missing_kwds={
                       "color": "lightgrey"
                       }
                    )
plt.axis("off")
plt.show()

