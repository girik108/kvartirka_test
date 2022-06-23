import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.cache import cache 


class User(AbstractUser):


    def last_seen(self):
        return cache.get(f'seen_{self.username}')

    @property
    def is_online(self):
        last_seen = self.last_seen()
        if not last_seen:
            return False
        now = datetime.datetime.now()

        return now <= last_seen + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT)
