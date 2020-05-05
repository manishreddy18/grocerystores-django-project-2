from django.conf import settings
from django.db import models



class StoresList(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    place = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=200, null=True)
    count = models.IntegerField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
