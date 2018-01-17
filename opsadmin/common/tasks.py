from __future__ import absolute_import
from opsadmin import celery_app
from asset.models.asset import Asset
from .ansible.run import AdHocRunner

from celery.signals import worker_process_init

@worker_process_init.connect
def fix_multiprocessing(**_):
  from multiprocessing import current_process
  try:
    current_process()._config
  except AttributeError:
    current_process()._config = {'semprefix': '/mp'}




@celery_app.task(name='tasks.host_alive')
def CheckHostAlive():

    asset_list = list(Asset.objects.all())
    adhoc_obj = AdHocRunner(asset_list=asset_list, task_name='CheckHostAlive', module='ping')
    result = adhoc_obj.run()
    if len(result['contacted']) > 0:
        for alive_host in result['contacted']:
            Asset.objects.filter(manage_ip=alive_host).update(asset_status='Online')
    if len(result['dark']) > 0:
        for not_alvie_host in result['dark']:
            Asset.objects.filter(manage_ip=not_alvie_host).update(asset_status='Not Online')





