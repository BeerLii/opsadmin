from django.db import models
from .user import User
class Permission(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    AssetEnable = models.BooleanField(default=False)
    PermEnable = models.BooleanField(default=False)
