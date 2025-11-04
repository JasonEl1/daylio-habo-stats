#v0.2

import os
import json

def get_filename():
    current_dir = os.getcwd()
    possible_filenames=[]

    for entry in os.listdir(current_dir):
        if os.path.isfile(os.path.join(current_dir, entry)):
            if entry.endswith(".json"):
                possible_filenames.append(entry)

    if(len(possible_filenames)==1):
        return possible_filenames[0]
    else:
        print("Multiple habo files found:")
        for i in range(len(possible_filenames)):
            print(f"[{i}]:{possible_filenames[i]}")
        while(True):
            try:
                choice = int(input("Select a habo file: "))
                if(choice>(len(possible_filenames)-1)):
                    raise ValueError
                break
            except ValueError:
                print("Invalid input, try again.")

        return possible_filenames[choice]

def get_first_last_dates(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        first_dates=[]
        last_dates=[]
        for habit in data["habits"]:
            first_dates.append(next(iter(habit['events'])))
            last_dates.append(list(habit["events"].keys())[-1])

    return [min(first_dates).split(" ")[0],min(last_dates).split(" ")[0]]

def get_completion_for_day(date,filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        num_habits=len(data["habits"])
        num_completed=0
        for i in range(num_habits):
            try:
                completed = (data["habits"][i]["events"])[f"{date} 12:00:00.000Z"][0]
            except Exception as e:
                completed="DayType.fail"
                num_habits-=1
            if(completed=="DayType.check" or completed =="DayType.skip"):
                num_completed+=1

    if(num_habits!=0):
        return num_completed/num_habits
    else:
        return 0
