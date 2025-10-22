import habo
import daylio
from datetime import datetime,timedelta

def get_start_end_days():
    return [max(habo.get_first_last_dates()[0],daylio.get_first_last_dates()[0]),min(habo.get_first_last_dates()[1],daylio.get_first_last_dates()[1])]

def get_total_days():
    start_date = datetime.strptime(get_start_end_days()[0], "%Y-%m-%d")
    end_date = datetime.strptime(get_start_end_days()[1], "%Y-%m-%d")

    return ((end_date-start_date).days)+1
