from django.db import models
import random
import string


def random_string(length):
    return ''.join(random.choice(_chars_for_secret) for _ in range(length))
    
def mk_key():
    return random_string(24)
    
def mk_secret():
    return random_string(256)


class ApiKey(models.Model):
    key = models.CharField(max_length=32, default=mk_key)
    secret = models.CharField(max_length=256, default=mk_secret)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return "%s [%s]" % (self.key, self.id)