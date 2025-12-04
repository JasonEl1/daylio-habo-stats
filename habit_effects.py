# habit_effects.py v0.2.0

import habo
import daylio
import analysis
from datetime import datetime, timedelta
import sys
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np

HABO_FILENAME=habo.get_filename()
DAYLIO_FILENAME=daylio.get_filename()

print("Analyzing data...")
start_time=datetime.now()

start_end_dates = analysis.get_start_end_days(HABO_FILENAME,DAYLIO_FILENAME)

if(len(sys.argv)==3 and len(sys.argv[1])==len(sys.argv[2]) and len(sys.argv[1])==10): #if correctly passed start, end dates
    try:
        start_date=sys.argv[1]
        date=datetime.strptime(start_date,"%Y-%m-%d")
        end_date=sys.argv[2]

    except ValueError:
        print("Incorrect start date format")
        sys.exit()

    try:
        assert((date-datetime.strptime(start_end_dates[0],"%Y-%m-%d")).days >=0)
    except:
        print(f"Error: Start date is not within data range\nAllowed range is: {start_end_dates[0]} to {start_end_dates[1]}")
        sys.exit()

    try:
        assert((datetime.strptime(end_date,"%Y-%m-%d")-datetime.strptime(start_end_dates[1],"%Y-%m-%d")).days <=0)
    except:
        print(f"Error: End date is not within data range\nAllowed range is: {start_end_dates[0]} to {start_end_dates[1]}")
        sys.exit()

    num_days=(datetime.strptime(end_date,"%Y-%m-%d")-date).days + 1
else:
    start_date = start_end_dates[0]
    end_date = start_end_dates[1]

    date=datetime.strptime(start_date, "%Y-%m-%d")

    num_days=analysis.get_total_days(HABO_FILENAME,DAYLIO_FILENAME)


daylio_data=daylio.load_data(DAYLIO_FILENAME)
data={}

for habit_id in habo.get_habit_ids(HABO_FILENAME):
    date=datetime.strptime(start_date, "%Y-%m-%d")
    completed_total=0
    num_completed=0
    failed_total=0
    num_failed=0
    for _ in tqdm(range(num_days)):
        mood=daylio.get_mood_for_date_preloaded(date.strftime("%Y-%m-%d"),daylio_data)
        if(habo.get_habit_for_day(date,HABO_FILENAME,habit_id)):
            completed_total+=mood
            num_completed+=1
        else:
            failed_total+=mood
            num_failed+=1

        date+=timedelta(days=1)
    if(num_completed==0):
        completed_total=0
        num_completed=1
    elif(num_failed==0):
        failed_total=0
        num_failed=1
    data[habit_id]=[round((completed_total/num_completed),2),round((failed_total/num_failed),2)]

end_time=datetime.now()
print()
print(f"Done in {round((end_time-start_time).total_seconds(),2)} seconds")
print("\nResults:")
print("--------")

RESET_COLOUR='\033[0m'

data_ids = list(data.keys())
completed_results=[]
failed_results=[]
habit_names=[]
data_ids=sorted(data_ids)
for habit_id in data_ids:
    difference=data[habit_id][0]-data[habit_id][1]
    if(difference>=0):
        difference_colour='\033[32m'
        difference_colour_opp='\033[31m'

    else:
        difference_colour='\033[31m'
        difference_colour_opp='\033[32m'
    print(f"Habit {habit_id}: {habo.get_habit_name_from_id(HABO_FILENAME,habit_id)} - {difference_colour}{data[habit_id][0]}{RESET_COLOUR} with and {difference_colour_opp}{data[habit_id][1]}{RESET_COLOUR} without ({difference_colour}{difference:+.2f}{RESET_COLOUR} difference)")
    completed_results.append(data[habit_id][0])
    failed_results.append(data[habit_id][1])
    habit_names.append(habo.get_habit_name_from_id(HABO_FILENAME,habit_id))

print("\nGenerating plot...")

bar_positions = np.arange(len(data_ids))
width=0.3
plt.bar(bar_positions-width/2,completed_results,width,label="Habit completed")
plt.bar(bar_positions+width/2,failed_results,width,label="Habit failed")
plt.xticks(bar_positions,data_ids)
plt.xlabel("Habit no.")
plt.ylabel("Average mood")
plt.legend()
plt.show()
