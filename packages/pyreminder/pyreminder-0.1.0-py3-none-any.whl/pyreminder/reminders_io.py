from json import load

def open_json(filename):
    with open(filename, 'r') as f:
        reminders = load(f)
    return reminders
