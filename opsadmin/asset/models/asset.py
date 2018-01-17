from django.db import models
from .asset_group import *

class Asset(models.Model):
    ASSET_TYPE_CHOICES = (
        ('server', u'服务器'),
        ('networkdevice', u'网络设备'),
        ('vm',u'虚拟机'),
        ('firewall',u'防火墙')
    )

    STATUS_CHOICES = (
        ('Online', u'在线'),
        ('Not Online', u'不在线')
    )

    ENV_CHOICES = (
        ('prod',u'生产环境'),
        ('dev',u'开发环境'),
        ('test',u'测试环境')
    )

    asset_type = models.CharField(choices=ASSET_TYPE_CHOICES,max_length=64, default='server')
    name = models.CharField(max_length=64, unique=True)
    manage_ip = models.GenericIPAddressField(unique=True)
    external_ip = models.GenericIPAddressField(null=True,blank=True,unique=True)
    asset_status = models.CharField(choices=STATUS_CHOICES,max_length=30,null=True,blank=True)
    descriptions = models.TextField()
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, auto_now=True)
    asset_env = models.CharField(choices=ENV_CHOICES,max_length=100,default='prod')
    asset_group = models.ManyToManyField(AssetGroup,default=None)



    @property
    def get_asset_type(self):
        return dict(self.ASSET_TYPE_CHOICES).get(self.asset_type)

    @property
    def get_asset_status(self):
        return dict(self.STATUS_CHOICES).get(self.asset_status)

    @property
    def get_asset_env(self):
        return dict(self.ENV_CHOICES).get(self.asset_env)


class Server(models.Model):
    asset = models.OneToOneField(Asset,on_delete=models.CASCADE)
    model = models.CharField(verbose_name=u'型号',max_length=128,null=True, blank=True )
    sn = models.CharField(u'SN号', max_length=128,null=True,blank=True)
    os_type = models.CharField(u'操作系统类型', max_length=64, blank=True, null=True)
    os_distribution = models.CharField(u'发型版本', max_length=64, blank=True, null=True)
    os_release = models.CharField(u'操作系统版本', max_length=64, blank=True, null=True)



class CPU(models.Model):
    asset = models.OneToOneField(Asset,on_delete=models.CASCADE)
    cpu_model = models.CharField( max_length=128,blank=True)
    cpu_count = models.CharField(u'物理cpu个数',max_length=10,blank=True,null=True)
    cpu_core_count = models.CharField(u'cpu核数',max_length=10,blank=True,null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True,null=True)

class RAM(models.Model):
    asset = models.ForeignKey(Asset,on_delete=models.CASCADE)
    sn = models.CharField(max_length=128, blank=True,null=True)
    model =  models.CharField(max_length=128,blank=True,null=True)
    slot = models.CharField(max_length=64,blank=True,null=True)
    capacity = models.CharField(max_length=10,blank=True,null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True,null=True)


class Disk(models.Model):
    asset = models.ForeignKey(Asset,on_delete=models.CASCADE)
    sn = models.CharField(max_length=128, blank=True,null=True)
    slot = models.CharField(max_length=64)
    model = models.CharField(max_length=128,blank=True,null=True)
    capacity = models.FloatField()
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

class NIC(models.Model):
    asset = models.ForeignKey(Asset,on_delete=models.CASCADE)
    name = models.CharField(u'网卡名', max_length=64, blank=True,null=True)
    sn = models.CharField(u'SN号', max_length=128, blank=True,null=True)
    model =  models.CharField(u'网卡型号', max_length=128, blank=True,null=True)
    macaddress = models.CharField(u'MAC', max_length=64,unique=True)
    ipaddress = models.GenericIPAddressField(u'IP', blank=True,null=True)
    netmask = models.CharField(max_length=64,blank=True,null=True)
    bonding = models.CharField(max_length=64,blank=True,null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True,null=True)


