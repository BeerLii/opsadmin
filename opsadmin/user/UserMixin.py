from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render_to_response


class AdminAuthorizedMixin(LoginRequiredMixin):
        def dispatch(self, request, *args, **kwargs):
            user = request.user
            if user.user_role == 'Admin' and user.admin_active:
                return super(AdminAuthorizedMixin, self).dispatch(request, *args, **kwargs)

            return render_to_response('user/deny.html')


