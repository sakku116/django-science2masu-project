from modules import colorizeString
from datetime import datetime
from modules import writeLog
from api_app.models import RequestLog

class RequestMonitor:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        user_agent = request.META['HTTP_USER_AGENT']
        try:
            view_name = request.resolver_match.view_name
        except:
            view_name = "unknown"
        full_path = f'"{request.get_full_path()}"'
        user = f'@{request.user}'
        device = f"{user_agent[user_agent.find('(')+1:user_agent.find(')')]}"

        # print log
        log_string = f"=> ({dt_string}) = {user} | {request.method} {full_path} ({view_name}) | {device}"
        max_log = 500
        if user == '@AnonymousUser':
            color = 'white'
        else:
            color = 'yellow'
        print(colorizeString(log_string, color, reverse=True))

        # exclude bot request
        if "bot" in user_agent.lower() or "media" in user_agent.lower() or "google" in user_agent.lower():
            pass
        else:
            # limit
            logs_total = RequestLog.objects.all().count()
            if logs_total >= max_log:
                first_log = RequestLog.objects.first()
                first_log.delete()

            # save
            new_log = RequestLog.objects.create(
                ViewName = view_name,
                Path = full_path,
                Username = user,
                Device = device,
            )
            new_log.save()

        return response