from django.db import models


class War(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    ended = models.BooleanField(default=False)


class Castle(models.Model):
    barbarian_quantity = models.IntegerField()
    barbarian_max_needed = models.BooleanField(default=False)
    archer_quantity = models.IntegerField()
    archer_max_needed = models.BooleanField(default=False)
    giant_quantity = models.IntegerField()
    giant_max_needed = models.BooleanField(default=False)
    goblin_quantity = models.IntegerField()
    goblin_max_needed = models.BooleanField(default=False)
    wall_breaker_quantity = models.IntegerField()
    wall_breaker_max_needed = models.BooleanField(default=False)
    balloon_quantity = models.IntegerField()
    balloon_max_needed = models.BooleanField(default=False)
    wizard_quantity = models.IntegerField()
    wizard_max_needed = models.BooleanField(default=False)
    healer_quantity = models.IntegerField()
    healer_max_needed = models.BooleanField(default=False)
    dragon_quantity = models.IntegerField()
    dragon_max_needed = models.BooleanField(default=False)
    pekka_quantity = models.IntegerField()
    pekka_max_needed = models.BooleanField(default=False)
    minion_quantity = models.IntegerField()
    minion_max_needed = models.BooleanField(default=False)
    hog_rider_quantity = models.IntegerField()
    hog_rider_max_needed = models.BooleanField(default=False)
    valkyrie_quantity = models.IntegerField()
    valkyrie_max_needed = models.BooleanField(default=False)
    golem_quantity = models.IntegerField()
    golem_max_needed = models.BooleanField(default=False)
    witch_quantity = models.IntegerField()
    witch_max_needed = models.BooleanField(default=False)
    lava_hound_quantity = models.IntegerField()
    lava_hound_max_needed = models.BooleanField(default=False)


class Attack(models.Model):
    attacker = models.CharField(max_length=100)
    army = models.CharField(max_length=100)
    donor = models.CharField(max_length=100, null=True)
    war = models.ForeignKey(War)
    castle = models.ForeignKey(Castle, null=True)
