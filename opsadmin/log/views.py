from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,DetailView,DeleteView
from django.urls import reverse_lazy
from .models.audit import AuditLog
from opsadmin import settings
import os

class SessionActionList(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('user:login')
    template_name = 'log/session_action_list.html'
    context_object_name = 'session_action_list'

    def get_queryset(self):
        queryset = AuditLog.objects.all()
        return queryset

class SessionActionDetail(LoginRequiredMixin,DetailView):
    login_url = reverse_lazy('user:login')
    model = AuditLog
    template_name = 'log/session_action_replay.html'
    context_object_name = 'log_obj'

    def get_context_data(self, **kwargs):
        audit_log_obj = kwargs['object']
        kwargs['log_path'] = '%s/%s-%s-%s/%s.json'%(settings.media,audit_log_obj.StartTime.year,audit_log_obj.StartTime.month,audit_log_obj.StartTime.day,audit_log_obj.LogId)

        return super(SessionActionDetail,self).get_context_data(**kwargs)


class SessionActionDelete(LoginRequiredMixin,DeleteView):
    login_url = reverse_lazy('user:login')
    model = AuditLog
    template_name = 'log/delete_confirm.html'
    success_url = reverse_lazy('log:session_action_list')

    def post(self, request, *args, **kwargs):
        audit_log_obj = AuditLog.objects.filter(id=kwargs['pk'])[0]
        log_path = '%s/%s-%s-%s/%s.json'%(settings.MEDIA_ROOT,audit_log_obj.StartTime.year,audit_log_obj.StartTime.month,audit_log_obj.StartTime.day,audit_log_obj.LogId)
        if(os.path.exists(log_path)):
            os.remove(log_path)
        return super(SessionActionDelete,self).post(request,*args,**kwargs)




