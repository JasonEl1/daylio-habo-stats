# VERSION = 0.1

import analysis
import habo
import daylio
from datetime import datetime,timedelta
import numpy as np

print("Analyzing data...")

start_date = analysis.get_start_end_days()[0]
end_date = analysis.get_start_end_days()[1]

x = np.arange(0, analysis.get_total_days(), 1)
y_daylio=[]
y_habo=[]
date=datetime.strptime(start_date, "%Y-%m-%d")
for i in range(analysis.get_total_days()):
    y_daylio.append(daylio.get_mood_for_date(date.strftime("%Y-%m-%d")))
    y_habo.append(5*(habo.get_completion_for_day(date.strftime("%Y-%m-%d"))))
    date+=timedelta(days=1)

print("Generating line plot...")

import matplotlib.pyplot as plt

plt.plot(x,y_daylio,label="Daylio")
plt.plot(x,y_habo,label="Habo")
plt.legend()
plt.xticks([x[0],x[len(x)-1]],labels=[start_date, end_date])
plt.xlabel("Date")
plt.ylabel("Mood / Habit Completion")
plt.show()
