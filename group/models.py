from django.db import models

# Create your models here.


class Group (models.Model):
    title = models.CharField(max_length=70, default='')
    description = models.CharField(max_length=200, default='')

    @property
    def cards(self):
        return self.card_set.all().order_by('price')
