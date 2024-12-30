from django.db import models
from django.contrib.auth.models import User


class RelyingParty(models.Model):
    name = models.CharField(max_length=64, unique=True)
    client_id = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class ConsentAccessToken(models.Model):
    token = models.CharField(max_length=64, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expired_at = models.DateTimeField()
    redirect_uri = models.CharField(max_length=256)
    state = models.CharField(max_length=32)


class ConsentAccessTokenScope(models.Model):
    token = models.ForeignKey(ConsentAccessToken, on_delete=models.CASCADE)
    scope = models.CharField(max_length=32)
