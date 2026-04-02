"""
    EAS 501 - Sustainable Urban Systems
    Tutorial 2: Variables, Data Structures, and Pandas
    Noel Boland
    3/10/2026
"""

# assign a simple variable
name = "Benjamin"
age = 29
print(name, "is", age, "years old")

# playing with the variables
name = "Nimajneb"
age = 92
print(name, "is", age, "years old")
new_age = age + 10
print("in 10 years", name, "will be", new_age, "years old")

# tuple
person = ("Nimajneb", 102, "Atlantis")
print(person[0], "is", person[1], "years old.", person[0], "lives in", person[2], "AND this is a tuple!")
# use to find length of tuple person
print("how long is my tuple?", len(person), "objects long")
# do a calculation with the tuple
new_age = person[1] + 10
print("In 10 years", person[0], "will be", new_age, "years old")

# lists!
cat = ["Maggie", "cat", 8, "Ann Arbor"]
print(cat[0], "is a", cat[1], "and she is", cat[2], "years old.", cat[0], "lives in", cat[3])
print("how long is my list? -->", len(cat), "objects long")
# append my list to include Maggie's favorite banned food
cat.append("CheezIts")
print("how long is my list now? -->", len(cat), "objects long")
print(cat[0], "loves", cat[4])
# do a calculation on the age element of the cat list!
cat[2] = cat[2] + 10
print("In 10 years,", cat[0], "will be", cat[2], "years old!! Happy Birthday", cat[0])
# count the elements 
print("How many times does", cat[0], "occur in this list? -->", cat.count("Maggie"))

# create and sort a new list
new_list=[0, 0.5, 100, 102, 0, 0.2, 104.3]
print(new_list)
new_list.sort()
print(new_list)
# new a new element in the new list
new_list.append((1000, 2000))
print(new_list)
print(new_list[7][0])

# dictionaries
dog = {"name":"Stella", "age":2}
print(dog)
# get the name out of the dog dictionary
print(dog["name"], "!!")
dog["location"]="Chicago"
print(dog["name"], "is a dog and she is", dog["age"], "years old.", dog["name"], "lives in", dog["location"])

# pandas!
# import libraries
import pandas as pd
# dummy data
data = {
    "Name": ["Noel", "Maggie", "Stella"],
    "Age": [29, 8, 2],
    "Height (m)": [1.8, 0.2, 0.4],
    "Neighborhood": ["Downtown", "Uptown", "Middletown"]
}
# assign a dataframe to our data
df = pd.DataFrame(data)
# print data head
print(df.head())
# print the column headers only
print(df.columns)
# look at the name column
print(df["Name"])
# look at the first object in the df
print(df.loc[0][["Name", "Age"]])
# do some calculations on our data
avg_age = df["Age"].mean()
max_age = df["Age"].max()
min_age = df["Age"].min()
print("The average age in this data is:", avg_age)
print("The maximum age in this data is:", max_age)
print("The minimum age in this data is:", min_age)
