from user.models.user import SystemUser
from opsadmin import settings
from user.util import prpcrypt
import base64
import  paramiko
from io import StringIO

class WebterminalUtil(object):
    def __init__(self,system_user_name):
        self.system_user_name = system_user_name
        self.pc = prpcrypt(settings.SECRET_KEY[0:16])

    def check_user_auth_way(self):
        data_dict = {}
        for system_user_obj in SystemUser.objects.filter(name=self.system_user_name):
            if system_user_obj.private_key:
                data_dict['private_key'] = paramiko.RSAKey.from_private_key(StringIO(system_user_obj.private_key))


            else:
                data_dict['password'] = self.pc.decrypt(base64.b64decode(system_user_obj.Password.encode('utf-8')))

        return data_dict

