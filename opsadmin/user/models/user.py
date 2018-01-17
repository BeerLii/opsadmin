from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import UserManager
from django.core.cache import cache
import datetime
from opsadmin import settings




class SystemUser(models.Model):
    name = models.CharField(max_length=50,unique=True,null=True,verbose_name=_('Name'))
    UserName = models.CharField(max_length=50,unique=True,verbose_name=_('UserName'))
    Password = models.CharField(max_length=100,blank=True,null=True,verbose_name=('Password'))
    CreateTime = models.DateTimeField(auto_now_add=True,verbose_name=_('CreateTime'))
    description = models.TextField(null=True,blank=True)
    private_key = models.TextField(null=True,blank=True)
    public_key = models.TextField(null=True,blank=True)


    @property
    def get_password(slef):
        raise AttributeError('Password raw is not a readable attribute')

    @get_password.setter
    def get_password(self,password):
        self.Password = password



class User(AbstractBaseUser):
    ROLE_CHOICES = (
        ('Admin', 'Administrator'),
        ('User', 'CommonUser')

    )

    DEPARTMENT_CHOICES = (
        ('ops', 'Operation Engineer'),
        ('dev', 'Development Engineer')
    )

    username = models.CharField(max_length=50,unique=True,verbose_name=_('username'))
    email = models.EmailField(max_length=30,unique=True,verbose_name=_('email'))
    name = models.CharField(max_length=50,unique=True,verbose_name=_('name'))
    user_role = models.CharField(choices=ROLE_CHOICES,max_length=10,verbose_name=_('role'))
    department = models.CharField(choices=DEPARTMENT_CHOICES,max_length=30,null=True,verbose_name=_('department'))
    wechat = models.CharField(max_length=30,blank=True,verbose_name=_('wechat'))
    CellPhoneNumber = models.CharField(max_length=30,blank=True,verbose_name=_('CellPhoneNumber'))
    CreateTime = models.DateTimeField(auto_now_add=True,verbose_name=_('CreateTime'))
    SystemUser_ID = models.ManyToManyField(SystemUser,null=True)
    user_img = models.CharField(default='dist/img/default.jpeg',max_length=100)
    uer_absolute_img = models.CharField(max_length=100,blank=True)
    description = models.CharField(max_length=100,blank=True)
    admin_active = models.BooleanField(default=False)
    log_path = models.CharField(max_length=100,blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name','email']
    objects = UserManager()



    @property
    def password_raw(self):
        raise AttributeError('Password raw is not a readable attribute')

    #: Use this attr to set user object password, example
    #: user = User(username='example', password_raw='password', ...)
    #: It's equal:
    #: user = User(username='example', ...)
    #: user.set_password('password')
    @password_raw.setter
    def password_raw(self, password_raw_):
        self.set_password(password_raw_)

    @property
    def is_superuser(self):
        if self.user_role == 'Admin':
            return True
        else:
            return False

    @property
    def is_staff(self):
        if self.is_authenticated:
            return True
        else:
            return False

    @is_staff.setter
    def is_staff(self, value):
        pass



    @is_superuser.setter
    def is_superuser(self, value):
        if value is True:
            self.user_role = 'Administrator'
        else:
            self.user_role = 'CommonUser'

    @property
    def is_online(self):
        last_time = cache.get('%s_last_time' % (self.username))

        if last_time:
            now = datetime.datetime.now()
            if now > last_time + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False

    @property
    def get_name(self):
        return self.name

    @property
    def get_user_img(self):
        return self.user_img

    @get_user_img.setter
    def get_user_img(self,img_location):
        self.user_img = img_location

    @property
    def get_absolute_user_img(self):
        return self.uer_absolute_img

    @property
    def get_update_time(self):
        return self.UpdateTime

    @get_update_time.setter
    def get_update_time(self,update_time):
        self.UpdateTime = update_time

    @property
    def get_description(self):
        return self.description

    @get_description.setter
    def get_description(self,description):
        self.description = description

    @property
    def get_user_role(self):
        return dict(self.ROLE_CHOICES).get(self.user_role)

    @property
    def get_department(self):
        return dict(self.DEPARTMENT_CHOICES).get(self.department)

    @get_department.setter
    def get_department(self,department):
        self.department = department













