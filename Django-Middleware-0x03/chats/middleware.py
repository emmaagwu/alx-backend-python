from datetime import datetime, time
from django.http import HttpResponseForbidden, JsonResponse

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


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = {}

    def __call__(self, request):
        # Only monitor chat message submissions (POST requests)
        if request.method == 'POST' and request.path.startswith('/api/chats/'):
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Initialize if this IP is seen for the first time
            if ip not in self.message_log:
                self.message_log[ip] = []

            # Filter out timestamps older than 1 minute
            recent_times = [
                timestamp for timestamp in self.message_log[ip]
                if now - timestamp < timedelta(minutes=1)
            ]
            self.message_log[ip] = recent_times

            # Check if limit exceeded
            if len(recent_times) >= 5:
                return JsonResponse(
                    {"error": "Rate limit exceeded. You can only send 5 messages per minute."},
                    status=403
                )

            # Log current message timestamp
            self.message_log[ip].append(now)

        # Proceed to view
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Helper to get user's IP address from headers or remote address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip