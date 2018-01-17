from ..models.user import User
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from ..forms.UserUpdateForm import UserUpdateForm

class user_update(LoginRequiredMixin,UpdateView):
    login_url = reverse_lazy('user:login')
    model = User
    template_name = 'user/user_message_update.html'
    success_url = reverse_lazy('user:info')
    form_class = UserUpdateForm



