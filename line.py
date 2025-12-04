#line.py v0.5.0

import analysis
import habo
import daylio
from datetime import datetime,timedelta
import numpy as np
import math
import sys
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd

HABO_FILENAME=habo.get_filename()
DAYLIO_FILENAME=daylio.get_filename()

def rolling_average(list):
    CHUNK_SIZE=math.ceil(len(list)/50)

    newlist=[]
    for i in range(0,len(list),CHUNK_SIZE):
        newlist.append(sum(list[i:i+CHUNK_SIZE])/len(list[i:i+CHUNK_SIZE]))

    list[:]=newlist

print("Analyzing data...")
start_time=datetime.now()

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

y_daylio=[]
y_habo=[]

daylio_data=daylio.load_data(DAYLIO_FILENAME)

for _ in tqdm(range(num_days)):
    y_daylio.append(daylio.get_mood_for_date_preloaded(date.strftime("%Y-%m-%d"),daylio_data))
    y_habo.append(habo.get_completion_for_day(date.strftime("%Y-%m-%d"),HABO_FILENAME))
    date+=timedelta(days=1)

print("Generating line plot...")

assert(len(y_daylio)!=0 and len(y_habo)!=0)
rolling_average(y_daylio)
rolling_average(y_habo)
x = np.arange(0, len(y_daylio), 1)

fig,daylio_axis=plt.subplots()
daylio_line = daylio_axis.plot(x,y_daylio,label="Daylio",color="blue")
daylio_axis.set_ylabel("Mood")
daylio_axis.set_xticks([x[0],x[len(x)-1]],labels=[start_date,end_date])
daylio_axis.set_xlabel("Date")

habo_axis = daylio_axis.twinx()
habo_line = habo_axis.plot(x,y_habo,label="Habo",color="orange")
habo_axis.set_ylabel("Habit Completion")

fig.legend(bbox_to_anchor=(.6,.3),draggable=True)

end_time=datetime.now()
print(f"Done in {round((end_time-start_time).total_seconds(),2)} seconds")
plt.show()
