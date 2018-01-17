from apscheduler.schedulers.background import BackgroundScheduler
from opsadmin import settings
import random,string
from common.mail_util import mail
from django.core.cache import cache
import hashlib
from .models.user import User


class task(object):
    def __init__(self,name,email,CellPhoneNumber,wechat,username_encrypt,username):
        self.count = 1
        self.sched = BackgroundScheduler()
        self.name = name
        self.username = username
        self.CellPhoneNumber = CellPhoneNumber
        self.email = email
        self.wechat = wechat
        self.username_encrypt = username_encrypt


    def mail_to_admin(self):

        random_code = ''.join(random.sample(string.digits + string.ascii_letters, 8))
        email_title = '授权请求'
        email_body = '''
                                            <p>%s用户请求申请成为管理员用户,请您与本人确认后进行授权</p>
                                            <p>邮件为%s.</p>
                                            <p>手机号码为%s.</p>
                                            <p>微信号码是%s.</p>
                                            <p>验证随机码 : %s</p>
                                            <p><a href="http://%s/opsadmin/user/permission/admin/authorized/%s">处理连接</a></p>

                                            ''' % (
            self.name, self.email, self.CellPhoneNumber, self.wechat,
            random_code, settings.WEBSITE_LOCATION, self.username_encrypt)
        mail_obj = mail(email_body=email_body, email_title=email_title)
        mail_obj.send_html()
        cache.set(self.username,
                  dict({'random_code': hashlib.md5(random_code.encode('utf-8')).hexdigest(), 'sign': False}),
                  30 * 60)
        self.count += 1


    def job(self):
        if cache.has_key('%s'%(self.username)):
            if dict(cache.get('%s'%(self.username))).get('sign'):
                cache.delete('%s' % (self.username))
                self.sched.shutdown(wait=False)
            elif dict(cache.get('%s'%(self.username))).get('sign') == False and self.count > settings.EMAIL_VAILD_COUNT:
                email_title = '授权超时'
                email_body = '''
                                <p>请主动联系%s用户</p>
                            ''' % (self.name)
                mail_obj = mail(email_body=email_body, email_title=email_title)
                mail_obj.send_html()
                User.objects.filter(username=self.username).update(user_role='User')
                cache.delete('%s' % (self.username))
                self.sched.shutdown(wait=False)
            else:
                self.mail_to_admin()
        else:
            self.mail_to_admin()


    def run(self):
        self.sched.add_job(self.job,'interval', minutes=settings.EMAIL_TIME_INTERVAL)
        self.sched.start()
