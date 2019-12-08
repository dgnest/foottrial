from django.db import models
from django.utils import timezone


class PublicIP(models.Model):

    public_ip = models.CharField(max_length=200)
    date_updated = models.DateTimeField(
        auto_now=True,
    )

    def __unicode__(self):
        return self.public_ip

    class Meta:
        db_table = 'publicip'
