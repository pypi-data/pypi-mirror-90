DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday",
        "Sunday"]
WEEKDAYS = DAYS[:5]
WEEKENDS = DAYS[5:]
EVERY_OTHER_DAY = DAYS[::2]
EVERY_OTHER_DAY_STARTING_TUESDAY = DAYS[1::2]

DAYS_MAP = {
        "everyday": DAYS,
        "weekdays": WEEKDAYS,
        "weekends": WEEKENDS,
        "every other day": EVERY_OTHER_DAY,
        "every other day starting Tuesday": EVERY_OTHER_DAY_STARTING_TUESDAY
}
