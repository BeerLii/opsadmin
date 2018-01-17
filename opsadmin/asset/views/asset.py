from django.views.generic import CreateView,ListView,TemplateView,View,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render_to_response
from ..forms.asset import AssetCreateForm
from ..models.asset import Asset
from perm.models import perm


class Asset_Create(LoginRequiredMixin,CreateView):
    login_url = reverse_lazy('user:login')
    form_class = AssetCreateForm
    template_name = 'asset/asset_create.html'
    success_url = reverse_lazy('dashboard')


class Asset_List(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('user:login')
    model = Asset
    template_name = 'asset/asset_list.html'
    context_object_name = "asset_list"

class Asset_Delete(LoginRequiredMixin,DeleteView):
    login_url = reverse_lazy('user:login')
    template_name = 'asset/asset_delete_confirm.html'
    model = Asset
    success_url = reverse_lazy('asset:asset_list')



class Asset_Detail(LoginRequiredMixin,TemplateView):
    login_url = reverse_lazy('user:login')
    template_name = 'asset/asset_detail.html'

    def get_context_data(self, **kwargs):
        if not self.request.GET['name']:
            raise ValueError('have no name value')
        asset_list = Asset.objects.filter(name=self.request.GET['name'])
        asset_data = {}
        for asset in asset_list:
            asset_data['asset_obj'] = asset
            asset_data['server_obj'] = asset.server
            asset_data['cpu_obj'] = asset.cpu
            asset_data['nic_obj'] = asset.nic_set.all()
            asset_data['ram_obj'] = asset.ram_set.all()
        context = super(Asset_Detail, self).get_context_data(**kwargs)
        context.update(asset_data)
        return context

class Asset_Connect(LoginRequiredMixin,View):
    login_url = reverse_lazy('user:login')

    def get(self,request,perm_name,asset_name,system_user):
        data_dict = {}
        data_dict['system_user_name'] = system_user
        data_dict['asset_name'] = asset_name
        data_dict['user'] = request.user.username
        data_dict['request'] = request
        for asset_obj in Asset.objects.filter(name=asset_name):
            data_dict['manage_ip'] = asset_obj.manage_ip

        for perm_obj in perm.objects.filter(name=perm_name):
            data_dict['asset_group_name'] = perm_obj.asset_group.name
            data_dict['system_user_perm'] = perm_obj.perm

        return render_to_response('asset/asset_connect.html',data_dict)







