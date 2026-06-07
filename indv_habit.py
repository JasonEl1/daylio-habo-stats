# indv_habit.py v0.0.1

import habo
from datetime import datetime, timedelta
import sys
from tqdm import tqdm
import analysis
import numpy as np
import matplotlib.pyplot as plt

HABO_FILENAME=habo.get_filename()

print("Analyzing data...")
start_time=datetime.now()

data={}

habit_ids = habo.get_habit_ids(HABO_FILENAME)

print("Habits:")
print("--------------")

for habit_id in habit_ids:
    print(f"ID {habit_id} - {habo.get_habit_name_from_id(HABO_FILENAME,habit_id)}")

print("--------------")


chosen_habit_id = int(input("Which habit to analyze? : "))
while int(chosen_habit_id) not in habit_ids:
    print("Invalid habit ID, try again.")
    chosen_habit_id = input("Which habit to analyze? : ")

start_end_dates = habo.get_first_last_dates_for_habit(HABO_FILENAME,chosen_habit_id)
num_days = (datetime.strptime(start_end_dates[1],"%Y-%m-%d")-datetime.strptime(start_end_dates[0],"%Y-%m-%d")).days+1

y_data = []

date = datetime.strptime(start_end_dates[0],"%Y-%m-%d")

for _ in tqdm(range(num_days)):
    y_data.append(habo.get_habit_for_day(date,HABO_FILENAME,chosen_habit_id))
    date+=timedelta(days=1)

print("Generating line plot...")

analysis.rolling_average(y_data)
x = np.arange(0, len(y_data), 1)

plt.plot(x, y_data)
plt.title(f"Habit completion - {habo.get_habit_name_from_id(HABO_FILENAME,int(chosen_habit_id))}")
plt.xticks([x[0],x[len(x)-1]],labels=[start_end_dates[0],start_end_dates[1]])
plt.xlabel("Date")
plt.ylabel("Habit completion (rolling avg.)")

plt.show()

end_time=datetime.now()
print(f"Done in {round((end_time-start_time).total_seconds(),2)} seconds")