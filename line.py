import analysis
import habo
import daylio
from datetime import datetime,timedelta

#STARTING_DATE="2024-10-01"

data_x=[]
data_y=[]

#date=datetime.strptime(get_start_end_days()[0], "%Y-%m-%d")


import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0, analysis.get_total_days(), 1)
y_daylio=[]
y_habo=[]
date=datetime.strptime(analysis.get_start_end_days()[0], "%Y-%m-%d")
for i in range(analysis.get_total_days()):
    y_daylio.append(daylio.get_mood_for_date(date.strftime("%Y-%m-%d")))
    y_habo.append(5*(habo.get_completion_for_day(date.strftime("%Y-%m-%d"))))
    date+=timedelta(days=1)

plt.plot(x,y_daylio,label="Daylio")
plt.plot(x,y_habo,label="Habo")
plt.show()
