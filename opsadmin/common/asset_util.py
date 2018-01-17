# [
#             "{'wake_up_type': 'Power Switch', 'uuid': '1BBF4D56-71FA-1E35-C40F-6B2628342EA0', 'os_release': 'CentOS release 6.5 (Final)', 'cpu_count': '1',"
#             " 'ram': [{'slot': 'RAM slot #0', 'capacity': '1024', 'manufactory': 'Not Specified', 'asset_tag': 'Not Specified', 'sn': 'Not Specified', 'model': 'DRAM'}], "
#             "'cpu_model': 'Intel(R) Core(TM) i7-7700HQ CPU @ 2.80GHz', 'manufactory': 'VMware, Inc.', "
#             "'physical_disk_driver': [], "
#             "'sn': 'VMware-56 4d bf 1b fa 71 35 1e-c4 0f 6b 26 28 34 2e a0', 'cpu_core_count': '', "
#             "'nic': [{'macaddress': 'E2:5D:6D:A4:1D:1A', 'name': 'pan0', 'netmask': None, 'bonding': 0, 'model': 'unknown', 'ipaddress': None, 'network': None}, {'macaddress': '00:0C:29:34:2E:A0', 'name': 'eth0', 'netmask': '255.255.255.0', 'bonding': 0, 'model': 'unknown', 'ipaddress': '192.168.5.138', 'network': '192.168.5.255'}], "
#             "'model': 'VMware Virtual Platform', 'os_distribution': 'CentOS', 'os_type': 'linux', 'ram_size': 980}"
#         ]


from asset.models import asset


class ServerAssetEntry(object):
    def __init__(self,asset_obj=None,asset_data=None):
        self.asset_obj = asset_obj
        self.asset_data = asset_data


    def server(self):
        server_dict = dict({
            'model':self.asset_data['model'],
            'os_type' : self.asset_data['os_type'],
            'os_distribution':self.asset_data['os_distribution'],
            'os_release' : self.asset_data['os_release'],
            'sn': self.asset_data['sn'],
            'asset' : self.asset_obj,
        })

        server_obj = asset.Server(**server_dict)
        server_obj.save()

    def cpu(self):
        cpu_dict = dict(
            {
                'asset':self.asset_obj,
                'cpu_model':self.asset_data['cpu_model'],
                'cpu_count':self.asset_data['cpu_count'],
                'cpu_core_count':self.asset_data['cpu_core_count'],
            }
        )

        cpu_obj = asset.CPU(**cpu_dict)
        cpu_obj.save()

    def ram(self):
        for ram_data in self.asset_data['ram']:
            ram_dict = dict(
                {
                    'asset':self.asset_obj,
                    'sn':ram_data['sn'],
                    'model':ram_data['model'],
                    'slot':ram_data['slot'],
                    'capacity':ram_data['capacity'],
                }
            )
            ram_obj = asset.RAM(**ram_dict)
            ram_obj.save()

    def nic(self):
        for nic_data in self.asset_data['nic']:
            nic_dict = dict({
                'asset':self.asset_obj,
                'name':nic_data['name'],
                'model':nic_data['model'],
                'macaddress':nic_data['macaddress'],
                'ipaddress':nic_data['ipaddress'],
                'netmask':nic_data['netmask'],
                'bonding':nic_data['bonding'],
            })

            nic_obj = asset.NIC(**nic_dict)
            nic_obj.save()

    def save(self):
        self.server()
        self.cpu()
        self.ram()
        self.nic()
