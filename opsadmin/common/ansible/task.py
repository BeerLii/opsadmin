from .run import playbook_runner
import json


class PlayBookTask(object):
    def __init__(self,asset_list=None,yaml_file=None,asset_group=None,extra_vars=None):
        self.asset_list = list(asset_list)
        self.yaml_file = yaml_file
        self.asset_group = asset_group
        self.extra_vars = extra_vars
        self.check_args()

    def check_args(self):
        if self.asset_list == None:
            raise ValueError('资产列表为空')

        if self.yaml_file == None:
            raise ValueError('剧本文件不存在')

    def run(self):
        playbook_run_obj = playbook_runner(asset_list=self.asset_list,yaml_file=self.yaml_file,asset_group=self.asset_group,extra_vars=self.extra_vars)
        result = playbook_run_obj.run()
        result = json.loads(result)
        return result