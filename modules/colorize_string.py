from termcolor import colored

def colorizeString(string="", color="", reverse=True):
    if reverse:
        return colored(string, color, attrs=['reverse'])
    else:
        return colored(string, color)