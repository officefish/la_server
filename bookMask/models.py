from django.db import models
from django.db.models.signals import post_save, pre_delete

from book.models import Book
from card.models import Card

# Create your models here.
class MaskItem (models.Model):
    card = models.OneToOneField(Card)
    rarity = models.IntegerField(default=0)
    buy_cost = models.IntegerField(default=40)
    sale_cost = models.IntegerField(default=10)
    access_simple = models.IntegerField(default=0)
    max_simple = models.IntegerField(default=2)
    access_golden = models.IntegerField(default=0)
    max_golden = models.IntegerField(default=2)
    craft_available = models.BooleanField (default=True)

class BookMask (models.Model):
    book = models.OneToOneField(Book)
    items = models.ManyToManyField(MaskItem, through='MaskCollector')

    def create_book_mask (sender, instance, created, **kwargs):
        if created:
            BookMask.objects.create(book = instance)

    def delete_book_mask (sender, instance, **kwargs):
        bookMask = BookMask.objects.get (book = instance)
        bookMask.delete()

    post_save.connect (create_book_mask, sender=Book)
    pre_delete.connect (delete_book_mask, sender=Book)

class MaskCollector (models.Model):
    item = models.ForeignKey(MaskItem, related_name='mask_item')
    mask = models.ForeignKey(BookMask)

