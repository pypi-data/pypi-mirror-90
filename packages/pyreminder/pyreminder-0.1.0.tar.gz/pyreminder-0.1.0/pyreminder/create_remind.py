import os

NEW_REMINDER = '''
osascript - "%s" "%s" "%s"<<END
on run argv
set stringedAll to date (item 2 of argv & " " & item 3 of argv)
tell application "Reminders"
make new reminder with properties {name:item 1 of argv, due date:stringedAll}
end tell
end run
END
'''

def new_reminder(name, date, time):
    new_reminder_cmd = NEW_REMINDER % (name, date, time)
    os.system(new_reminder_cmd)
