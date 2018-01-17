from django.utils.deprecation import MiddlewareMixin
from .models.user import User
import datetime
from django.core.cache import cache
from opsadmin import settings
class ActiveUserMiddleware(MiddlewareMixin):
    def process_request(self,request):


        if request.user.is_authenticated() and not request.user.is_anonymous():
            now = datetime.datetime.now()
            cache.set('%s_last_time' % (request.user),now,settings.USER_LASTSEEN_TIMEOUT)
            cache.get('%s_last_time' % (request.user))
        return None
