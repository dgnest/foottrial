from django.db import models
from django.utils import timezone


class Hospital(models.Model):

    name = models.CharField(max_length=200)
    abbrev = models.CharField(max_length=20, blank=True)
    doctor = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    date_created = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'hospital'
