from modules import colorizeString
from datetime import datetime
from utils import writeLog
import threading

class RequestMonitor:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")        
        user_agent = request.META['HTTP_USER_AGENT']
        view_name = request.resolver_match.view_name
        full_path = f'"{request.get_full_path()}"'
        user = f'@{request.user}'
        device = f"{user_agent[user_agent.find('(')+1:user_agent.find(')')]}"

        log_string = f"=> ({dt_string}) = {user} | {full_path} ({view_name}) | {device}"
        max_log_line = 5
        
        if user == '@AnonymousUser':
            color = 'white'
        else:
            color = 'yellow'
        print(colorizeString(log_string, color, reverse=True))

        # save log with threading
        write_log_thread = threading.Thread(target=writeLog, args=(log_string, 10,))
        write_log_thread.start()

        return response