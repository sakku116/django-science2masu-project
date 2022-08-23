from termcolor import colored

def customLogInfo(path, view_name, user_agent, user, device, dt_string):
    text = f"=> ({dt_string}) = {user} | {path} ({view_name}) | {device}"

    if user == '@AnonymousUser':
        color = 'white'
    else:
        color = 'yellow'

    return colored(text, color, attrs=['reverse'])