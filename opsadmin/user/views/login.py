from django.views.generic import FormView
from ..forms import AuthForm
from django.shortcuts import redirect,reverse
from django.contrib.auth import login as auth_login , logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect



@method_decorator(csrf_protect, name='dispatch')
class UserLoginView(FormView):
    template_name = "user/login.html"
    form_class = AuthForm.UserLoginForm

    def get(self, request, *args, **kwargs):

        if request.user.is_staff:
            return redirect(reverse('dashboard'))
        return super(UserLoginView,self).get(request,*args,**kwargs)

    def form_valid(self, form):

        auth_login(self.request,form.get_user())

        return redirect(reverse('dashboard'))