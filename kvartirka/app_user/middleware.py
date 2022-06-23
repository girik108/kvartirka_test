import datetime
from django.core.cache import cache
from django.conf import settings


class ActiveUserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        current_user = request.user
        if current_user.is_authenticated:
            now = datetime.datetime.now()
            cache.set(f'seen_{current_user.username}',
                      now, timeout=settings.USER_LASTSEEN_TIMEOUT)

        response = self.get_response(request)

        return response


