# -*- coding:utf-8 -*-

from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.utils.vars import load_options_vars
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager

from .callback import ResultCallback,AdHocResultCallBack
from .inventory import JMSInventory




class playbook_runner():
    def __init__(self,asset_list,yaml_file=None,asset_group=None,extra_vars=None):
        self.asset_list = asset_list
        self.yaml_file = yaml_file
        self.asset_group = asset_group
        self.extra_vars = extra_vars

    def run(self):
        loader = DataLoader()


        variable_manager = VariableManager()

        if self.asset_group != None:

            inventory = JMSInventory(host_list=self.asset_list,asset_group=self.asset_group)
        else:
            inventory = JMSInventory(host_list=self.asset_list)



        results_callback = ResultCallback()


        Options = namedtuple('Options',
                             ['connection',
                              'remote_user',
                              'ask_sudo_pass',
                              'verbosity',
                              'ack_pass',
                              'module_path',
                              'forks',
                              'become',
                              'become_method',
                              'become_user',
                              'check',
                              'listhosts',
                              'listtasks',
                              'listtags',
                              'syntax',
                              'sudo_user',
                              'sudo',
                              ])

        options = Options(connection='smart',
                          remote_user='Ansible',
                          ack_pass=None,
                          sudo_user='root',
                          forks=10,
                          sudo='yes',
                          ask_sudo_pass=False,
                          verbosity=5,
                          module_path='/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/ansible/modules/',
                          become=True,
                          become_method='sudo',
                          become_user='root',
                          check=False,
                          listhosts=None,
                          listtasks=None,
                          listtags=None,

                          syntax=None,
                          )
        if self.extra_vars != None:
            variable_manager.extra_vars = self.extra_vars
        variable_manager.options_vars = load_options_vars(options)
        variable_manager.set_inventory(inventory)
        runner = PlaybookExecutor(
            playbooks=[self.yaml_file],

            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            options=options,
            passwords=dict(vault_pass=''),
        )
        if runner._tqm:
            runner._tqm._stdout_callback = results_callback

        runner.run()
        result = results_callback.data
        runner._tqm.cleanup()

        return result

class AdHocRunner():

    def __init__(self,asset_list,task_name=None,module=None,partern='all',args=''):
        self.asset_list = asset_list
        self.module = module
        self.partern = partern
        self.args = args
        self.task_name = task_name
        self.result_callback_result = AdHocResultCallBack()

    def run(self):

        loader = DataLoader()


        variable_manager = VariableManager()



        inventory = JMSInventory(host_list=self.asset_list)

        variable_manager.set_inventory(inventory)

        # 初始化需要的对象
        Options = namedtuple('Options',
                             ['connection',
                              'remote_user',
                              'ask_sudo_pass',
                              'verbosity',
                              'ack_pass',
                              'module_path',
                              'forks',
                              'become',
                              'become_method',
                              'become_user',
                              'check',
                              'listhosts',
                              'listtasks',
                              'listtags',
                              'syntax',
                              'sudo_user',
                              'sudo'])
        options = Options(connection='smart',
                          remote_user='Ansible',
                          ack_pass=None,
                          sudo_user='root',
                          forks=10,
                          sudo='yes',
                          ask_sudo_pass=False,
                          verbosity=5,
                          module_path='/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/ansible/modules/',
                          become=True,
                          become_method='sudo',
                          become_user='root',
                          check=False,
                          listhosts=None,
                          listtasks=None,
                          listtags=None,
                          syntax=None)

        play_source =  dict(
                    name = self.task_name,
                    hosts = self.partern,
                    gather_facts = 'no',
                    tasks = [
                        dict(action=dict(module=self.module, args=self.args)),
                     ]
                )
        play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
        tqm = None

        tqm = TaskQueueManager(
                          inventory=inventory,
                          variable_manager=variable_manager,
                          loader=loader,
                          options=options,
                          passwords=dict(vault_pass=''),
                          stdout_callback=self.result_callback_result,
                      )
        try:
            tqm.run(play)
        except Exception as e:
            print('error')
        result = self.result_callback_result.result_q

        if tqm is not None:

            tqm.cleanup()

        return result