from django.db import models


class War(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    ended = models.BooleanField(default=False)


class Attack(models.Model):
    attacker = models.CharField(max_length=100)
    army = models.CharField(max_length=100)
    war = models.ForeignKey(War)
