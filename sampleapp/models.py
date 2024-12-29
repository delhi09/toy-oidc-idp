from django.db import models


class RelyingParty(models.Model):
    name = models.CharField(max_length=64, unique=True)
    client_id = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name
