#set up dependencies
import pandas as pd 
import numpy as np
import time
from datetime import timedelta, datetime
import random

# create list of random user ids 
user_id = list(np.random.randint(low=1, high=5, size=147))

# print(user_id)

# create list of project_ids depending on the number of project days @ 8 hours per work day
# project 1
project_id = list(np.random.randint(low=1, high=2, size=29))

# project 2
project_id = project_id + list(np.random.randint(low=2, high=3, size=4))

# project 3
project_id = project_id + list(np.random.randint(low=3, high=4, size=8))

# project 4
project_id = project_id + list(np.random.randint(low=4, high=5, size=13))

# project 5
project_id = project_id + list(np.random.randint(low=5, high=6, size=3))

# project 6
project_id = project_id + list(np.random.randint(low=6, high=7, size=15))

# project 7
project_id = project_id + list(np.random.randint(low=7, high=8, size=19))

# project 8
project_id = project_id + list(np.random.randint(low=8, high=9, size=3))

# project 9
project_id = project_id + list(np.random.randint(low=9, high=10, size=7))

# project 10
project_id = project_id + list(np.random.randint(low=10, high=11, size=36))

# project 11
project_id = project_id + list(np.random.randint(low=11, high=12, size=10))

# print(len(project_id))

# create function to create random dates between two dates for each project
def randomDate(start, end):
    frmt = "%Y-%m-%d 07:15"

    stime = time.mktime(time.strptime(start, frmt))
    etime = time.mktime(time.strptime(end, frmt))

    ptime = stime + random.random() * (etime - stime)
    dt = datetime.fromtimestamp(time.mktime(time.localtime(ptime)))
    return dt.isoformat()

# append random dates to a list for each projects number of project days within the project start and end date

dates = []

# project 1
for i in range(0 , 29):
    dates.append(randomDate("2020-01-08 07:15", "2020-02-06 07:15"))

# project 2

for i in range(0 , 4):
    dates.append(randomDate("2020-02-15 07:15", "2020-02-20 07:15"))

# project 3

for i in range(0 , 8):
    dates.append(randomDate("2020-03-05 07:15", "2020-03-13 07:15"))

# project 4

for i in range(0 , 13):
    dates.append(randomDate("2020-04-17 07:15", "2020-05-01 07:15"))

# project 5

for i in range(0 , 3):
    dates.append(randomDate("2020-05-09 07:15", "2020-05-13 07:15"))

# project 6

for i in range(0 , 15):
    dates.append(randomDate("2020-06-23 07:15", "2020-07-09 07:15"))

# project 7

for i in range(0 , 19):
    dates.append(randomDate("2020-07-10 07:15", "2020-07-31 07:15"))

# project 8

for i in range(0 , 3):
    dates.append(randomDate("2020-08-01 07:15", "2020-08-04 07:15"))

# project 9

for i in range(0 , 7):
    dates.append(randomDate("2020-09-13 07:15", "2020-09-22 07:15"))

# project 10

for i in range(0 , 36):
    dates.append(randomDate("2020-10-11 07:15", "2020-11-17 07:15"))

# project 11

for i in range(0 , 10):
    dates.append(randomDate("2020-11-06 07:15", "2020-11-17 07:15"))


# add lists to pandas dataframe
df = pd.DataFrame({"user_id": user_id, "project_id": project_id, "start_time": dates, "finish_time": dates})

# convert to pandas datetime with just the date
df["start_time"] = pd.to_datetime(df["start_time"]).dt.date.astype(str)
df["finish_time"] = pd.to_datetime(df["finish_time"]).dt.date.astype(str)

# add start and finish time to each date that will equate to 8 hours of work
df["start_time"] += " 07:15:00"
df["finish_time"] += " 15:15:00"

# print(df)

# print(df.info())

df.to_csv("for_database/timesheets.csv", index=False)
