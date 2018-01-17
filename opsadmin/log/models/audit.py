from django.db import models
from asset.models.asset import Asset
import uuid
class AuditLog(models.Model):
    PERM_CHOICES = (
        ('Admin', '管理权限'),
        ('Comman', '普通权限'),
    )

    User = models.CharField(max_length=30)
    SystemUser = models.CharField(max_length=30)
    SystemUserPerm = models.CharField(max_length=30,choices=PERM_CHOICES,default='Comman')
    AssetGroup = models.CharField(max_length=30)
    Asset = models.ForeignKey(Asset,related_name='Asset')
    LogId = models.UUIDField(max_length=100,default=uuid.uuid4,blank=False,unique=True,editable=False)
    StartTime = models.DateTimeField(auto_now_add=True)
    EndTime = models.DateTimeField(auto_created=True, auto_now=True)

    @property
    def get_system_user_perm(self):
        return dict(self.PERM_CHOICES).get(self.SystemUserPerm)

