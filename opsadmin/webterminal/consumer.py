from channels.generic.websockets import WebsocketConsumer
import json
import paramiko
from .interactive import get_redis_instance,SshTerminalThread,InterActiveShellThread
from .util import WebterminalUtil
from asset.models.asset import Asset
from log.models.audit import AuditLog
from django.utils.timezone import now
import os
class webterminal(WebsocketConsumer):
    ssh = paramiko.SSHClient()
    http_user = True
    http_user_and_session = True
    channel_session = True
    channel_session_user = True

    def connect(self, message):

        self.message.reply_channel.send({"accept": True})
        # permission auth
        self.message.reply_channel.send({"text": json.dumps(['stdout', '************按exit来退出远程链接主机*************\r\n'])},immediately=True)

    def disconnect(self, message):
        # close threading
        self.closessh()
        self.message.reply_channel.send({"accept": False})
        self.close()


    def queue(self):
        queue = get_redis_instance()
        channel = queue.pubsub()
        return queue

    def closessh(self):
        # close threading
        try:
            self.queue().publish(self.message.reply_channel.name, 'close')
        except Exception as e:
            pass

    def receive(self, text=None, bytes=None, **kwargs):

            if text:
                data = json.loads(text)

                if 'login' in data:
                    data_dict = WebterminalUtil(data['login']['system_user_name']).check_user_auth_way()

                    self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    if 'private_key' in data_dict:
                        self.ssh.connect(hostname=data['login']['manage_ip'], port=22, username=data['login']['system_user_name'],pkey=data_dict['private_key'],timeout=3)
                    elif 'password' in data_dict:

                        self.ssh.connect(hostname=data['login']['manage_ip'], port=22, username=data['login']['system_user_name'], password=data_dict['password'], timeout=3)

                    chan = self.ssh.invoke_shell(term='xterm',width=90, height=40, )
                    asset_obj = Asset.objects.get(name=data['login']['asset_name'])
                    audit_log_obj = AuditLog.objects.create(User=data['login']['user'],
                                            SystemUser=data['login']['system_user_name'],
                                            SystemUserPerm=data['login']['system_user_perm'],
                                            AssetGroup=data['login']['asset_group_name'],
                                            Asset=asset_obj)
                    audit_log_obj.save()
                    directory_date_time = now()
                    log_name = os.path.join('{0}-{1}-{2}'.format(directory_date_time.year,directory_date_time.month,directory_date_time.day),'{0}.json'.format(audit_log_obj.LogId))


                    t1 = SshTerminalThread(self.message, chan,log_name)
                    t1.setDaemon = True
                    t1.start()

                    interactive_thread = InterActiveShellThread(chan=chan, channel=self.message.reply_channel.name,log_name=log_name,log_obj=audit_log_obj)
                    interactive_thread.setDaemon = True
                    interactive_thread.start()



                elif 'stdin' in data:

                    self.queue().publish(self.message.reply_channel.name, json.loads(text)['stdin'])


                else:
                    self.message.reply_channel.send(
                        {"text": json.dumps(['stdout', '\033[1;3;31mUnknow command found!\033[0m'])}, immediately=True)
            elif bytes:
                self.queue().publish(self.message.reply_channel.name, json.loads(bytes)[1])


