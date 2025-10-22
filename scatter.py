import analysis
import habo
import daylio
from datetime import datetime,timedelta

data_x=[]
data_y=[]

#date=datetime.strptime(get_start_end_days()[0], "%Y-%m-%d")
date=datetime.strptime("2024-10-01", "%Y-%m-%d")
for i in range(analysis.get_total_days()):
    data_x.append(daylio.get_mood_for_date(date.strftime("%Y-%m-%d")))
    data_y.append(habo.get_completion_for_day(date.strftime("%Y-%m-%d")))
    date+=timedelta(days=1)

import matplotlib.pyplot as plt
import numpy as np

print(type(data_x[0]))
print(type(data_y[0]))


plt.scatter(data_x, data_y)
plt.ylim(0.0, 1.2)
plt.show()
