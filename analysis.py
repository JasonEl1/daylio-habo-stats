#v0.2

import habo
import daylio
from datetime import datetime,timedelta

def get_start_end_days(habo_filename,daylio_filename):
    habo_dates=habo.get_first_last_dates(habo_filename)
    daylio_dates=daylio.get_first_last_dates(daylio_filename)
    return [max(habo_dates[0],daylio_dates[0]),min(habo_dates[1],daylio_dates[1])]

def get_total_days(habo_filename,daylio_filename):
    start_date = datetime.strptime(get_start_end_days(habo_filename,daylio_filename)[0], "%Y-%m-%d")
    end_date = datetime.strptime(get_start_end_days(habo_filename,daylio_filename)[1], "%Y-%m-%d")

    return ((end_date-start_date).days)+1
