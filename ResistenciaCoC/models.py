from django.db import models


class War(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    ended = models.BooleanField(default=False)


class Castle(models.Model):
    barbarian_quantity = models.IntegerField()
    barbarian_level = models.IntegerField()
    archer_quantity = models.IntegerField()
    archer_level = models.IntegerField()
    giant_quantity = models.IntegerField()
    giant_level = models.IntegerField()
    goblin_quantity = models.IntegerField()
    goblin_level = models.IntegerField()
    wallbreaker_quantity = models.IntegerField()
    wallbreaker_level = models.IntegerField()
    balloon_quantity = models.IntegerField()
    balloon_level = models.IntegerField()
    wizard_quantity = models.IntegerField()
    wizard_level = models.IntegerField()
    healer_quantity = models.IntegerField()
    healer_level = models.IntegerField()
    dragon_quantity = models.IntegerField()
    dragon_level = models.IntegerField()
    pekka_quantity = models.IntegerField()
    pekka_level = models.IntegerField()
    minion_quantity = models.IntegerField()
    minion_level = models.IntegerField()
    hog_rider_quantity = models.IntegerField()
    hog_rider_level = models.IntegerField()
    valkyrie_quantity = models.IntegerField()
    valkyrie_level = models.IntegerField()
    golem_quantity = models.IntegerField()
    golem_level = models.IntegerField()
    witch_quantity = models.IntegerField()
    witch_level = models.IntegerField()
    lava_hound_quantity = models.IntegerField()
    lava_hound_level = models.IntegerField()


class Attack(models.Model):
    attacker = models.CharField(max_length=100)
    army = models.CharField(max_length=100)
    donor = models.CharField(max_length=100, null=True)
    war = models.ForeignKey(War)
    castle = models.ForeignKey(Castle, null=True)
