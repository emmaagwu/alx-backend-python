from datetime import datetime

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