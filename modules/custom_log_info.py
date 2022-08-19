from termcolor import colored
from datetime import datetime

def customLogInfo(path, view_name, user_agent, user):
    path = f'"{path}"'
    user = f'@{user}'
    device = f"{user_agent[user_agent.find('(')+1:user_agent.find(')')]}"

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    text = f"=> ({dt_string}) = {user} | {path} ({view_name}) | {device}"

    if user == '@AnonymousUser':
        color = 'white'
    else:
        color = 'yellow'

    return colored(text, color, attrs=['reverse'])