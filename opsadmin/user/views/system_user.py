from django.views.generic import CreateView,ListView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from ..forms import SystemUserForm,SystemUserUpdateForm
from ..models.user import SystemUser


class create_system_user(LoginRequiredMixin,CreateView):
    login_url = reverse_lazy('user:login')
    template_name = 'user/system_user_create.html'
    form_class = SystemUserForm.SystemUserCreateForm
    success_url = reverse_lazy('dashboard')


    def form_valid(self, form):
        # role = form.cleaned_data['user_role']
        # if role == 'Admin':
        #     email_title = '%s用户注册系统用户' % (self.request.user)
        #     email_body = '用户注册的系统用户角色是管理员,请您确认'
        #     email = '735964033@qq.com'
        #     send_status = send_mail(email_title, email_body,'2710417389@qq.com',[email])

        form.cleaned_data['request'] = self.request
        return super(create_system_user, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        mutable = request.POST._mutable
        request.POST._mutable = True
        if request.FILES:
            file = str(request.FILES['private_key_file'].read(),encoding='utf-8')
            request.POST['private_key'] = file
        else:
            request.POST['private_key'] = ''
        request.POST._mutable = mutable
        return super(create_system_user,self).post(request,*args,**kwargs)


class system_user_list(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('user:login')
    template_name = 'user/system_user_list.html'
    context_object_name = 'system_user_list'

    def get_queryset(self):
        queryset = self.request.user.SystemUser_ID.all()
        return queryset

class system_user_update(LoginRequiredMixin,UpdateView):
    login_url = reverse_lazy('user:login')
    template_name = 'user/system_user_update.html'
    model = SystemUser
    form_class = SystemUserUpdateForm.SystemUserUpdateForm

class system_user_delete(LoginRequiredMixin,DeleteView):
    login_url = reverse_lazy('user:login')
    template_name = 'user/system_user_delete_confirm.html'
    model = SystemUser
    success_url = reverse_lazy('user:system_user_list')

    def post(self, request, *args, **kwargs):

        return super(system_user_delete,self).post(request,*args,kwargs)






