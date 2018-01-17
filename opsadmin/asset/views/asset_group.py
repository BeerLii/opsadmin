from django.views.generic import CreateView,TemplateView,DeleteView,DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from ..forms import asset_group
from asset.models.asset_group import AssetGroup

class asset_group_create(LoginRequiredMixin,CreateView):
    template_name = "asset/asset_group_create.html"
    success_url = reverse_lazy("dashboard")
    form_class = asset_group.AssetGroupForm



class asset_group_list(LoginRequiredMixin,TemplateView):
    template_name = "asset/asset_group_list.html"

    def get_context_data(self, **kwargs):
        context = super(asset_group_list,self).get_context_data(**kwargs)
        AssetGroupList = []
        asset_group_dict = {}
        for asset_group_obj in AssetGroup.objects.all():
            asset_group_dict['id'] = asset_group_obj.id
            asset_group_dict['asset_count'] = asset_group_obj.asset_set.all().count()
            asset_group_dict['asset_group_name'] = asset_group_obj.name
            asset_group_dict['asset_group_descriptions'] = asset_group_obj.descriptions
            asset_group_dict['asset_group_id'] = asset_group_obj.id
            AssetGroupList.append(asset_group_dict)

        context['asset_group_data'] = AssetGroupList
        return context

class asset_group_delete(LoginRequiredMixin,DeleteView):
    login_url = reverse_lazy('user:login')
    success_url = reverse_lazy('asset:asset_group_list')
    template_name = 'asset/asset_group_delete_confirm.html'
    model = AssetGroup

    def get_context_data(self, **kwargs):
        context = super(asset_group_delete, self).get_context_data(**kwargs)
        print(self.object.perm_set.all())
        context['perm_obj_list'] = self.object.perm_set.all()
        return context

class asset_group_detail(LoginRequiredMixin,DeleteView):
    login_url = reverse_lazy('user:login')
    model = AssetGroup
    template_name = 'asset/asset_group_detail.html'

    def get_context_data(self, **kwargs):
        context = super(asset_group_detail,self).get_context_data(**kwargs)
        context['asset_list'] = self.object.asset_set.all()
        return context







