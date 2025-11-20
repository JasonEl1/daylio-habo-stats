#v0.3

import analysis
import habo
import daylio
from datetime import datetime,timedelta
import sys
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

HABO_FILENAME=habo.get_filename()
DAYLIO_FILENAME=daylio.get_filename()

print("Analyzing data...")

start_end_dates=analysis.get_start_end_days(HABO_FILENAME,DAYLIO_FILENAME)

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

data_x=[]
data_y=[]

for i in range(num_days):
    data_x.append(daylio.get_mood_for_date(date.strftime("%Y-%m-%d"),DAYLIO_FILENAME))
    data_y.append(habo.get_completion_for_day(date.strftime("%Y-%m-%d"),HABO_FILENAME))
    date+=timedelta(days=1)

print("Generating scatter plot...")

daylio_cmap = ListedColormap(daylio.DAYLIO_MOOD_COLOURS)

m,b=np.polyfit(data_x,data_y,1)
print(m)
print(b)
print(data_x[0])
x=np.array([1,2,3,4,5])

plt.scatter(data_x, data_y,c=data_x,cmap=daylio_cmap)
plt.plot(x,m*x+b,alpha=0.1)
plt.ylim(0.0, 1.2)
plt.xticks(list(daylio.DAYLIO_MOOD_TO_INT.values()),labels=list(daylio.DAYLIO_MOOD_TO_INT.keys()))
plt.yticks([0.0,0.2,0.4,0.6,0.8,1.0])
plt.xlabel("Mood")
plt.ylabel("Habit Completion")

print("Done")
plt.show()
