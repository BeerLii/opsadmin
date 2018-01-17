import threading
import sys
import json
import socket
import time
import os
import errno
try:
    import termios
    import tty
    has_termios = True
except ImportError:
    has_termios = False

from opsadmin import settings
from django.utils import timezone


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass

class CustomeFloatEncoder(json.JSONEncoder):
    def encode(self, obj):
        if isinstance(obj, float):
            return format(obj, '.6f')
        return json.JSONEncoder.encode(self, obj)


def get_redis_instance():
    from .asgi import channel_layer
    return channel_layer._connection_list[0]

def interactive_shell(chan,channel,log_name=None,width=90,height=40):
    if has_termios:
        posix_shell(chan,channel,log_name=log_name,width=width,height=height)
    else:
        sys.exit(1)

def posix_shell(chan,channel,log_name=None,width=90,height=40,log_obj=None):
    from .asgi import channel_layer
    stdout = list()
    begin_time = time.time()
    last_write_time = {'last_activity_time': begin_time}
    try:
        chan.settimeout(0.0)
        while True:

            try:
                x = chan.recv(9999)
                x = str(x,encoding='utf-8')
                if len(x) == 0:
                    channel_layer.send(channel, {'text': json.dumps(['disconnect', str('\r\n*** EOF\r\n')])})
                    break
                now = time.time()

                delay = now - last_write_time['last_activity_time']
                last_write_time['last_activity_time'] = now

                if x == "exit\r\n" or x == "\r\nlogout\r\n" or x == 'logout' or x == 'logout\r\n':
                        channel_layer.send(channel,{'text':json.dumps(['disconnect',str('\r\n*** EOF ***\r\n')])})
                        stdout.append([delay, x])
                        chan.close()
                else:
                        stdout.append([delay, x])

                channel_layer.send(channel, {'text': json.dumps(['stdout' , x])})

            except socket.timeout:
                pass

    finally:

        attrs = {
            "version": 1,
            "width": width,
            "height": height,
            "duration": round(time.time() - begin_time, 6),
            "command": os.environ.get('SHELL', None),
            'title': None,
            "env": {
                "TERM": os.environ.get('TERM'),
                "SHELL": os.environ.get('SHELL', 'sh')
            },
            'stdout': list(stdout)
        }
        mkdir_p('/'.join(os.path.join(settings.MEDIA_ROOT, log_name).rsplit('/')[0:-1]))
        with open(os.path.join(settings.MEDIA_ROOT, log_name), "a") as f:
            f.write(json.dumps(attrs,ensure_ascii=True,cls=CustomeFloatEncoder,indent=2))
        log_obj.EndTime = timezone.now()
        log_obj.save()
        queue = get_redis_instance()
        redis_channel = queue.pubsub()
        queue.publish(channel, 'close')




class SshTerminalThread(threading.Thread):

    def __init__(self,message,chan,log_name):
        super(SshTerminalThread, self).__init__()
        self._stop_event = threading.Event()
        self.message = message
        self.queue = self.redis_queue()
        self.chan = chan
        self.log_name = log_name

    def redis_queue(self):
        redis_instance = get_redis_instance()
        redis_sub = redis_instance.pubsub()
        redis_sub.subscribe(self.message.reply_channel.name)
        return redis_sub

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        first_flag = True
        while (not self._stop_event.is_set()):
            text = self.queue.get_message()

            if text:

                data = text['data']

                if isinstance(data, int):
                    if data == 1 and first_flag:
                        first_flag = False
                    else:
                        self.chan.send(str(data))

                else:
                    print('stdin-----%s' % (bytes.decode(data)))
                    if data == b'close':

                        if self.chan.closed == False:
                            self.chan.close()
                        self.stop()


                    else:

                        self.chan.send(bytes.decode(data))



class InterActiveShellThread(threading.Thread):
    def __init__(self,chan,channel,log_name=None,width=90,height=40,log_obj=None):
        super(InterActiveShellThread,self).__init__()
        self.chan = chan
        self.channel = channel
        self.log_name = log_name
        self.width = width
        self.height = height
        self.log_obj = log_obj


    def run(self):
        posix_shell(chan=self.chan,channel=self.channel,log_name=self.log_name,width=self.width,height=self.height,log_obj=self.log_obj)

