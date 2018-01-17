from django.views.generic import CreateView
from ..forms import RegisterForm
from django.urls import reverse_lazy
from ..util import prpcrypt
from ..time_task import task
from opsadmin import settings
import base64



class UserRegisterView(CreateView):
    template_name = "user/register.html"
    form_class = RegisterForm.RegisterUserForm
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        form_obj_data = form.cleaned_data
        if form_obj_data['user_role'] == 'Admin':
            username_encrypt = str(base64.b64encode(bytes(form.cleaned_data['username'],encoding='utf-8')),encoding='utf-8')
            task_obj = task(username_encrypt=username_encrypt,name=form.cleaned_data['name'],wechat=form.cleaned_data['wechat'],CellPhoneNumber=form.cleaned_data['CellPhoneNumber'],email=form.cleaned_data['email'],username=form.cleaned_data['username'])
            task_obj.run()
        return super(UserRegisterView,self).form_valid(form)

