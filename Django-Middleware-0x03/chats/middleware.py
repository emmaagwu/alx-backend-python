from datetime import datetime, time
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}\n"

        # Write to log file
        with open("requests.log", "a") as log_file:
            log_file.write(log_entry)

        # Continue to the next middleware or view
        response = self.get_response(request)
        return response
    
    
    
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define allowed hours (6PM to 9PM)
        start_time = time(18, 0, 0)  # 6:00 PM
        end_time = time(21, 0, 0)    # 9:00 PM

        current_time = datetime.now().time()

        # Only restrict access to specific app paths if needed
        if request.path.startswith('/chat/') or 'chat' in request.path.lower():
            if not (start_time <= current_time <= end_time):
                return HttpResponseForbidden("Access to chat is only allowed between 6PM and 9PM.")

        return self.get_response(request)