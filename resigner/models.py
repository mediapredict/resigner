from dpm_core.models import BaseModel
from django.db import models

class ApiKey(BaseModel):
    key = models.CharField(max_length=32)
    secret = models.CharField(max_length=256)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return "%s [%s]" % (self.key, self.id)