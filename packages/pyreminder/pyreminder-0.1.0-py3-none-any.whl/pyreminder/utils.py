from .constants import DAYS, DAYS_MAP
from .create_remind import new_reminder
import os
import datetime
import random

def get_current_date():
    return datetime.date.strftime(datetime.datetime.now(), "%m/%d/%Y")

def get_current_day():
    _, _, current_day = datetime.date.today().isocalendar()
    return DAYS[current_day - 1]
    
CURRENT_DAY = get_current_day()
CURRENT_DATE = get_current_date()

def parse_time(time):
    if len(time) == 1:
        return time[0]
    elif len(time) == 2:
        return get_random_time(time)

def get_random_time(time_range):
    start, end = time_range
    sh, sm = start.split(":")
    eh, em = end.split(":")
    rh = random.randint(int(sh), int(eh))
    if (rh == sh) and (rh == eh):
        return "{:02d}:{:02d}".format(rh, random.randint(int(sm),int(em)))
    elif rh == sh:
        return "{:02d}:{:02d}".format(rh, random.randint(int(sm),59))
    elif rh == eh:
        return "{:02d}:{:02d}".format(rh, random.randint(0, int(em)))
    else:
        return "{:02d}:{:02d}".format(rh, random.randint(0, 59))

def convert_time(task_time):
    return datetime.datetime.strptime(task_time, "%H:%M").strftime("%I:%M%p")

def _create_reminder(task, task_date): 
    task_time = convert_time(parse_time(task['time']))
    new_reminder(task['name'], task_date, task_time)

def create_reminder(task):
    if task.get("days"):
        if CURRENT_DAY in DAYS_MAP[task["days"]]:
            _create_reminder(task, CURRENT_DATE)
    elif task.get("date"):
        _create_reminder(task, task["date"])
    else:
        _create_reminder(task, CURRENT_DATE)

def create_reminders(tasks):
    for task in tasks:
        create_reminder(task)
