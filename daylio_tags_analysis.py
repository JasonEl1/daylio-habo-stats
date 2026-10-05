# daylio_tags_analysis.py v0.1.0

import daylio
from datetime import datetime,timedelta
import matplotlib.pyplot as plt
import numpy as np

DAYLIO_FILENAME=daylio.get_filename()

print("Analyzing data...")
start_time=datetime.now()

daylio_data = daylio.load_data(DAYLIO_FILENAME)

first_date, last_date = daylio.get_first_last_dates(DAYLIO_FILENAME)
num_days = (datetime.strptime(last_date, "%Y-%m-%d") - datetime.strptime(first_date, "%Y-%m-%d")).days
date=datetime.strptime(first_date, "%Y-%m-%d")

tags_data = {}

print("Pass 1 of 2...")
for _ in range(num_days):
    tags = daylio.get_tags_for_date(date.strftime("%Y-%m-%d"),daylio_data)
    for tag in tags:
        if(tag not in tags_data.keys()):
            tags_data[tag] = [0,0,0,0]
    date+=timedelta(days=1)

date=datetime.strptime(first_date, "%Y-%m-%d")

print("Pass 2 of 2...")
for _ in range(num_days):
    tags = daylio.get_tags_for_date(date.strftime("%Y-%m-%d"),daylio_data)
    mood = daylio.get_mood_for_date(date.strftime("%Y-%m-%d"),daylio_data)
    for tag in tags_data.keys():
        if tag in tags: # tag from dict was present in the day's tags
            tags_data[tag][0] += mood
            tags_data[tag][1] += 1
        else:
            tags_data[tag][2] += mood
            tags_data[tag][3] += 1
    date+=timedelta(days=1)

for tag in tags_data.keys():
    tags_data[tag] = [tags_data[tag][0]/tags_data[tag][1],tags_data[tag][2]/tags_data[tag][3]]

sorted_data = dict(sorted(tags_data.items(),key = lambda x:x[1][0]-x[1][1],reverse=True))

RESET_COLOUR='\033[0m'

end_time=datetime.now()
print()
print(f"Done in {round((end_time-start_time).total_seconds(),2)} seconds")
print("\nResults:")
print("--------")

for tag in sorted_data.keys():
    mood_with = tags_data[tag][0]
    mood_without = tags_data[tag][1]
    difference = mood_with-mood_without
    if(difference>=0):
        difference_colour='\033[32m'
        difference_colour_opp='\033[31m'
    else:
        difference_colour='\033[31m'
        difference_colour_opp='\033[32m'
    print(f"{tag}: {difference_colour}{mood_with:.2f}{RESET_COLOUR} with and {difference_colour_opp}{mood_without:.2f}{RESET_COLOUR} without ({difference_colour}{difference:+.2f}{RESET_COLOUR} difference)")