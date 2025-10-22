import csv

DAYLIO_MOOD_TO_INT={"awful":1,"bad":2,"meh":3,"good":4,"rad":5}

def get_mood_for_date(date):
    with open('daylio.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0]==date:
                return DAYLIO_MOOD_TO_INT[row[4]]

def get_first_last_dates():
    with open('daylio.csv', 'r') as file:
        reader = csv.reader(file)
        last_date=""
        first_date=""
        loopcount=0
        for row in reader:
            if(loopcount==1):
                last_date=row
            first_date=row
            loopcount+=1

    return [first_date[0],last_date[0]]
