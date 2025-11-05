#v0.3

import analysis
import habo
import daylio
from datetime import datetime,timedelta
import numpy as np
import math

HABO_FILENAME=habo.get_filename()
DAYLIO_FILENAME=daylio.get_filename()

def rolling_average(list):
    CHUNK_SIZE=math.ceil(len(list)/100)

    newlist=[]
    for i in range(0,len(list),CHUNK_SIZE):
        newlist.append(sum(list[i:i+CHUNK_SIZE])/CHUNK_SIZE)

    list[:]=newlist

print("Analyzing data...")

start_end_dates=analysis.get_start_end_days(HABO_FILENAME,DAYLIO_FILENAME)

start_date = start_end_dates[0]
end_date = start_end_dates[1]

y_daylio=[]
y_habo=[]
date=datetime.strptime(start_date, "%Y-%m-%d")
for i in range(analysis.get_total_days(HABO_FILENAME,DAYLIO_FILENAME)):
    y_daylio.append(daylio.get_mood_for_date(date.strftime("%Y-%m-%d"),DAYLIO_FILENAME))
    y_habo.append(habo.get_completion_for_day(date.strftime("%Y-%m-%d"),HABO_FILENAME))
    date+=timedelta(days=1)

print("Generating line plot...")

import matplotlib.pyplot as plt

assert(len(y_daylio)!=0 and len(y_habo)!=0)
rolling_average(y_daylio)
rolling_average(y_habo)
x = np.arange(0, len(y_daylio), 1)

fig,daylio_axis=plt.subplots()
daylio_line = daylio_axis.plot(x,y_daylio,label="Daylio",color="blue")
daylio_axis.set_ylabel("Mood")
daylio_axis.set_xticks([x[50],x[len(x)-10]],labels=["2024-11-04", "2025-11-04"]) #needs update
daylio_axis.set_xlabel("Date")

habo_axis = daylio_axis.twinx()
habo_line = habo_axis.plot(x,y_habo,label="Habo",color="orange")
habo_axis.set_ylabel("Habit Completion")

fig.legend(bbox_to_anchor=(.6,.3),draggable=True)
print("Done")
plt.show()
