from django.db import models

class ApiKey(models.Model):
    key = models.CharField(max_length=32)
    secret = models.CharField(max_length=256)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return "%s [%s]" % (self.key, self.id)

class ApiClient(models.Model):
    name = models.CharField(max_length=200, unique=True)
    key = models.CharField(max_length=32)

    def __unicode__(self):
        return "%s [%s]" % (self.name, self.id)
