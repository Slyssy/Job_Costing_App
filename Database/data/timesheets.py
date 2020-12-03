#set up dependencies
import pandas as pd 
import numpy as np
import time
from datetime import timedelta, datetime
import random

# create list of random user ids
user_id = list(np.random.randint(low=1, high=5, size=147))

# print(user_id)

# create list of project_ids
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

# create a list of random dates for each project
def randomDate(start, end):
    frmt = "%Y-%m-%d 07:15"

    stime = time.mktime(time.strptime(start, frmt))
    etime = time.mktime(time.strptime(end, frmt))

    ptime = stime + random.random() * (etime - stime)
    dt = datetime.fromtimestamp(time.mktime(time.localtime(ptime)))
    return dt.isoformat()

start_times = []

# project 1
for i in range(0 , 29):
    start_times.append(randomDate("2020-01-08 07:15", "2020-02-06 07:15"))

# project 2
proj_2 = []

for i in range(0 , 4):
    proj_2.append(randomDate("2020-02-15 07:15", "2020-02-20 07:15"))

start_times = start_times + proj_2

# project 3
proj_3 = []

for i in range(0 , 8):
    start_times.append(randomDate("2020-03-05 07:15", "2020-03-13 07:15"))

start_times = start_times + proj_3

# project 4
proj_4 = []

for i in range(0 , 13):
    start_times.append(randomDate("2020-04-17 07:15", "2020-05-01 07:15"))

start_times = start_times + proj_4

# project 5
proj_5 = []

for i in range(0 , 3):
    start_times.append(randomDate("2020-05-09 07:15", "2020-05-13 07:15"))

start_times = start_times + proj_5

# project 6
proj_6 = []

for i in range(0 , 15):
    start_times.append(randomDate("2020-06-23 07:15", "2020-07-09 07:15"))

start_times = start_times + proj_6

# project 7
proj_7 = []

for i in range(0 , 19):
    start_times.append(randomDate("2020-07-10 07:15", "2020-07-31 07:15"))

start_times = start_times + proj_7

# project 8
proj_8 = []

for i in range(0 , 3):
    start_times.append(randomDate("2020-08-01 07:15", "2020-08-04 07:15"))

start_times = start_times + proj_8

# project 9
proj_9 = []

for i in range(0 , 7):
    start_times.append(randomDate("2020-09-13 07:15", "2020-09-22 07:15"))

start_times = start_times + proj_9

# project 10
proj_10 = []

for i in range(0 , 36):
    start_times.append(randomDate("2020-10-11 07:15", "2020-11-17 07:15"))

start_times = start_times + proj_10

# project 11
proj_11 = []

for i in range(0 , 10):
    start_times.append(randomDate("2020-11-06 07:15", "2020-11-17 07:15"))

start_times = start_times + proj_11

print(start_times)
print(len(start_times))