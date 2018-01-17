from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from .. import models
from common import asset_util
from common.ansible import task
from opsadmin import settings

import re

class collect_asset(APIView):

    def post(self, request, format=None):
        asset_name = request.POST['asset_name']
        asset_list = models.Asset.objects.filter(name=asset_name)
        task_obj = task.PlayBookTask(asset_list=asset_list,yaml_file='%s/comman/ansible/playbook/collect.yaml'%(settings.BASE_DIR),extra_vars={'sysinfo_file':'%s/comman/ansible/plugin/sysinfo.py'%(settings.BASE_DIR)})
        result = task_obj.run()


        asset_data = re.sub('\'','\"',result['%s' % (asset_list[0].manage_ip)]['stdout'])
        asset_data = re.sub('None','\"None\"',asset_data)
        util_obj = asset_util.ServerAssetEntry(asset_obj=asset_list[0],asset_data=json.loads(asset_data))
        util_obj.save()
        return Response('ok')


class delete_asset(APIView):

    def delete(self,request,pk,format=None):
        asset_obj = models.Asset.objects.get(pk=pk)
        asset_obj.delete()
        return Response('ok')

class delete_asset_group(APIView):
    def delete(self,request,pk,format=None):
        asset_group_obj = models.AssetGroup.objects.get(pk=pk)
        asset_group_obj.delete()
        return Response('ok')