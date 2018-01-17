# ~*~ coding: utf-8 ~*~
from ansible.inventory import Inventory, Host, Group
from ansible.vars import VariableManager
from ansible.parsing.dataloader import DataLoader
from opsadmin import settings

class JMSHost(Host):
    def __init__(self, asset=None):

        self.asset = asset
        self.name = name = asset.manage_ip
        self.port = port = 22

        super(JMSHost, self).__init__(name, port)
        self.set_all_variable()

    def set_all_variable(self):
        asset = self.asset
        self.set_variable('ansible_host', self.name)
        self.set_variable('ansible_port', self.port)
        self.set_variable('ansible_user', settings.ANSIBLE_USER)
        self.set_variable('ansible_ssh_private_key_file', settings.ANSIBLE_PRIVATE_KEY)
        self.set_variable("ansible_become", True)
        self.set_variable("ansible_become_method", 'sudo')
        self.set_variable("ansible_become_user", 'root')




class JMSInventory(Inventory):

    def __init__(self, host_list=None,asset_group=None):
        if host_list is None:
            host_list = []
        assert isinstance(host_list, list)
        self.host_list = host_list
        self.asset_group = asset_group
        self.loader = DataLoader()
        self.variable_manager = VariableManager()
        super(JMSInventory, self).__init__(self.loader, self.variable_manager,
                                           host_list=host_list)

    def parse_inventory(self, host_list):
        ungrouped = Group('ungrouped')
        all = Group('all')
        all.add_child_group(ungrouped)
        self.groups = dict(all=all, ungrouped=ungrouped)

        for asset in host_list:
            host = JMSHost(asset=asset)

            if self.asset_group != None:
                    if  self.asset_group.name not in self.groups:
                        group = Group(self.asset_group.name)
                        self.groups[self.asset_group.name] = group
                    else:
                        group = self.groups[self.asset_group.name]
                    group.add_host(host)
            else:
                ungrouped.add_host(host)
            all.add_host(host)

