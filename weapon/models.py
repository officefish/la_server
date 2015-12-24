from django.db import models

# Create your models here.


class Weapon(models.Model):
    title = models.CharField(max_length=70)
    description = models.CharField(max_length=200)
    power = models.IntegerField(default=1)
    strength = models.IntegerField(default=1)
