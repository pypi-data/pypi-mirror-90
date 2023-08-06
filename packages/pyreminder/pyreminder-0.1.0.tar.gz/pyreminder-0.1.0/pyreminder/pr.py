from .constants import DAYS
from .reminders_io import open_json
from .utils import create_reminder, create_reminders
import datetime
import os
import argparse
import sys

class PyReminders(object):
    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Create Apple Reminders through CLI interface",
            usage='''pyreminder <command> [<args>]

            The available commands are:
            create_from   Create all reminders from specified json files
            new           New reminder from specified parameters
            add           Add reminder to specified json file #TODO
            '''
        )
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def create_from(self):
        parser = argparse.ArgumentParser(
            description='Create reminders from specified json file'
        )
        parser.add_argument("--file", help="Choose reminders json file",
                required=True)
        args = parser.parse_args(sys.argv[2:])
        
        file_to_create_from = args.file
        print("Running pyreminder create, file=%s" % file_to_create_from)
        create_reminders(open_json(file_to_create_from)['tasks'])

    def new(self):
        parser = argparse.ArgumentParser(
            description='New reminder from specified parameters'
        )
        parser.add_argument("--name", help="Name of reminder",
                required=True)
        parser.add_argument("--time", help="Time of reminder", nargs="+",
                required=True)
        parser.add_argument("--days", help="Days to create reminder")
        parser.add_argument("--date", help="Date to create reminder")
        args = parser.parse_args(sys.argv[2:])
        
        print("Running pyreminder new:")
        new_reminder_dict = vars(args)
        for key in new_reminder_dict:
            if new_reminder_dict[key]:
                print("%s : %s" % (key, new_reminder_dict[key]))
        create_reminder(new_reminder_dict)
        



if __name__ == '__main__':
    PyReminders()
