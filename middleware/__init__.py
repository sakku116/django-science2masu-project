from modules import customLogInfo

class RequestMonitor:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        full_path = request.get_full_path()
        user_agent = request.META['HTTP_USER_AGENT']
        user = request.user
        print(customLogInfo(full_path, request.resolver_match.view_name, user_agent, user))

        return response