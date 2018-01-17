from django.db import models
from user.models.user import SystemUser,User
from asset.models.asset_group import AssetGroup


class perm(models.Model):
    PERM_CHOICES = (
        ('Admin', '管理权限'),
        ('Comman', '普通权限'),
    )
    name = models.CharField(max_length=100,unique=True)
    CreateTime = models.DateTimeField(auto_now_add=True)
    perm = models.CharField(max_length=30,choices=PERM_CHOICES,default='Comman')
    SystemUser = models.ForeignKey(SystemUser,on_delete=models.CASCADE)
    asset_group = models.ForeignKey(AssetGroup,on_delete=models.CASCADE)
    descriptions = models.TextField(null=True,blank=True)
    create_perm_user = models.ForeignKey(User)
    active = models.BooleanField(default=False)



