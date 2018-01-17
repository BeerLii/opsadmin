from django.views.generic import CreateView,ListView,View,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render_to_response
from .forms import perm_form
from django.urls import reverse_lazy
from .models import perm
from .perm_util import perm_util



class create_perm(LoginRequiredMixin,CreateView):
    login_url = reverse_lazy('user:login')
    template_name = 'perm/perm_create.html'
    form_class = perm_form
    success_url = reverse_lazy('dashboard')

    def __init__(self,*args,**kwargs):
        self.perm_obj = perm()
        super(create_perm,self).__init__(*args,**kwargs)


    def get_form_kwargs(self):
        kwargs = super(create_perm,self).get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs
    

    def form_valid(self, form):
        perm = self.perm_obj
        perm.name = form.cleaned_data.get('name', '')
        perm.descriptions = form.cleaned_data.get('descriptions', '')
        perm.perm = form.cleaned_data.get('perm', '')
        perm.asset_group = form.cleaned_data.get('asset_group_choices', '')
        perm.SystemUser = form.cleaned_data.get('system_user_choices', '')

        perm.create_perm_user = self.request.user
        perm.save()
        perm_util_obj = perm_util(asset_group_obj=perm.asset_group,system_user_obj=perm.SystemUser,perm=form.cleaned_data.get('perm', ''))
        perm_util_obj.start()
        return super(create_perm, self).form_valid(form)

class list_perm(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('user:login')
    template_name = 'perm/perm_list.html'
    context_object_name = "perm_list"


    def get_queryset(self):
        queryset = perm.objects.filter(create_perm_user=self.request.user)
        return queryset


class perm_asset_host_connect_list(LoginRequiredMixin,View):

    def get(self,request,name):
        data_dict = {}
        for perm_obj in perm.objects.filter(name=name):
            data_dict['perm_name'] = perm_obj.name
            data_dict['system_user_name'] = perm_obj.SystemUser.name
            data_dict['asset_host_list'] = perm_obj.asset_group.asset_set.all()
            data_dict['request'] = request
        return render_to_response('perm/perm_asset_host_connect_list.html',data_dict)

class delete_perm(LoginRequiredMixin,DeleteView):
    login_url = reverse_lazy('user:login')
    model = perm
    success_url = reverse_lazy('perm:perm_list')
    template_name = 'perm/delete_confirm.html'









