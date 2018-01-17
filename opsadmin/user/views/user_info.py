from ..models import user
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from user.models import user


def get_alive_user():
    count = 0
    alive_user_list = []
    for obj in user.User.objects.all():
        if obj.is_online:
            count = count + 1
            alive_user_list.append(obj.get_name)
    return {'alive_user_count':count,'alive_user_list':alive_user_list}




def get_all_user_count():
    return len(user.User.objects.all())



class myuser_info(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('user:login')
    model = user.User
    context_object_name = 'user_info_list'
    template_name = 'user/user_info.html'





