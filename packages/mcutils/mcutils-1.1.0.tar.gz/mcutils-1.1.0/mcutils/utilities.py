from .print_manager import mcprint, Color
import logging


def clear(n=3):
    print('\n' * n)


def exit_application(text=None, enter_quit=False):
    if text:
        mcprint(text=text, color=Color.YELLOW)
    logging.info('Exiting Application Code:0')
    if enter_quit:
        input('Press Enter to exit...')
    exit(0)


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