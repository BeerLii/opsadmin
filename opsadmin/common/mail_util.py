from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

from opsadmin import settings

#email_title = '%s用户注册系统用户' % (self.request.user)


#     email_body = '用户注册的系统用户角色是管理员,请您确认'
#     email = '735964033@qq.com'
#     send_status = send_mail(email_title, email_body,'2710417389@qq.com',[email])

class mail(object):
    def __init__(self,email_title=None,email_body=None):
        self.email_titile = email_title
        self.email_body = email_body
        self.email = settings.ADMIN_EMAIL
        self.from_eamil = settings.EMAIL_FROM

    def send(self):
        send_status = send_mail(self.email_titile,self.email_body,self.from_eamil,[self.email])
        if send_status != 1:
            raise ValueError('邮件发送失败')

    def send_html(self):
        msg = EmailMultiAlternatives(self.email_titile,self.email_body,self.from_eamil,[self.email])
        msg.content_subtype = "html"
        msg.send()
