# VERSION = 0.1

import json

def get_first_last_dates():
    with open('habo.json', 'r') as file:
        data = json.load(file)
        first_dates=[]
        last_dates=[]
        for habit in data["habits"]:
            first_dates.append(next(iter(habit['events'])))
            last_dates.append(list(habit["events"].keys())[-1])

    return [min(first_dates).split(" ")[0],min(last_dates).split(" ")[0]]

def get_completion_for_day(date):
    with open('habo.json', 'r') as file:
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
