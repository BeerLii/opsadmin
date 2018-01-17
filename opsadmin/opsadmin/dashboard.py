from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from user.views import user_info
from opsadmin import settings
from asset.models.asset import Asset
from log.models.audit import AuditLog
from django.db.models import Count

from django.utils import timezone

class dashboard(LoginRequiredMixin,TemplateView):
    login_url = reverse_lazy('user:login')
    template_name = "index.html"

    def get_context_data(self, **kwargs):

        context = super(dashboard,self).get_context_data(**kwargs)
        context['recent_ten_access'] = []
        context['all_hosts_count'] = Asset.objects.all().count()
        context['all_user_count'] = int(user_info.get_all_user_count())
        context['alive_host_count'] = Asset.objects.filter(asset_status='Online').count()
        week_time = timezone.now() - timezone.timedelta(days=7)
        obj_list = AuditLog.objects.all().order_by('-StartTime')[:10]
        for obj in obj_list:
            context['recent_ten_access'].append({'user':obj.User,'SystemUser':obj.SystemUser,'time':obj.StartTime,'manage_ip':obj.Asset.manage_ip})
        context['week_asset_list'] = AuditLog.objects.filter(StartTime__gt=week_time).values('Asset').annotate(total=Count('Asset')).order_by('-total')[:10]
        context['week_system_user_list'] = AuditLog.objects.filter(StartTime__gt=week_time).values('User','SystemUser').annotate(total=Count('SystemUser')).order_by('-total')[:10]
        return context





class testview(TemplateView):
    template_name = 'test.html'

    def get_context_data(self, **kwargs):
        context_data = super(testview,self).get_context_data(**kwargs)

        context_data['data_path'] = "/media/asciicast.json"
        return context_data
