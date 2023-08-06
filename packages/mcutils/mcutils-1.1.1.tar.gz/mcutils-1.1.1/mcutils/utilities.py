from .print_manager import mcprint, Color
from .input_validation import get_input
from datetime import datetime
import logging


class About:
    def __init__(self,
                 authors=None,
                 company_name=None,
                 team_name=None,
                 github_account=None,
                 email_address=None,
                 github_repo=None):

        self.authors = authors
        self.company_name = company_name
        self.team_name = team_name
        self.github_account = github_account
        self.github_repo = github_repo
        self.email_address = email_address

    def print_credits(self):
        clear(100)
        mcprint('>> About <<')
        if self.company_name:
            mcprint('Company: {}'.format(self.company_name))
        if self.team_name:
            mcprint('Developed by {}'.format(self.team_name))
        if self.authors:
            mcprint('\nAuthors:')
            for author in self.authors:
                mcprint('\t-{}'.format(author))
        print()
        if self.email_address:
            mcprint('Email: {}'.format(self.email_address))
        if self.github_account:
            mcprint('GitHub: {}'.format(self.github_account))
        if self.github_repo:
            mcprint('GitHub Repository: {}'.format(self.github_repo))
        input('\nPress Enter to Continue...')


def clear(n=3):
    print('\n' * n)


def date_generator(include_time=False, year=None, month=None, day=None, hour=None, minute=None, second=None):

    if not year:
        while True:
            try:
                year = get_input(format_='Year: ')
                if year == '':
                    year = datetime.now().year
                year = int(year)
                datetime(year, 1, 1)
                break
            except ValueError:
                logging.warning('Enter a valid year')

    if not month:
        while True:
            try:
                month = get_input(format_='Month: ')
                if month == '':
                    month = datetime.now().month
                month = int(month)
                datetime(year, month, 1)
                break
            except ValueError:
                logging.warning('Enter a valid month')

    if not day:
        while True:
            try:
                day = get_input(format_='Day: ')
                if day == '':
                    day = datetime.now().day
                day = int(day)
                datetime(year, month, day)
                break
            except ValueError:
                logging.warning('Enter a valid day')

    if not include_time:
        date = datetime(year, month, day)
        return date

    if not hour:
        while True:
            try:
                hour = get_input(format_='Hour: ')
                if hour == '':
                    hour = datetime.now().hour
                hour = int(hour)
                datetime(year, month, day, hour)
                break
            except ValueError:
                logging.warning('Enter a valid hour')

    if not minute:
        while True:
            try:
                minute = get_input(format_='Minute: ')
                if minute == '':
                    minute = datetime.now().minute
                minute = int(minute)
                datetime(year, month, day, hour, minute)
                break
            except ValueError:
                logging.warning('Enter a valid minute')

    if not second:
        while True:
            try:
                second = get_input(format_='Second: ')
                if second == '':
                    second = datetime.now().second
                second = int(second)
                datetime(year, month, day, hour, minute, second)
                break
            except ValueError:
                logging.warning('Enter a valid second')
    date = datetime(year, month, day, hour, minute, second)
    return date
