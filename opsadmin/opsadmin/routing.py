from channels.routing import route, route_class
from channels.generic.websockets import WebsocketConsumer
import paramiko
import time
from webterminal import consumer

# def message_handler(message):
#     print(message.content['text'])
#     message.content['text']
# sshclient = paramiko.SSHClient()
# sshclient.load_system_host_keys()
# sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# sshclient.connect('192.168.92.129', 22, 'root', 'lbw13534464110')
# chan = sshclient.invoke_shell(term='xterm')
# while True:
#     data = chan.recv(1024)
#
# chan.send(message.content['text'])

# print(message.content['text'])


class MyConsumer(WebsocketConsumer):
    http_user = True  # 设置为 ``True`` 将会自动从 HTTP cookie 中登录用户，因此可以省去 channel_session_user 的设置。
    strict_ordering = False  # 默认设置

    def connect(self, message, **kw):
        """连接开始
        """

        sshclient = paramiko.SSHClient()
        sshclient.load_system_host_keys()
        sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshclient.connect('192.168.5.138', 22, 'root', 'lbw13534464110')
        chan = sshclient.invoke_shell(term='xterm')
        MyConsumer.chan = chan
        send_data = ''

        # while True:
        #     data = chan.recv(1024)
        #     print(data)
        #     if not len(str(data,encoding='utf-8')):
        #         break
        #     send_data = send_data + str(data,encoding='utf-8')
        # print("yes")

        self.message.reply_channel.send({'accept': True})

    def receive(self, text=None, bytes=None, **kw):
        """接收到信息时调用的函数
        """
        my_data = text + '\n'
        print(len(my_data))
        MyConsumer.chan.send(my_data)
        time.sleep(0.5)
        send_data = ''
        print(MyConsumer.chan.recv_ready())
        while True:

            if MyConsumer.chan.recv_ready():
                data = MyConsumer.chan.recv(9999)
                print(data)
                send_data = send_data + str(data, encoding='utf-8')
            else:
                break
        self.send(text=send_data.replace(text, ''), bytes=bytes)

    def disconnect(self, message, **kw):
        """断开连接时将会被调用
        """
        MyConsumer.chan.close()


channel_routing = [
    route_class(consumer.webterminal, path=r"/webterminal/$"),
]