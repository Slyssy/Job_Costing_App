# set up dependencies
import pandas as pd

# read in users csv
df_users = pd.read_csv("originals/users.csv")

# print datatypes
print(df_users.info())

# user data is correct, no changes needed


# read in project details csv
df = pd.read_csv("originals/project_details.csv")

# convert columns to correct datatypes
df["zip"] = df["zip"].astype("str")
df["revenue"] = df["revenue"].astype("float")
df["est_labor_rate"] = df["est_labor_rate"].astype("float")
df["est_labor_hours"] = df["est_labor_hours"].astype("float")
df["est_labor_expense"] = df["est_labor_expense"].astype("float")

#print datatypes
print(df.info())

df.to_csv("for_database/project_details.csv", index=False)

