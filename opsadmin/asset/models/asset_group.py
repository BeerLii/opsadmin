from django.db import models

class AssetGroup(models.Model):

    name = models.CharField(max_length=100,unique=True)
    descriptions = models.TextField()
