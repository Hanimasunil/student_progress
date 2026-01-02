from django.shortcuts import redirect
from django.conf import settings

class LoginRequiredMiddleware:
    """
    Force login for all dashboard views except login, signup, verify-otp, admin, static
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_paths = [
            '/', '/signup/', '/verify-otp/', '/admin/', '/static/'
        ]
        if not request.user.is_authenticated and not any(request.path.startswith(p) for p in allowed_paths):
            return redirect(settings.LOGIN_URL)
        return self.get_response(request)
