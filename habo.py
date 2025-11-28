# habo.py v0.2.1

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

def get_num_habits(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        num_habits=len(data["habits"])
        file.close()
        return num_habits

def get_first_last_dates(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        first_dates=[]
        last_dates=[]
        for habit in data["habits"]:
            first_dates.append(next(iter(habit['events'])))
            last_dates.append(list(habit["events"].keys())[-1])

    return [max(first_dates).split(" ")[0],min(last_dates).split(" ")[0]]

def get_habit_name_from_id(filename,habit_id):
    with open(filename, 'r') as file:
        data = json.load(file)

        index=0
        for habit_index in range(len(data["habits"])):
            index=habit_index

            if(data["habits"][habit_index]["id"]==habit_id):
                break
        else:
            return -1

        return data["habits"][index]["title"]


def get_habit_for_day(date,filename,habit_id):
    with open(filename, 'r') as file:
        data = json.load(file)

        index=0
        for habit_index in range(len(data["habits"])):
            index=habit_index

            if(data["habits"][habit_index]["id"]==habit_id):
                break
        else:
            return -1

        file.close()

        try:
            completed = (data["habits"][index]["events"])[f"{date.strftime("%Y-%m-%d")} 12:00:00.000Z"][0]
        except:
            completed = "DayType.skip"
        if(completed=="DayType.check" or completed =="DayType.skip"):
            return 1
        return 0

def get_habit_ids(filename):
    with open(filename, 'r') as file:
        data = json.load(file)

        ids=[]
        for habit in data["habits"]:
            ids.append(habit["id"])

        file.close()

    return ids

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

        file.close()

    if(num_habits!=0):
        return num_completed/num_habits
    else:
        return 0
