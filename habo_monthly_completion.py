# habo_monthly_completion.py v0.0.1

import habo
from datetime import datetime, timedelta
from tqdm import tqdm
import matplotlib.pyplot as plt

MONTH_NUM_TO_DAY = [
    "",
    "January ",
    "February ",
    "March ",
    "April ",
    "May ",
    "June ",
    "July ",
    "August ",
    "September ",
    "October ",
    "November ",
    "December "
]

HABO_FILENAME = habo.get_filename()
first_last_dates = habo.get_first_last_dates(HABO_FILENAME)

num_days = (datetime.strptime(first_last_dates[1], "%Y-%m-%d") - datetime.strptime(first_last_dates[0], "%Y-%m-%d")).days

print("Analyzing data...")
start_time=datetime.now()

date=datetime.strptime(first_last_dates[0], "%Y-%m-%d")

month_completions = {}

month = date.month
prev_month = month

month_completed = 0
month_total = 0

year_compensation = 0

for _ in tqdm(range(num_days)):
    month=date.month
    if(month != prev_month):
        if(prev_month == 12):
            year_compensation = 1
        month_completions[str(str(MONTH_NUM_TO_DAY[prev_month])+str(date.year-year_compensation))] = month_completed/month_total
        year_compensation = 0
        prev_month = month
        month_completed = 0
        month_total = 0

    month_total+=1
    month_completed += habo.get_completion_for_day(date.strftime("%Y-%m-%d"),HABO_FILENAME)
    date+=timedelta(days=1)

print("Generating line plot...")

x = list(month_completions.keys())
y = []
for key in month_completions.keys():
    y.append(month_completions[key])

plt.plot(x,y)
plt.ylabel("Habit completion")
plt.xlabel("Months")
plt.xticks([x[0],x[int(len(x)/2)],x[-1]])

end_time=datetime.now()
print(f"Done in {round((end_time-start_time).total_seconds(),2)} seconds")

print("Habit completion by month:")
print("--------------------------")

sorted_completions = sorted(month_completions.items(),key = lambda x:x[1],reverse=True)
for month in sorted_completions:
    print(f"{month[0]} - {round(month[1],2)}")

plt.show()