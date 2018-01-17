from common import util
from common.ansible import task
from opsadmin import settings
from user.util import prpcrypt
import base64

class perm_util(object):
    def __init__(self,asset_group_obj=None,system_user_obj=None,perm=None):
        self.asset_group_obj = asset_group_obj
        self.system_user_obj = system_user_obj
        self.perm = perm
        self.pc = prpcrypt(settings.SECRET_KEY[0:16])

    def get_public_key(self):
        private_key = self.system_user_obj.private_key
        public_key = util.ssh_pubkey_gen(private_key=private_key)
        return public_key

    def get_extra_vars(self):
        extra_vars = {}
        if self.perm == 'Admin':
            extra_vars['admin_group'] = settings.SYSTEM_USER_ADMIN_GROUP
        elif self.perm == 'Comman':
            extra_vars['admin_group'] = ''
        extra_vars['groupname'] = extra_vars['username'] = self.system_user_obj.UserName
        print(self.system_user_obj.private_key)
        if  self.system_user_obj.private_key:
            extra_vars['key_data'] = self.get_public_key()
            if self.system_user_obj.Password:
                extra_vars['password'] = self.pc.decrypt(base64.b64decode(self.system_user_obj.Password.encode('utf-8')))
        else:

            extra_vars['password'] = self.pc.decrypt(base64.b64decode(self.system_user_obj.Password.encode('utf-8')))

        print(extra_vars)
        return extra_vars

    def start(self):
        asset_list = self.asset_group_obj.asset_set.all()
        extra_vars = self.get_extra_vars()
        playbook_task_obj = task.PlayBookTask(asset_list=asset_list,asset_group=self.asset_group_obj,extra_vars=extra_vars,yaml_file='%s/common/ansible/playbook/AddUser.yaml'%(settings.BASE_DIR))
        result = playbook_task_obj.run()
        print(result)

