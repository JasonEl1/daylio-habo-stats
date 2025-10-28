# VERSION = 0.1

import analysis
import habo
import daylio
from datetime import datetime,timedelta

print("Analyzing data...")

data_x=[]
data_y=[]

date=datetime.strptime("2024-10-01", "%Y-%m-%d")
for i in range(analysis.get_total_days()):
    data_x.append(daylio.get_mood_for_date(date.strftime("%Y-%m-%d")))
    data_y.append(habo.get_completion_for_day(date.strftime("%Y-%m-%d")))
    date+=timedelta(days=1)

print("Generating scatter plot...")

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

daylio_cmap = ListedColormap(daylio.DAYLIO_MOOD_COLOURS)

plt.scatter(data_x, data_y,c=data_x,cmap=daylio_cmap)
plt.ylim(0.0, 1.2)
plt.xticks(list(daylio.DAYLIO_MOOD_TO_INT.values()),labels=list(daylio.DAYLIO_MOOD_TO_INT.keys()))
#plt.yticks([0.0,0.2,0.4,0.6,0.8,1.0])
plt.xlabel("Mood")
plt.ylabel("Habit Completion")
plt.show()
