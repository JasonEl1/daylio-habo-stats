# daylio.py v0.3.0

import os
import csv
import pandas as pd

def get_filename():
    current_dir = os.getcwd()
    possible_filenames=[]

    for entry in os.listdir(current_dir):
        if os.path.isfile(os.path.join(current_dir, entry)):
            if entry.endswith(".csv"):
                possible_filenames.append(entry)

    if(len(possible_filenames)==1):
        return possible_filenames[0]
    else:
        print("Multiple Daylio files found:")
        for i in range(len(possible_filenames)):
            print(f"[{i}]:{possible_filenames[i]}")
        while(True):
            try:
                choice = int(input("Select a Daylio file: "))
                break
            except ValueError:
                print("Invalid input, try again.")

        return possible_filenames[choice]

DAYLIO_MOOD_TO_INT={"awful":1,"bad":2,"meh":3,"good":4,"rad":5}
DAYLIO_MOOD_COLOURS = ["red", "orange","gold","limegreen","mediumseagreen"]

def load_data(filename):
    return pd.read_csv(filename)


def get_mood_for_date(date,filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0]==date:
                result=int(DAYLIO_MOOD_TO_INT[row[4]])
                file.close()
                return result
        file.close()
        return -1

def get_mood_for_date_preloaded(date,data):
    return int(DAYLIO_MOOD_TO_INT[data[data["full_date"]==date]["mood"].iloc[0]])

def get_first_last_dates(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        last_date=""
        first_date=""
        loopcount=0
        for row in reader:
            if(loopcount==1):
                last_date=row
            first_date=row
            loopcount+=1

    return [first_date[0],last_date[0]]
